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
        if self.attrs.has_key("style") and self.attrs["style"]:
            H+=' class="santa-clara-editor '+self.attrs["style"]+'"'
        else:
            H+=' class="santa-clara-editor"'
        H+=' data-ta_id="'+ta_id+'"'
        H+=' data-ta_name="'+name+'"'
        H+=u'>'
        H+=unicode(value)
        H+='</div>\n'
        H+="\n"
        
        return mark_safe(H)
    

# Valore che esiste:
#
# <label class="required" for="id_santaclara_base-version-content_type-object_id-0-text">LABEL:</label>
# <textarea class="vLargeTextField" cols="40" id="id_santaclara_base-version-content_type-object_id-0-text" 
#    name="santaclara_base-version-content_type-object_id-0-text" rows="10">
# TESTO</textarea>



# Valore nuovo (quando ne esiste uno):
#
# <label class="required" for="id_santaclara_base-version-content_type-object_id-1-text">Text:</label>
# <textarea class="vLargeTextField" cols="40" id="id_santaclara_base-version-content_type-object_id-1-text" 
#    name="santaclara_base-version-content_type-object_id-1-text" rows="10"></textarea>

# Valore nuovo (quando non ne esiste uno):
#                
# <label class="required" for="id_santaclara_base-version-content_type-object_id-0-text">Text:</label>
# <textarea class="vLargeTextField" cols="40" id="id_santaclara_base-version-content_type-object_id-0-text" 
#     name="santaclara_base-version-content_type-object_id-0-text" rows="10"></textarea>

class SantaClaraTextEditorButton(object):
    def __init__(self,hclass,tag,tooltip,rendering):
        self.tag=tag
        self.rendering=rendering
        self.tooltip=tooltip
        self.hclass="santa_clara_text_editor_button_"+hclass
        pass

    def __unicode__(self):
        html=u'<a href="" class="'+self.hclass+'" data-tag="'+self.tag+'">'
        html+=u'  '+self.rendering+'<span class="tooltip">'+self.tooltip+'</span></a>'
        return html

class SantaClaraTextEditorButtonFontAwesome(SantaClaraTextEditorButton):
    def __init__(self,hclass,tag,tooltip,icon):
        self.tag=tag
        self.rendering='<i class="editor-button fa fa-'+icon+'"></i>'
        self.tooltip=tooltip
        self.hclass="santa_clara_text_editor_button_"+hclass

class SantaClaraTextEditorButtonHtmlTag(SantaClaraTextEditorButton):
    def __init__(self,hclass,tag,tooltip,html_tag,label):
        self.tag=tag
        self.rendering='<'+html_tag+'>'
        self.rendering+='<span class="editor-button" style="padding-left:.2em;padding-right:.2em;">'
        self.rendering+=label
        self.rendering+='</span></'+html_tag+'>'
        self.tooltip=tooltip
        self.hclass="santa_clara_text_editor_button_"+hclass

class SantaClaraTextEditorButtonSpanClass(SantaClaraTextEditorButton):
    def __init__(self,hclass,tag,tooltip,span_class,label):
        self.tag=tag
        self.rendering+='<span class="editor-button '+span_class+'" style="padding-left:.2em;padding-right:.2em;">'
        self.rendering+=label
        self.rendering+='</span>'
        self.tooltip=tooltip
        self.hclass="santa_clara_text_editor_button_"+hclass


