PandocReferencr
===============

This plugin totes up the Pandoc/Markdown footnote references in the current  file  and checks there is an entry for the reference. It also checks for orphaned footnote entries (i.e. footnote text that has no insert point in the main body).

    A footnote in pandoc looks like this.[^footnoteid1]

    [^footnoteid1]: And this is the text of the footnote.

There is also a very useful command for inserting footnotes, which prompts you for a footnote id (with defaults) and then the text for the footnote, which is inserted at the end of the file (soon to be a configurable location). See below for more information.


Installing it in Sublime Text
-----------------------------

It's available from Package Control - https://sublime.wbond.net/packages/Pandoc%20Referencer


Invoking it
-----------

Default command palette (and key bindings):

* 'Pandoc Footnotes: Check' (ctrl+super+alt+r)

* 'Pandoc Footnotes: Insert New' (super+alt+r)

There are also menu items under "Tools -> Pandoc Footnotes". See below for behaviour.


Settings
--------

Select "Preferences -> Package Settings -> Pandoc Referencr -> Settings - User" to customised your settings. You can also override the keyboard bindings if you prefer other keystrokes to the ones I've provided.

Here are the default settings:

    {
        // footnote_placement is either 'document' or 'paragraph'. 
        "footnote_placement": "document",

        // how many spaces to put before the footnote text. 
        // default is 0. Must be < 4. Values other than 0 not strictly
        // conformant to the Pandoc spec, but they work if < 4 (four spaces
        // or a tab, or more, would make the text block into a code block)
        "space_prepend_count": 0,

        // by default, what is the default prefix to use for footnotes 
        // when no other value can be computed. default is "fn".
        "default_footnote_prefix": "fn",
    }

"Footnote placement" is not currently used; see below. Footnotes are currently always at the end of the document.


Inserting Footnotes (super+alt+r)
-------------------

Command: insert_footnote

When you insert a footnote, you will be asked for the footnote id. If you have any selections, the first selection will pre-fill the footnote id field. The footnote id is inserted at the end of the selection, otherwise at the current cursor position.

After you enter the footnote id, you will be asked to supply the footnote text. The footnote text is inserted at the end of the document. It tries to insert the footnote cleanly. If there is no newline at the end of the file, it compensates for this. If there are multiple newlines at the end of the file, it inserts the footnote at the top of the newlines. If there is a complex mixture of whitespace and newlines at the end of the file, it acts fairly sensibly, but not as cleanly. You could try keeping the end of your file in a cleaner state ;-) ... there are settings for this:

    "default_line_ending": "unix",
    "ensure_newline_at_eof_on_save": true,

There are a number of changes coming to this behaviour. Please see the comments on [this issue](https://github.com/scotartt/PandocReferencr/issues/1) for a description of how that behaviour will work.

Checking Footnotes (ctrl+super+alt+r)
------------------

Command: check_footnotes

This checks that each footnote id inserted in the text has a corresponding footnote text item, and that all footnote text items has a matching footnote id inserted in the text.

When you check the footnotes, if everything is OK in current buffer (open document), that is all the footnote ids and texts match, then the status line will say "All Footnotes OK!"

If there are errors, a warning dialog will tell you the footnote ids and line numbers where there are issues, up to five issues. If there are more than five issues with the footnotes, you are only shown the first four, plus additional line alerting you to the presence of more footnotes errors.

    For example, this text has a footnote with a valid footnote 
    text.[^footnote1] However this note is missing,[^missing1] if 
    you invoke check_references on this file it will say there's 
    TWO errors. The first one is 'missing1'.

    [^hithere0]: The second error is that there is no 'hithere0'
    footnote inserted anywhere in the main body text (Orphaned 
    footnote text).

    [^footnote1]: This is the valid footnote text.

Licence
-------

This software is licensed using the GNU GPL version 2. 

No warranty, responsibility, or liability is assumed by the author in any use of this software. 

