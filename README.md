PandocReferencr
===============

This plugin totes up the Pandoc/Markdown footnote references in a file ([^reference1]) and checks there is an entry for the reference. It also checks for orphaned footnote entries (i.e. footnote text that has no insert point in the main body).

Default command palette (and key bindings):
    Pandoc Footnotes: Check (ctrl+super+alt+r)
    Pandoc Footnotes: Insert New (super+alt+r)

There are also menu items under "Tools - Pandoc Footnotes"

Inserting Footnotes
-------------------

When you insert a footnote, you will be asked for the footnote id. If you have any selections, the first selection will pre-fill the footnote id field. The footnote id is inserted at the end of the selection, otherwise at the current cursor position.

After you enter the footnote id, you will be asked to supply the footnote text. The footnote text is inserted at the end of the document.

There are a number of changes coming to this behaviour. Please see the comments on [this issue](https://github.com/scotartt/PandocReferencr/issues/1) for a description of how that behaviour will work.

Checking Footnotes
------------------

This checks that each footnote id inserted in the text has a corresponding footnote text item, and that all footnote text items has a matching footnote id inserted in the text.

When you check the footnotes, if everything is OK in current buffer (open document), that is all the footnote ids and texts match, then the status line will say "All OK!"

If there are errors, a warning dialog will tell you the ids and line numbers where there are issues.


  [^reference1]: The text of reference1 is this text.
