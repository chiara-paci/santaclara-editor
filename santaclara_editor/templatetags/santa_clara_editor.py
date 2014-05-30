# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from santaclara_editor.languages import language_register


import re

### django filters

register = template.Library()

def santa_clara_plain(value,ind=0,autoescape=None): 
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    txt=esc(value).replace("\n","<br/>")
    return mark_safe(txt)
register.filter("santa_clara_plain",santa_clara_plain)
santa_clara_plain.needs_autoescape = True

def santa_clara_raw(value,ind=0,autoescape=None): 
    txt=value.replace('\\',r"&#92")
    txt=txt.replace('\r\n',"&#10")
    txt=txt.replace('\n\r',"&#10")
    txt=txt.replace('\r',"&#10")
    txt=txt.replace('\n',"&#10")
    return txt
register.filter("santa_clara_raw",santa_clara_raw)
santa_clara_raw.needs_autoescape = True

def santa_clara_lang(value,ind=0,autoescape=None): 
    return(language_register.extended.filter(value,ind,autoescape))
register.filter("santa_clara_lang",santa_clara_lang)
santa_clara_lang.needs_autoescape = True

def santa_clara_toc(value,ind=0,autoescape=None): 
    sclang_toc=language_register.extended.get_toc_companion()
    return(sclang_toc.filter(value,ind,autoescape))
register.filter("santa_clara_toc",santa_clara_toc)
santa_clara_toc.needs_autoescape = True

def santa_clara_simple(value,ind=0,autoescape=None): 
    return(language_register.simple.filter(value,ind,autoescape))
register.filter("santa_clara_simple",santa_clara_simple)
santa_clara_simple.needs_autoescape = True

def santa_clara_json(value,ind=0,autoescape=None): 
    txt=language_register.extended.filter(value,ind,lambda x: x)
    txt=esc(txt).replace('"',"'")
    txt=txt.replace('\n',"<br/>")
    txt=txt.replace('\\',r"&#92")
    return txt
register.filter("santa_clara_json",santa_clara_json)
santa_clara_json.needs_autoescape = True

def santa_clara_pdf(txt): 
    ret=language_register.extended.filter_pdf(txt)
    if type(ret) not in [ str,unicode ]:
        return(ret)
    return( [ ("Normal", ret) ] )

