# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

class SCButtons(dict):
    def __init__(self):
        dict.__init__(self)
        for (tag,i) in [ (u"left",u"align-left"), (u"center",u"align-center"),
                         (u"right",u"align-right"), (u"justify",u"align-justify"),
                         (u"vspace",u"resize-vertical"),(u"hspace",u"resize-horizontal") ]:
            txt=u'<i class="editor-button fa fa-'+i+u'"></i>'
            t=i.split("-")
            if t[0]=="align":
                if t[1]!="justify":
                    self[tag]=(txt,u" ".join(t))
                else:
                    self[tag]=(txt,u"justify")
                continue
            self[tag]=(txt,u"add "+t[1]+u" space")

        for (tag,i) in [ (u"b",u"bold"), (u"i",u"italic"), (u"t",u"terminal type")]:
            htag=tag
            if tag=="t": htag="tt"
            txt=u'<'+htag+u'><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">'
            txt+=tag.upper()+u'</span></'+htag+u'>'
            self[tag]=(txt,i)

        for (tag,i) in [ (u"s",u"linethrough"), (u"u",u"underline"),
                         (u"o",u"overline"), (u"sc",u"smallcaps") ]:
            txt=u'<span class="editor-button '+i+u'" style="padding-left:.2em;padding-right:.2em;">'+tag.upper()+u'</span>'
            self[tag]=(txt,i)
            pass
        
        self[u"code"]=(u'<i class="editor-button fa fa-file"></i>',u"code")
        self[u"term"]=(u'<i class="editor-button fa fa-desktop"></i>',u"terminal")
        self[u"quote"]=(u'<i class="editor-button fa fa-quote-right"></i>',u"quote")

        self[u"action_upper"]=(u'a⇾A',u"upper case")
        self[u"action_lower"]=(u'A⇾a',u"lower case")

    def get_buttons(self,blist):
        buttons=[]
        for b in blist:
            buttons.append( (b,self[b][0],self[b][1]) )
        return buttons

SANTA_CLARA_BUTTONS=SCButtons()        

class SantaClaraSimpleWidget(forms.Textarea):
    class Media:
        css = {
            "all": ('css/font-awesome.min.css',
                    'css/jquery-ui-1.10.4.custom.min.css',
                    'css/santa-clara-tags.css',)
            }
        js = ('js/jquery.js',
              'js/jquery-ui-1.10.4.custom.min.js',
              'js/jquery-santaclara.js',
              'js/santa-clara-widget.js')

    def render(self, name, value, attrs=None):
        ### Aggiungere tooltip
        html = super(SantaClaraSimpleWidget, self).render(name, value, attrs=attrs)

        align_buttons=SANTA_CLARA_BUTTONS.get_buttons([u"left",u"center",u"right",u"justify"])
        space_buttons=SANTA_CLARA_BUTTONS.get_buttons([u"vspace",u"hspace"])
        format_buttons=SANTA_CLARA_BUTTONS.get_buttons([u"b",u"i",u"s",u"u",u"o",u"t",u"sc"])
        div_buttons=SANTA_CLARA_BUTTONS.get_buttons([u"code",u"term",u"quote" ])
        action_buttons=SANTA_CLARA_BUTTONS.get_buttons([u"action_upper",u"action_lower" ])

        T=[]
        for buttons in [ align_buttons, space_buttons, action_buttons, format_buttons, div_buttons ]:
            t=""
            for (tag,txt,tooltip) in buttons:
                #t+=u'<a href="" name="'+tag+u'">'+txt+u'<span class="tooltip">'+tooltip+u'</span></a>'
                t+=u'<a href="" name="'+tag+u'">'+txt+u'</a>'
            T.append(t)

        sep=u' <span class="hspace" style="padding-left:.5em;"></span>'
        S=u'<div class="editor"><div class="toolbar">'
        S+=sep.join(T)
        S+=u"</div>"
        return mark_safe(S+html+"</div>")

class SantaClaraJQueryUIWidget(forms.Textarea):
    class Media:
        css = {
            "all": ('css/font-awesome.min.css',
                    'css/jquery-ui-1.10.4.custom.min.css',
                    'css/santa-clara-tags.css',)
            }
        js = ('js/jquery-1.11.0.js',
              'js/jquery-ui-1.11.0.custom.min.js',
              'js/jquery-santaclara.js',
              'santaclara_editor/js/santa-clara-editor.js',
              'js/santa-clara-widget.js')

    def render(self, name, value, attrs=None):
        ta_id=attrs["id"]

        html = super(SantaClaraJQueryUIWidget, self).render(name, value, attrs=attrs)

        H=u'<div id="santa_clara_'+ta_id+'"'
        if self.attrs["style"]:
            H+=' class="santa-clara-editor '+self.attrs["style"]+'"'
        else:
            H+=' class="santa-clara-editor"'
        H+=' data-ta_name="'+name+'"'
        H+=' data-ta_id="'+ta_id+'"'
        H+=u'>'
        H+=unicode(value)
        H+='</div>\n'
        #H+='<script type="text/javascript">\n'
        #H+='set_santaclara_editor();\n'
        #H+='</script>'
        H+="\n"
        
        return mark_safe(H)
    
