import sublime, sublime_plugin, sys, re, operator

footnote_insert = re.compile(r'(\[\^([a-zA-Z0-9]+?)\])\s*[^:]') 
footnote_text = re.compile(r'^\s*(((\[\^([a-zA-Z0-9]+?)\])\s*:).*?)$', re.MULTILINE) 
spaces = re.compile(r"[\s\W]+", re.MULTILINE)

_s = sublime.load_settings('PandocReferencr.sublime-settings')
_footnote_placement = _s.get('footnote_placement', 'document')
_space_prepend_count = _s.get('space_prepend_count', 0)
_default_footnote_prefix = _s.get('default_footnote_prefix', 'rfn')
if _space_prepend_count > 2:
	print ("space prepend count value is too large. forcing to maxvalue=2 ... was " + str(_space_prepend_count))
	_space_prepend_count = 2;

class InsertFootnoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('Insert Reference... ')
		print("Referencr - Insert a new Reference at " + _footnote_placement + " end with " + str(_space_prepend_count) + " prepended spaces and default prefix: " + _default_footnote_prefix)
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
		self.view.insert(edit, self.view.size(), "\n  " + fnref + ": " + fntext + "\n")
		pass

# test block
# text comment block
# comments for ref insert test.

