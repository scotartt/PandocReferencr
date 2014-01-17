import sublime, sublime_plugin, sys, re, operator


footnote_insert = re.compile(r'(\[\^([a-zA-Z0-9]+?)\])\s*[^:]') 
footnote_text = re.compile(r'^\s*(((\[\^([a-zA-Z0-9]+?)\])\s*:).*?)$', re.MULTILINE) 

# trailing gumpf to prevent this from matching on the actual footnote.[^test0]
# a test selection.[^test1] this is text of markdown footnotes.[^test2] in a comment
# such that this class can test on itself![^nomatch0]***<-this ref has no match.

class CheckRefCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('running referencr... ')
		print("Referencr - looking for markdown reference matches and unmatched references.")
		unmatched_fn = [] # list of dicts!
		matched_fn = {} # dict of dicts!
		all_buffer = self.view.substr(sublime.Region(0, self.view.size()))
		## first find the insert values, that should have matching text items (with the colons)
		matched_arrays = self.match_fninserts(matched_fn, unmatched_fn, all_buffer);
		matched_fn = matched_arrays[0]
		unmatched_fn = matched_arrays[1]

		## next, find the text values (with the colon), that have no insert value
		matched_arrays = self.match_fntexts(matched_fn, unmatched_fn, all_buffer);
		unmatched_fn = matched_arrays[1] 
		## the above function only modifies the unmatched data.

		self.alert(unmatched_fn)
		return

	def alert(self, unmatched_fn):
		if len(unmatched_fn) > 0:
			unmatched_msg = ""
			## first get the fn_inserts with no fn_text
			from operator import itemgetter
			newlist = sorted(unmatched_fn, key=itemgetter('line'))
			i = 0;
			for item in newlist:
				i = i+1
				unmatched_msg = unmatched_msg + "(" + str(i) + ") " + item['err_msg'] + "\n\n"
			
			sublime.error_message("Unmatched footnotes!\n\n" + str(unmatched_msg))
		else :
			msg = "All OK!"
			print(msg)
			sublime.status_message(msg)
		return

	## find the insert values, that should have matching text items (with the colons)
	## fully populates the matched_fn dictionary with all the data of the matched footnote pairs.
	def match_fninserts(self, matched_fn, unmatched_fn, all_buffer):
		print("... looking in all current buffer for matches with " + footnote_insert.pattern)
		matches = footnote_insert.finditer(all_buffer)
		for m in matches :
			grp = m.group(1) # this is the real note. group(0) has trailing gumpf
			fn = m.group(2)
			## row and column of the footnote in the main text
			rowcol = self.view.rowcol(m.start())
			line = rowcol[0]+1 # it's zero-based!
			col = rowcol[1]+1 # it's zero-based!
			fn_textvalue = re.compile(r'^\s*(\[\^' + fn + r'\]\s*:\s*(.*))$\n', re.MULTILINE)
			fn_match = fn_textvalue.search(all_buffer)
			if fn_match:
				## row and column of the matching footnote text.
				fntext_rowcol = self.view.rowcol(fn_match.start())
				fntext_line = fntext_rowcol[0]+1 # it's zero-based!
				fntext_col = fntext_rowcol[1]+1 # it's zero-based!
				# all the footnote except the leading space and trailing newline
				fntext = fn_match.group(1) 
				data = { 
					'fn_insert': grp, 'fn_num':fn, 'line':line, 'col':col,
					'fn_text_line':fntext_line, 'fn_text_col':fntext_col,
					'fn_text':fntext,
					'err_msg':'no error found'
				}
				matched_fn[grp]=data 
				print(data['fn_insert'] + " at line " + str(data['line']) + ", col " + str(data['col']) 
					+ "; match at line " + str(data['fn_text_line']) + ", value: '" + data['fn_text'] + "'")
			else:	
				data = {'fn_insert':grp, 'fn_num': fn, 'line':line,'col':col, 
					    'err_msg':"line "+str(line)+"; col "+str(col)+"; '"+ grp+"' with no matching footnote text entry."
				}
				unmatched_fn.append( data )
				print(data['err_msg'])
				#finish

		return (matched_fn, unmatched_fn)

	## find the text values (with the colons), that should have matching insert items
	## this function must be run with a populated matched_fn dict containing the inserts footnote data.
	def match_fntexts(self, matched_fn, unmatched_fn, all_buffer):
		print("... looking in all current buffer for matches with " + footnote_text.pattern)
		matches = footnote_text.finditer(all_buffer)
		for m in matches :
			grp = m.group(3) # this is the real note. group(0) has leading gumpf, group(1), trailing gumpf
			fn = m.group(4)
			notetext = m.group(2)
			alltext = m.group(1)
			## row and column of the footnote text
			rowcol = self.view.rowcol(m.start())
			line = rowcol[0]+1 # it's zero-based!
			col = rowcol[1]+1 # it's zero-based!
			if grp in matched_fn: 
				# this will be found from the earlier run (gah! not independent of order!!!)
				# just do nothing here except print success, matched_fn has got this data.
				found_fn = matched_fn[grp]
				print(found_fn['fn_insert'] + " at line " + str(found_fn['line']) + ", col " + str(found_fn['col']) 
					+ " got match at line " + str(found_fn['fn_text_line']) + " text value: '" + found_fn['fn_text'] + "'")
			else:	
				data = {'fn_insert' : grp, 'fn_num' : fn, 'line':line,'col':col,
					'err_msg':"line "+str(line)+"; col "+str(col)+"; '"+grp+"' fn text with no matching insert. Orphaned footnote is '"+alltext+"'"
				}		
				unmatched_fn.append( data )
				print(notetext + " no matching fn insert found!")
				#finish

		return (matched_fn, unmatched_fn)


class CompileRefCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('running referencr... ')
		print("Referencr - compiling markdown reference matches.")
		unmatched_fn = {}
		matched_fn = {}
		all_buffer = self.view.substr(sublime.Region(0, self.view.size()))
		print("... looking in all current buffer for matches with " + footnote.pattern)
		matches = footnote.finditer(all_buffer)
		outview = self.new_view(edit, self.view)
		outedit = outview.begin_edit
		outview.insert(outedit, 0, "Hello World")
		outview.end_edit(outedit)

		for m in matches :
			grp = m.group(1) # this is the real note. group(0) has trailing gumpf
			fn = m.group(2)
			fn_textvalue = re.compile(r'\s*(\[\^' + fn + r'\]\s*:\s*(.*))$\n', re.MULTILINE)
			#print("... searching now for note " + fn_textvalue.pattern)
			fn_match = fn_textvalue.search(all_buffer)
			if fn_match:
				print(grp + " got match")
				matched_fn[fn] = fn_match.group(2)
			else :
				print(grp + " no match found")

	def new_view(self, edit, ownerview):
		ownername = ownerview.file_name();
		if not ownername:
			ownername = ownerview.name()
			if not ownername:
				ownername = ownerview.id()
		newview = ownerview.window().create_output_panel(ownername + ".refs")
		##ownerview.window().show_panel("output." + ownername + ".refs")
		ownerview.window().focus_view(newview)
		return newview


'''
[^test0]: hi, this is a friendly footnote.

this is a comment[^test3]

[^test1]: it exists to match to the test note above.

Footnotes entries can be spread throughout a Pandoc documents, not just at the end.

[^test2]: the second match

 [^test3]: this note is indented a bit.

 [^NOMATCH1]: this note has no matching footnote insert anywhere.

''' 