class SantaClaraAceWidget(forms.Textarea):
    class Media:
        css = {
            "all": ('css/font-awesome.min.css',
                    'css/jquery-ui-1.10.4.custom.min.css',
                    'santaclara_editor/css/ace.css',)
            }
        js = ('js/jquery.js',
              'js/jquery-ui-1.10.4.custom.min.js',
              'js/ace/ace.js',
              'santaclara_editor/js/ace_widget.js'
              )


    def render(self, name, value, attrs=None):
        BUTTONS=[ SantaClaraTextEditorButtonFontAwesome("simple","left",'align left','align-left'),
                  SantaClaraTextEditorButtonFontAwesome("simple","center",'align center','align-center'),
                  SantaClaraTextEditorButtonFontAwesome("simple","right",'align right','align-right'),
                  SantaClaraTextEditorButtonFontAwesome("simple","justify",'align justify','align-justify'),
                  u'<span class="hspace" style="padding-left:1em;"></span>',
                  SantaClaraTextEditorButtonFontAwesome("single","hspace",'add horizontal space','arrows-h'),
                  SantaClaraTextEditorButtonFontAwesome("single","vspace",'add vertical space','arrows-v'),
                  u'<span class="hspace" style="padding-left:1em;"></span>',
                  SantaClaraTextEditorButtonHtmlTag("simple","b",'bold','b','B'),
                  SantaClaraTextEditorButtonHtmlTag("simple","i",'italic','i','I'),
                  SantaClaraTextEditorButtonSpanClass("simple","s",'linethrough','linethrough','S'),
                  SantaClaraTextEditorButtonSpanClass("simple","u",'underline','underline','U'),
                  SantaClaraTextEditorButtonSpanClass("simple","o",'overline','overline','O'),
                  SantaClaraTextEditorButtonHtmlTag("simple","t",'terminal type','tt','T'),
                  SantaClaraTextEditorButtonSpanClass("simple","sc",'smallcaps','smallcaps','SC'),
                  SantaClaraTextEditorButton("function","action_bracket",'add bracket','[]'),
                  u'<span class="hspace" style="padding-left:1em;"></span>',
                  SantaClaraTextEditorButtonFontAwesome("simple","code",'code','file'),
                  SantaClaraTextEditorButtonFontAwesome("simple","term",'terminal','desktop'),
                  SantaClaraTextEditorButtonFontAwesome("simple","quote",'quote','quote-right'),
                  SantaClaraTextEditorButtonFontAwesome("simple","reading",'reading text (mail, paper, ecc.)','newspaper-o'),
                  u'<span class="hspace" style="padding-left:1em;"></span>',
                  SantaClaraTextEditorButton("function","action_upper",'upper case',u'a⇾A'),
                  SantaClaraTextEditorButton("function","action_lower",'lower case',u'A⇾a') ]
        
        #html = super(SantaClaraAceWidget, self).render(name, value, attrs=attrs)
        ta_id=attrs["id"]

        print "ta_id:",ta_id
        print "name:",name
        print "value:",value
        print "attrs:",attrs

        if not value: value=""

        html=u'<div id="santa_clara_text_editor_box_'+ta_id+'" class="santa_clara_text_editor_box"'
        html+=u'   data-ta_id="'+ta_id+'"'
        html+=u'   data-ta_name="'+name+'">'
        html+=u'   <div id="santa_clara_text_editor_button_bar_'+ta_id+'" class="santa_clara_text_editor_button_bar"'
        html+=u'       data-santa_clara_text_editor_box_id="santa_clara_text_editor_box_'+ta_id+'"'
        html+=u'       data-santa_clara_text_editor_id="santa_clara_text_editor_'+ta_id+'">'
        for button in BUTTONS:
            html+=unicode(button)
        html+=u'   </div><!-- text_editor_button_bar -->'

        html+=u'<div id="santa_clara_text_editor_'+ta_id+'" class="santa_clara_text_editor"'
        html+=u'   data-ta_id="'+ta_id+'"'
        html+=u'   data-ta_name="'+name+'">'
        html+=unicode(value)
        html+=u'</div>'

        html+=u'</div><!-- text_editor_box -->'
        
        return mark_safe(html)






    # def render(self, name, value, attrs=None):
    #     html = super(SantaClaraAceWidget, self).render(name, value, attrs=attrs)
    #     ta_id=attrs["id"]

    #     print "ta_id:",ta_id
    #     print "name:",name
    #     print "value:",value
    #     print "attrs:",attrs

    #     if not value: value=""

    #     html=u'<div id="santa_clara_text_editor_box_'+ta_id+'" class="santa_clara_text_editor_box"'
    #     html+=u' data-ta_id="'+ta_id+'"'
    #     html+=u' data-ta_name="'+name+'">'
    #     html+=u'<div id="santa_clara_text_editor_button_bar_'+ta_id+'" class="santa_clara_text_editor_button_bar"'
    #     html+=u' data-santa_clara_text_editor_box_id="santa_clara_text_editor_box_'+ta_id+'"'
    #     html+=u' data-santa_clara_text_editor_id="santa_clara_text_editor_'+ta_id+'">'

    #     for tag in [ "left","center","right","justify" ]:
    #         html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="'+tag+'">'
    #         html+=u'  <i class="editor-button fa fa-align-'+tag+'"></i><span class="tooltip">align '+tag+'</span></a>'

    #     html+=u'<span class="hspace" style="padding-left:1em;"></span>'

    #     html+=u'<a href="" class="santa_clara_text_editor_button_single" data-tag="hspace">'
    #     html+=u'  <i class="editor-button fa fa-arrows-h"></i><span class="tooltip">add horizontal space</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_single" data-tag="vspace">'
    #     html+=u'  <i class="editor-button fa fa-arrows-v"></i><span class="tooltip">add vertical space</span></a>'

    #     html+=u'<span class="hspace" style="padding-left:1em;"></span>'

    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="b">'
    #     html+=u'  <b><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">B</span></b>'
    #     html+=u'  <span class="tooltip">bold</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="i">'
    #     html+=u'  <i><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">I</span></i>'
    #     html+=u'  <span class="tooltip">italic</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="s">'
    #     html+=u'  <span class="editor-button linethrough" style="padding-left:.2em;padding-right:.2em;">S</span>'
    #     html+=u'  <span class="tooltip">linethrough</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="u">'
    #     html+=u'  <span class="editor-button underline" style="padding-left:.2em;padding-right:.2em;">U</span>'
    #     html+=u'  <span class="tooltip">underline</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="o">'
    #     html+=u'  <span class="editor-button overline" style="padding-left:.2em;padding-right:.2em;">O</span>'
    #     html+=u'  <span class="tooltip">overline</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="t">'
    #     html+=u'  <tt><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">T</span></tt>'
    #     html+=u'  <span class="tooltip">terminal type</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="sc">'
    #     html+=u'  <span class="editor-button smallcaps" style="padding-left:.2em;padding-right:.2em;">SC</span>'
    #     html+=u'  <span class="tooltip">smallcaps</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_function" data-tag="action_bracket">'
    #     html+=u'  []<span class="tooltip">add bracket</span></a>'
        
    #     html+=u'<span class="hspace" style="padding-left:1em;"></span>'
        
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="code">'
    #     html+=u'  <i class="editor-button fa fa-file"></i><span class="tooltip">code</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="term">'
    #     html+=u'  <i class="editor-button fa fa-desktop"></i><span class="tooltip">terminal</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="quote">'
    #     html+=u'  <i class="editor-button fa fa-quote-right"></i><span class="tooltip">quote</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_simple" data-tag="reading">'
    #     html+=u'  <i class="editor-button fa fa-newspaper-o"></i><span class="tooltip">reading text (mail, paper, ecc.)</span></a>'
        
    #     html+=u'<span class="hspace" style="padding-left:1em;"></span>'
        
    #     html+=u'<a href="" class="santa_clara_text_editor_button_function" data-tag="action_upper">'
    #     html+=u'  a⇾A<span class="tooltip">upper case</span></a>'
    #     html+=u'<a href="" class="santa_clara_text_editor_button_function" data-tag="action_lower">'
    #     html+=u'  A⇾a<span class="tooltip">lower case</span></a>'
    #     html+=u'</div><!-- text_editor_button_bar -->'

    #     html+=u'<div id="santa_clara_text_editor_'+ta_id+'" class="santa_clara_text_editor"'
    #     html+=u' data-ta_id="'+ta_id+'"'
    #     html+=u' data-ta_name="'+name+'">'
    #     html+=unicode(value)
    #     html+=u'</div>'

    #     html+=u'</div><!-- text_editor_box -->'
        
    #     return mark_safe(html)
