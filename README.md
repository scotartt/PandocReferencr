PandocReferencr
===============

This plugin totes up the Pandoc/Markdown footnote references in the current  file  and checks there is an entry for the reference. It also checks for orphaned footnote entries (i.e. footnote text that has no insert point in the main body).

    A footnote in pandoc looks like this.[^footnoteid1]

    [^footnoteid1]: And this is the text of the footnote.


Installing it in Sublime Text
-----------------------------

It's available from Package Control - https://sublime.wbond.net/packages/Pandoc%20Referencer


Invoking it
-----------

Default command palette (and key bindings):

* 'Pandoc Footnotes: Check' (ctrl+super+alt+r)

* 'Pandoc Footnotes: Insert New' (super+alt+r)

There are also menu items under "Tools - Pandoc Footnotes"

Inserting Footnotes (super+alt+r)
-------------------

When you insert a footnote, you will be asked for the footnote id. If you have any selections, the first selection will pre-fill the footnote id field. The footnote id is inserted at the end of the selection, otherwise at the current cursor position.

After you enter the footnote id, you will be asked to supply the footnote text. The footnote text is inserted at the end of the document.

There are a number of changes coming to this behaviour. Please see the comments on [this issue](https://github.com/scotartt/PandocReferencr/issues/1) for a description of how that behaviour will work.

Checking Footnotes (ctrl+super+alt+r)
------------------

This checks that each footnote id inserted in the text has a corresponding footnote text item, and that all footnote text items has a matching footnote id inserted in the text.

When you check the footnotes, if everything is OK in current buffer (open document), that is all the footnote ids and texts match, then the status line will say "All OK!"

If there are errors, a warning dialog will tell you the ids and line numbers where there are issues.

    For example, this text has a footnote with a valid footnote 
    text.[^footnote1] However this note is missing,[^missing1] if 
    you invoke check_references on this file it will say there's 
    TWO errors. The first one is 'missing1'.

    [^hithere0]: The second error is that there is no 'hithere0'
    footnote inserted anywhere in the main body text (Orphaned 
    footnote text).

    [^footnote1]: This is the valid footnote text.

