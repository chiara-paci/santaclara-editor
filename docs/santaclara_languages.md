#Santa Clara Language

Santa Clara Language is a bb-code style language for formatting text.

##Space and newline

Like in html, space are collapsed: you can write any number of spaces
and they will be rendered as a single space.

Single newline are transformed in a space (and eventually collapsed if
there is spaces surrounding it). Multiple newlines (two or more) are
used to separate paragraphs. So if you need a new paragraph you have
to type two newlines.

##Tags

Santa Clara Language has two kinds of tags: isolated tags and
surrounding tags. Some tags can exist in both forms.

###Isolate tags

Isolate tags are like:
```
[<tag_name> <args>/]
```
i.e, one bracket sequence ending with _/]_ (the slash is mandatory).

Isolate tags are translate in simple html piece. For example, a tag like
```
[hr/]
```
will be rendered as:
```
<hr/>
```

###Surrounding tags

Surrounding tags are like: 
``` 
[<tag_name> <args>]<content>[/<tag_name>] 
```
i.e, two bracket sequence with the same _tag_name_ (the slash
in second tag is mandatory) and surrounding _content_.

Surrounding tags transform _content_ in html and can be nested. For example:
```
[b]for [i]example[/i][/b]
```
will be rendered as:
```
<b>for <i>example</i></b>
```
The rendering it's not just inserting some html tag but could be very complex.

###Arguments

Both isolate and surrounding tags could take arguments. They are
parsed with a shell-like syntax, where you can use double or single
quote to group argument pieces. Arguments are not positional and you
have to write them with _name_=_value_ syntax:
```
[<tag_name> <arg1>=<value1> <arg2>=<value2> ...]
```

Some tags can accept this syntax:
```
[<tag_name>=<value0> <arg1>=<value1> <arg2>=<value2> ...]
```
a shortcut for:
```
[<tag_name> <arg0>=<value0> <arg1>=<value1> <arg2>=<value2> ...]
```
where _arg0_ is a default argument, often an argument named _tag_name_.

###Special characters

You can write bracket and slash using a doubled version:

| sequence | will become | render |
|:-------:|:-------:|:------:|
|\\\\|\&#47;|\|
|[[|\&#91;|[|
|]]|\&#93;|]|

###Extending

You can define your own tags. See [How To Extend Language](extend_language.md).

##Simple and full version

You can use two version of the Santa Clara Language, _simple_ and
_full_ (see [Template Filters](santa_clara_editor.md)). The _simple_
version use a subset of the tags.

The _full_ version is intended to render entire page, with both text
formatting (italics, bold, quote, ecc.) and layout tags (adding
vertical space, list, heading, ecc.).

The _simple_ version has just text formatting tags and is intended to
render simpler text, like comments, notes, forum posts, ecc.

You can [extend](extend_language.md) both list.


##Tag Reference

| tag name | simple | extended | has argument | description |
|----|:----:|:----:|:----:|----|
| [b][/b] |X|X||bold|
| [i][/i] |X|X||italics|
| [t][/t] |X|X||terminal type|
| [u][/u] |X|X||underline|
| [s][/s] |X|X||linethrough|
| [o][/o] |X|X||overline|
| [sc][/sc] |X|X||small caps|
| [color][/color] |X|X|X|color|
| [center][/center] |X|X||align center|
| [left][/left] |X|X||align left|
| [right][/right] |X|X||align right|
| [justify][/justify] |X|X||justify|
| [quote][/quote] |X|X|X|quote|
| [cite][/cite] |X|X|X|citation|
| [code][/code] |X|X||preformatted with code look|
| [term][/term] |X|X||preformatted with terminal look|
| [hr/] ||X||horizontal line|
| [br/] ||X||line break|
| [space/] ||X||space|
| [hspace/] ||X|X|horizontal space|
| [vspace/] ||X|X|vertical space|
| [ref][/ref] ||X|X|internal reference|
| [url][/url] ||X|X|url|
| [li][/li] ||X||list item|
| [dt][/dt] ||X||dictionary list item|
| [dd][/dd] ||X||dictionary list item|
| [item][/item] ||X||punctuated list|
| [enum][/enum] ||X||numbered list|
| [dict][/dict] ||X||dictionary list|
| [h _num_][/h _num_] ||X||heading of level _num_|

###color

```
[color fore=<foreground_color> back=<background_color>]<text>[/color]
```

Arguments are not mandatory.

###quote

```
[quote name=<person> name_url=<person_url> ts=<timestamp> url=<text_url>]<text>[/quote]
[quote=<person> name_url=<person_url> ts=<timestamp> url=<text_url>]<text>[/quote]
```

Arguments are not mandatory.

###cite

```
[cite ref=<internal_reference> page=<page_number(s)> url=<url> label=<label>]<text>[/cite]
```

###hspace

```
[hspace w=<len>/]
```

Arguments are not mandatory (default: _len_=1em).

###vspace

```
[vspace h=<len>/]
```

Arguments are not mandatory (default: _len_=1em).

###ref

```
[ref ref=<internal_reference>]<text>[/ref]
[ref=<internal_reference>]<text>[/ref]
```

Without "#".

###url

```
[url url=<address>]<text>[/url]
[url=<address>]<text>[/url]
```

