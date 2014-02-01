import sublime, sublime_plugin, sys, re, operator

footnote_insert = re.compile(r'(\[\^([a-zA-Z0-9]+?)\])\s*[^:]') 
footnote_text = re.compile(r'^\s*(((\[\^([a-zA-Z0-9]+?)\])\s*:).*?)$', re.MULTILINE) 
spaces = re.compile(r"[\s\W]+", re.MULTILINE)
# the following is deliberately greedy. we're trying to find the newlines at EOF
eof_newlines0 = re.compile(r'^(\s+)$', re.MULTILINE)

# global settings variables.
_set = sublime.load_settings('PandocReferencr.sublime-settings')
_footnote_placement = _set.get('footnote_placement', 'document')
_space_prepend_count = _set.get('space_prepend_count', 0)
_default_footnote_prefix = _set.get('default_footnote_prefix', 'fn')
if _space_prepend_count > 3:
	print ("space prepend count value is too large. forcing to maxvalue=3 ... was " + str(_space_prepend_count))
	_space_prepend_count = 3;
print("InsertFootnote settings complete. Footnote placement='" + str(_footnote_placement) + "'; prepended spaces='" + str(_space_prepend_count) + "'; default prefix='" + str(_default_footnote_prefix) +"'")
# end global settings variables.

class InsertFootnoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('Insert Reference... ')
		print("Referencr - Insert a new Reference")
		v = self.view
		w = v.window()
		r = v.sel()[0]
		t = spaces.sub("", self.view.substr(r).lower().strip())
		if not t:
			t = _default_footnote_prefix

		w.show_input_panel("Enter footnote id:", t, lambda s: self.set_ref(s), None, None)
		pass

	def set_ref(self, ref):
		print("user entered: " + ref)
		self.view.run_command("insert_entered_fn",
				{"ref":ref}
			)

class InsertEnteredFnCommand(sublime_plugin.TextCommand):
	def run(self, edit, ref):
		_ref = "[^" + ref + "]"
		v = self.view
		w = v.window()
		pos = v.sel()
		print("position of cursor is " + str(pos))
		i = 0
		for r in pos:
			print(str(i) + ": inserting '" + _ref + "' at end of region from " + str(r.begin()) + " to " + str(r.end()))
			v.insert(edit, r.end(), _ref)
			i = i+1
		w.show_input_panel("Enter footnote text:", '', 
			lambda s:self.set_footnote_text(_ref, s), None, None)
		pass

	def set_footnote_text(self, fnref, fntext):
		print("for ref" + fnref + "user entered: '" + fntext + "'")
		self.view.run_command("insert_entered_footnote_text",
				{ "fnref":fnref, "fntext":fntext}
			)
		pass

class InsertEnteredFootnoteTextCommand(sublime_plugin.TextCommand):
	def run(self, edit, fnref, fntext):
		(insert_pt, is_two_newlines_required) = self.calc_fn_text_insert()
		prepend = self.get_prepend(is_two_newlines_required)
		self.view.insert(edit, insert_pt, prepend + fnref + ": " + fntext + "\n")
		pass

	def get_prepend(self, is_two_newlines_required):
		prepend = ""
		if is_two_newlines_required:
			prepend += "\n\n"
		else:
			prepend += "\n"
		i = 0
		while i < _space_prepend_count:
			i += 1
			prepend = prepend + " "
		return prepend

	def calc_fn_text_insert(self):
		# a complex and horrible procedure to locate 
		# the best position to insert the fn text.
		buffer_size = self.view.size()
		match_start = buffer_size
		match_end = buffer_size
		all_buffer = self.view.substr(sublime.Region(0, buffer_size))
		#we're looking for multiple whitespace/newlines at the end of the file.
		matches0 = eof_newlines0.finditer(all_buffer)
		if matches0:
			# primitively iterate over the whole thing reassigning the start and end.
			for match in matches0:
				(match_start, match_end) = match.span()
				# the last one in the list is the one we want anyway.
				print("start={0}; end={1}; eof={2}".format(match_start, match_end, buffer_size))
			if match_end+2 < buffer_size : 
				# we did not find the end of the file.
				# usually because there is not a newline at the end of it.
				# therefore simply the end of the buffer is the one we want
				# but put two newlines at the start of the inserted note.
				return buffer_size, True
			else :
				# it's the EOF region. the match start is where we begin to insert
				# use a single newline at the start of the footnote.
				# if you have multiple newlines at the end of your file
				# this will insert at the TOP of the newlines.
				# this will get confused by complex mixtures of whitespace
				# and newlines. your EOF should be cleaner than that. ;-)
				return match_start, False
		else:
			# there were no matches, just use the EOF and prepend 2 newlines.
			return buffer_size, True
