from django.conf import settings

from santaclara_editor.santaclara_lang import tags
from santaclara_editor.santaclara_lang import tables
from santaclara_editor.santaclara_lang import factories
from santaclara_editor.santaclara_lang.parsers import SantaClaraLang

class LanguageRegister(object):
    def __init__(self):
        simple_tags={ "b": factories.mk_format_tag("b"),
                      "i": factories.mk_format_tag("i"),
                      "t": factories.mk_format_tag("tt"),
                      "u": factories.mk_span_tag("underline"),
                      "s": factories.mk_span_tag("linethrough"),
                      "o": factories.mk_span_tag("overline"),
                      "sc": factories.mk_span_tag("smallcaps"),
                      "center": factories.mk_align_tag("center"),
                      "left": factories.mk_align_tag("left"),
                      "right": factories.mk_align_tag("right"),
                      "justify": factories.mk_align_tag("justify"),
                      "quote": factories.mk_class_tag(tags.QuoteTag),
                      "cite": factories.mk_class_tag(tags.CiteTag),
                      "code": factories.mk_pre_tag("code"),
                      "term": factories.mk_pre_tag("terminal") }

        extended_tags=dict(simple_tags.items() + { "hr": factories.mk_single_tag("hr"),
                                                   "br": factories.mk_class_tag(tags.LineBreakTag),
                                                   "space": factories.mk_class_tag(tags.SpaceTag),
                                                   "hspace": factories.mk_class_tag(tags.SpaceTag),
                                                   "vspace": factories.mk_class_tag(tags.SpaceTag),
                                                   "ref": factories.mk_class_tag(tags.RefTag),
                                                   "url": factories.mk_class_tag(tags.UrlTag),
                                                   "color": factories.mk_class_tag(tags.ColorTag),
                                                   "li": factories.mk_item_tag("li"),
                                                   "dt": factories.mk_item_tag("dt"),
                                                   "dd": factories.mk_item_tag("dd"),
                                                   "item": factories.mk_list_tag("ul"),
                                                   "enum": factories.mk_list_tag("ol"),
                                                   "dict": factories.mk_list_tag("dl"),
                                                   "table": factories.mk_class_tag(tables.TableTag),
                                                   }.items())

        self.simple=SantaClaraLang(simple_tags)
        self.extended=SantaClaraLang(extended_tags)

    def add_tag(self,tag,tagobject):
        self.extended.add_tag(tag,tagobject)
        
    def add_tag_simple(self,tag,tagobject):
        self.simple.add_tag(tag,tagobject)
        self.extended.add_tag(tag,tagobject)

    def __str__(self):
        S="simple: "+", ".join(self.simple.tags.keys())
        S+="\nextended: "+", ".join(self.extended.tags.keys())
        return S

language_register=LanguageRegister()


