import sublime, sublime_plugin, sys, re


footnote = re.compile(r'(\[\^([a-zA-Z0-9]+?)\])\s*[^:]') 
# trailing gumpf to prevent this from matching on the actual footnote.[^test0]
# a test selection.[^test1] this is text of markdown footnotes.[^test2] in a comment
# such that this class can test on itself![^nomatch0]

class CheckRefCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('running referencr... ')
		print("Referencr - looking for markdown reference matches.")
		unmatched_fn = {}
		all_buffer = self.view.substr(sublime.Region(0, self.view.size()))
		print("... looking in all current buffer for matches with " + footnote.pattern)
		matches = footnote.finditer(all_buffer)
		for m in matches :
			grp = m.group(1) # this is the real note. group(0) has trailing gumpf
			fn = m.group(2)
			fn_textvalue = re.compile(r'\s*(\[\^' + fn + r'\]\s*:\s*(.*))$\n', re.MULTILINE)
			#print("... searching now for note " + fn_textvalue.pattern)
			fn_match = fn_textvalue.search(all_buffer)
			if fn_match:
				print(grp + " got match")
			else:
				lineno = all_buffer.count("\n", 0, m.start()) + 1;
				unmatched_fn[grp]="line " + str(lineno) + "; pos " + str(m.span())
				print(grp + " no match found!")

		if len(unmatched_fn) > 0:
			unmatched_msg = ""
			for key in unmatched_fn:
				unmatched_msg = unmatched_msg + key + " at " + unmatched_fn[key] + "\n"
			sublime.error_message("Unmatched footnotes!\n" + str(unmatched_msg))
		else :
			msg = "All OK!"
			print(msg)
			sublime.status_message(msg)
		return

class CompileRefCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('running referencr... ')
		print("Referencr - compiling markdown reference matches.")
		unmatched_fn = {}
		matched_fn = {}
		all_buffer = self.view.substr(sublime.Region(0, self.view.size()))
		print("... looking in all current buffer for matches with " + footnote.pattern)
		matches = footnote.finditer(all_buffer)
		newview = self.view.window().new_file()
		for m in matches :
			grp = m.group(1) # this is the real note. group(0) has trailing gumpf
			fn = m.group(2)
			fn_textvalue = re.compile(r'\s*(\[\^' + fn + r'\]\s*:\s*(.*))$\n', re.MULTILINE)
			#print("... searching now for note " + fn_textvalue.pattern)
			fn_match = fn_textvalue.search(all_buffer)
			if fn_match:
				print(grp + " got match")
				matched_fn[fn] = fn_match.grp(2)
			else :
				print(grp + " no match found")



'''
[^test0]: hi, this is a friendly footnote.

this is a comment[^test3]

[^test1]: it exists to match to the test note above.

Footnotes entries can be spread throughout a Pandoc documents, not just at the end.

[^test2]: the second match

 [^test3]: this note is indented a bit.

''' 
