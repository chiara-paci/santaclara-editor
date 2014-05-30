#Template Tags

##Invocation

You can use tag defined by santaclara-css with:
```
{% load css_tags %}
```

Santa Clara Css Tags replace several css rows with just one tag (for
example, dealing with several browser difference adding -moz-* or -o-*
or -webkit-* or -ms-* stuff).

##Tags

###columned

It defines columned style for an object:
```
{% columned <num_col> %}
```

Equivalent to: 
```
... {
  ...
  column_count: <num_col>
  ...
}
```

###background_gradient

```
{% background_gradient <grad_style> <start> <stop> %}
```

_start_ and _stop_ are colours; _grad_style_ is top, bottom, left, ecc.

It's equivalent to:
```
... {
  ...
  background: linear-gradient(<style>,<start>,<stop>);
  ...
}
```

###border_radius

```
{% border_radius <radius> %}
```

It's equivalent to:
```
... {
  ...
  border-radius: <radius>;
  ...
}
```

###border_shadow

```
{% border_shadow <shadow> %}
```

It's equivalent to:
```
... {
  ...
  border-shadow: <shadow>;
  ...
}
```

###border_radius_pos

```
{% border_radius_pos <pos> <radius> %}
```

It defines a radius _radius_ at position _pos_, wher _pos_ can be: right, left,
top, bottom, top-right, top-left, bottom-right, bottom-left.

For example, with _pos_=top it's equivalent to:
```
... {
  ...
  border-top-left-radius: <radius>;
  border-top-right-radius: <radius>;
  ...
}
```

###text_rotation

```
{% text_rotation <degree> %}
```

It's equivalent to:
```
... {
  ...
  transform: rotate(<degree>deg);
  ...
}
```

###icon_file_manager_levels

```
{% icon_file_manager_levels <num_levels> <step> %}
```

_levels_ must be an integer and _step_ a float. 

It defines several css classes (_.iconlevel#_) for indentation in a tree-like style:
```
.iconlevel0, iconlevel1, ..., .iconlevel<num_levels-1> {
   vertical-align: bottom;
   font-size: 1.1em;
}

.iconlevel0 {
   padding-left: 0;
}

.iconlevel1 {
   padding-left: <step>em;
}

.iconlevel2 {
   padding-left: <2*step>em;
}

...

.iconlevel<num_levels-1> {
   padding-left: <(num_levels-1)*step>em;
}
```

