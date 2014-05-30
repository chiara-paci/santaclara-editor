#Template Filters

##Invocation

You can use filters defined by santaclara-editor with:
```
{% load santa_clara_editor %}
```

Santa Clara Editor filters format text written in [Santa Clara
Language](docs/santaclara_languages.md), a bb-code style language.

##Filters

###santa_clara_lang

Format _text_ using full version of [Santa Clara
Language](docs/santaclara_languages.md).

```
{{ <text>|santa_clara_lang }}
```

###santa_clara_simple

Format _text_ using reduced version of [Santa Clara
Language](docs/santaclara_languages.md).

```
{{ <text>|santa_clara_simple }}
```

###santa_clara_json

Format _text_ using full version of [Santa Clara
Language](docs/santaclara_languages.md) and clean it to be inserted in
a json response.

```
{{ <text>|santa_clara_json }}
```

###santa_clara_raw

Return the raw version of _text_ (with '['), cleaned to be inserted in a json response.

```
{{ <text>|santa_clara_raw }}
```

###santa_clara_plain

Replace newline with break:

```
{{ <text>|santa_clara_plain }}
```

