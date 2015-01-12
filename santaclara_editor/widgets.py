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


    # <div id="santa_clara_text_editor_box_{{ scene.id }}" class="santa_clara_text_editor_box">
    #   <!-- editor button bar -->
    #   <div id="santa_clara_text_editor_button_bar_{{ scene.id }}" class="santa_clara_text_editor_button_bar"
    #        data-santa_clara_text_editor_box_id="santa_clara_text_editor_box_{{ scene.id }}"
    #        data-santa_clara_text_editor_id="santa_clara_text_editor_{{ scene.id }}">

    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="left">
    #       <i class="editor-button fa fa-align-left"></i><span class="tooltip">align left</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="center">
    #       <i class="editor-button fa fa-align-center"></i><span class="tooltip">align center</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="right">
    #       <i class="editor-button fa fa-align-right"></i><span class="tooltip">align right</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="justify">
    #       <i class="editor-button fa fa-align-justify"></i><span class="tooltip">justify</span></a>

    #     <span class="hspace" style="padding-left:1em;"></span>

    #     <a href="" class="santa_clara_text_editor_button_single" data-tag="hspace">
    #       <i class="editor-button fa fa-arrows-h"></i><span class="tooltip">add horizontal space</span></a>
    #     <a href="" class="santa_clara_text_editor_button_single" data-tag="vspace">
    #       <i class="editor-button fa fa-arrows-v"></i><span class="tooltip">add vertical space</span></a>

    #     <span class="hspace" style="padding-left:1em;"></span>

    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="b">
    #       <b><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">B</span></b><span class="tooltip">bold</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="i">
    #       <i><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">I</span></i><span class="tooltip">italic</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="s">
    #       <span class="editor-button linethrough" style="padding-left:.2em;padding-right:.2em;">S</span>
    #       <span class="tooltip">linethrough</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="u">
    #       <span class="editor-button underline" style="padding-left:.2em;padding-right:.2em;">U</span><span class="tooltip">underline</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="o">
    #       <span class="editor-button overline" style="padding-left:.2em;padding-right:.2em;">O</span><span class="tooltip">overline</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="t">
    #       <tt><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">T</span></tt>
    #       <span class="tooltip">terminal type</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="sc">
    #       <span class="editor-button smallcaps" style="padding-left:.2em;padding-right:.2em;">SC</span><span class="tooltip">smallcaps</span></a>

    #     <span class="hspace" style="padding-left:1em;"></span>

    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="code">
    #       <i class="editor-button fa fa-file"></i><span class="tooltip">code</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="term">
    #       <i class="editor-button fa fa-desktop"></i><span class="tooltip">terminal</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="quote">
    #       <i class="editor-button fa fa-quote-right"></i><span class="tooltip">quote</span></a>
    #     <a href="" class="santa_clara_text_editor_button_simple" data-tag="reading">
    #       <i class="editor-button fa fa-newspaper-o"></i><span class="tooltip">reading text (mail, paper, ecc.)</span></a>

    #     <span class="hspace" style="padding-left:1em;"></span>

    #     <a href="" class="santa_clara_text_editor_button_function" data-tag="action_upper">
    #       a⇾A<span class="tooltip">upper case</span></a>
    #     <a href="" class="santa_clara_text_editor_button_function" data-tag="action_lower">
    #       A⇾a<span class="tooltip">lower case</span></a>

    #   </div><!-- editor button bar -->

    #   <div id="santa_clara_text_editor_{{ scene.id }}" class="santa_clara_text_editor">{{ scene.text }}</div>

    # </div><!-- editor box -->



    def render(self, name, value, attrs=None):
        ta_id=attrs["id"]

        html='<div id="santa_clara_text_editor_box_'+ta_id+'" class="santa_clara_text_editor_box"'
        html+=' data-ta_id="'+ta_id+'"'
        html+=' data-name="'+name+'">'
        html+='<div id="santa_clara_text_editor_button_bar_'+ta_id+'" class="santa_clara_text_editor_button_bar"'
        html+=' data-santa_clara_text_editor_box_id="santa_clara_text_editor_box_'+ta_id+'"'
        html+=' data-santa_clara_text_editor_id="santa_clara_text_editor_'+ta_id+'">'

        for tag in [ "left","center","right","justify" ]:
            html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="'+tag+'">'
            html+='  <i class="editor-button fa fa-align-'+tag+'"></i><span class="tooltip">align '+tag+'</span></a>'

        html+='<span class="hspace" style="padding-left:1em;"></span>'

        html+='<a href="" class="santa_clara_text_editor_button_single" data-tag="hspace">'
        html+='  <i class="editor-button fa fa-arrows-h"></i><span class="tooltip">add horizontal space</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_single" data-tag="vspace">'
        html+='  <i class="editor-button fa fa-arrows-v"></i><span class="tooltip">add vertical space</span></a>'

        html+='<span class="hspace" style="padding-left:1em;"></span>'

        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="b">'
        html+='  <b><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">B</span></b><span class="tooltip">bold</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="i">'
        html+='  <i><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">I</span></i><span class="tooltip">italic</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="s">'
        html+='  <span class="editor-button linethrough" style="padding-left:.2em;padding-right:.2em;">S</span>'
        html+='  <span class="tooltip">linethrough</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="u">'
        html+='  <span class="editor-button underline" style="padding-left:.2em;padding-right:.2em;">U</span><span class="tooltip">underline</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="o">'
        html+='  <span class="editor-button overline" style="padding-left:.2em;padding-right:.2em;">O</span><span class="tooltip">overline</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="t">'
        html+='  <tt><span class="editor-button" style="padding-left:.2em;padding-right:.2em;">T</span></tt>'
        html+='  <span class="tooltip">terminal type</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="sc">'
        html+='  <span class="editor-button smallcaps" style="padding-left:.2em;padding-right:.2em;">SC</span><span class="tooltip">smallcaps</span></a>'
        
        html+='<span class="hspace" style="padding-left:1em;"></span>'
        
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="code">'
        html+='  <i class="editor-button fa fa-file"></i><span class="tooltip">code</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="term">'
        html+='  <i class="editor-button fa fa-desktop"></i><span class="tooltip">terminal</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="quote">'
        html+='  <i class="editor-button fa fa-quote-right"></i><span class="tooltip">quote</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_simple" data-tag="reading">'
        html+='  <i class="editor-button fa fa-newspaper-o"></i><span class="tooltip">reading text (mail, paper, ecc.)</span></a>'
        
        html+='<span class="hspace" style="padding-left:1em;"></span>'
        
        html+='<a href="" class="santa_clara_text_editor_button_function" data-tag="action_upper">'
        html+='  a⇾A<span class="tooltip">upper case</span></a>'
        html+='<a href="" class="santa_clara_text_editor_button_function" data-tag="action_lower">'
        html+='  A⇾a<span class="tooltip">lower case</span></a>'
        html+='</div><!-- text_editor_button_bar -->'

        html+='<div id="santa_clara_text_editor_'+ta_id+'" class="santa_clara_text_editor"'
        html+=' data-ta_id="'+ta_id+'"'
        html+=' data-name="'+name+'">'
        html+=unicode(value)
        html+='</div>'

        html+='</div><!-- text_editor_box -->'
        
        return mark_safe(html)
