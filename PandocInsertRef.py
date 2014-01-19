import sublime, sublime_plugin, sys, re, operator

footnote_insert = re.compile(r'(\[\^([a-zA-Z0-9]+?)\])\s*[^:]') 
footnote_text = re.compile(r'^\s*(((\[\^([a-zA-Z0-9]+?)\])\s*:).*?)$', re.MULTILINE) 

class InsertRefCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('Insert Reference... ')
		print("Referencr - Insert a new Reference.")

