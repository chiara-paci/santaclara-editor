import re

from django.utils.html import conditional_escape

class Tag(object):
    def __init__(self,lang,padre,inline=True):
        self.lang=lang
        self.inline=inline
        self.break_to_par=False
        self.padre=padre
        self.level=0
        self.format={}
        self.format["html"]=self.output
        self.format["pdf"]=self.pdf
        if self.padre:
            self.padre.add(self)
        self.elenco=[]
        self.args={}
        self.re_newline=re.compile(r'[ \r\n]+')

    def reparent(self,padre):
        self.padre=padre
        self.padre.add(self)

    def set_args(self,args):
        n=0
        for arg in args:
            self.args[n]=arg
            n+=1
            t=arg.split("=")
            if len(t)==1: continue
            self.args[t[0]]='='.join(t[1:])

    def close_last_par(self):
        if not self.break_to_par: return
        if not self.elenco: return
        if not ((type(self.elenco[-1]) in [str,unicode]) or (self.elenco[-1].inline)): return
        temp=[]
        while self.elenco and (type(self.elenco[-1]) in [str,unicode] or self.elenco[-1].inline):
            temp.append(self.elenco.pop(-1))
        temp.reverse()
        p=ParagraphTag(self.lang,self)
        for obj in temp:
            if type(obj) in [str,unicode]:
                p.elenco.append(obj)
                continue
            obj.reparent(p)

    def insert(self,pos,obj):
        self.elenco.insert(pos,obj)
        obj.padre=self

    def add(self,obj):
        ##### Aggiungere qualcosa che elimini gli spazi doppi
        if type(obj) == LineBreakTag:
            if not self.elenco: return
            if not ((type(self.elenco[-1]) in [str,unicode]) or (self.elenco[-1].inline)): return
            if not self.break_to_par:
                self.elenco.append(obj)
                return
            temp=[]
            while self.elenco and (type(self.elenco[-1]) in [str,unicode] or self.elenco[-1].inline):
                temp.append(self.elenco.pop(-1))
            temp.reverse()
            p=ParagraphTag(self.lang,self)
            for obj in temp:
                if type(obj) in [str,unicode]:
                    p.elenco.append(obj)
                    continue
                obj.reparent(p)
            #self.elenco.append(obj)
            return
        if type(obj) not in [str,unicode]:
            if obj.inline:
                self.elenco.append(obj)
                return
            self.close_last_par()
            if not self.elenco:
                self.elenco.append(obj)
                return
            if type(self.elenco[-1]) == LineBreakTag:
                self.elenco.remove(self.elenco[-1])
            self.elenco.append(obj)
            return
        self.elenco.append(obj)

    def output(self,autoescape,outtype="html"):
        if autoescape:
            esc = conditional_escape
        else:
            esc = lambda x: x
        S=u""
        for e in self.elenco:
            if type(e) in [ str,unicode ]:
                S+=esc(e)
                continue
            S+=e.format[outtype](autoescape)
        S=S.strip()
        return(S)

    def pdf(self,autoescape,outtype="pdf"):
        if autoescape:
            esc = conditional_escape
        else:
            esc = lambda x: x
        ret=[]
        S=u""
        for e in self.elenco:
            if type(e) in [ str,unicode ]:
                S+=esc(e)
                continue
            r=e.format[outtype](autoescape)
            if type(r) in [ str,unicode ]:
                S+=esc(r)
                continue
            ret.append( ("Normal",S) )
            S=u""
            ret+=r
        if S: ret.append( ("Normal",S) )
        if len(ret)==1 and ret[0][0]=="Normal":
            return(ret[0][1])
        return(ret)

class FormatTag(Tag):
    def __init__(self,lang,padre,tid,inline=True):
        Tag.__init__(self,lang,padre,inline=inline)
        self.tid=tid

    def output(self,autoescape,outtype="html"):
        S="<"+self.tid+">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</"+self.tid+">"
        return(S)

    def pdf(self,autoescape,outtype="pdf"):
        S="<"+self.tid+">"
        S+=Tag.pdf(self,autoescape,outtype)
        S+="</"+self.tid+">"
        return(S)

class ParagraphTag(FormatTag):
    def __init__(self,lang,padre):
        FormatTag.__init__(self,lang,padre,"p",inline=False)

class HTag(FormatTag):
    def __init__(self,lang,padre,tid,the):
        FormatTag.__init__(self,lang,padre,tid,inline=False)
        self.the=the

    def output(self,autoescape,outtype="html"):
        S=""
        S+="<"+self.tid+">"
        S+='<a class="anchor" name="section-h'+self.the.replace(" ","_")+'"></a>'
        S+=self.the+". "
        S+=Tag.output(self,autoescape,outtype)
        S+="</"+self.tid+">"
        return(S)

class HLinkTag(FormatTag):
    def __init__(self,lang,padre,tid,the):
        FormatTag.__init__(self,lang,padre,"p",inline=False)
        self.the=the
        self.style="toc-"+tid

    def output(self,autoescape,outtype="html"):
        S=""
        S+="<"+self.tid+' class="'+self.style+'">'
        S+='<a href="#section-h'+self.the.replace(" ","_")+'">'
        S+=self.the+". "
        S+=Tag.output(self,autoescape,outtype)
        S+="</a>"
        S+="</"+self.tid+">"
        return(S)

class ListTag(FormatTag):
    def __init__(self,lang,padre,tid):
        FormatTag.__init__(self,lang,padre,tid,inline=False)
        self.level=self.padre.level+1

    def pdf(self,autoescape,outtype="pdf"):
        S=[]
        if self.tid=="ol":
            S.append(('Normal','<seqreset id="enum'+str(self.level)+'"/>'))
        S+=Tag.pdf(self,autoescape,outtype)
        return(S)

class ItemTag(FormatTag):
    def __init__(self,lang,padre,tid):
        FormatTag.__init__(self,lang,padre,tid,inline=False)
        self.level=self.padre.level

    def pdf(self,autoescape,outtype="pdf"):
        if autoescape:
            esc = conditional_escape
        else:
            esc = lambda x: x
        S=u""
        if self.tid=="li":
            if self.padre.tid=="ol":
                S+='<seq id="enum'+str(self.level)+'"/>'
                style="enum"
            else:
                style="item"
        elif self.tid=="dd":
            style="dictdef"
        else:
            print self.tid
            style="dicttag"
        ret=[]
        for e in self.elenco:
            if type(e) in [ str,unicode ]:
                S+=esc(e)
                continue
            r=e.format[outtype](autoescape)
            if type(r) in [ str,unicode ]:
                S+=esc(r)
                continue
            ret.append( (style+str(self.level),S) )
            S=u""
            ret+=r
        if S: ret.append( (style+str(self.level),S) )
        return(ret)

class RefTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre)

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("ref"):
            if len(self.args)>=1:
                self.args["ref"]=self.args[0]
            else:
                self.args["ref"]=""

    def output(self,autoescape,outtype="html"):
        S='<a href="#'+self.args["ref"]+'">'
        S+=Tag.output(self,autoescape,outtype)
        S+="</a>"
        return(S)

class UrlTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre)

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("url"):
            if len(self.args)>=1:
                self.args["url"]=self.args[0]
            else:
                self.args["url"]=""

    def output(self,autoescape,outtype="html"):
        S='<a href="'+self.args["url"]+'">'
        S+=Tag.output(self,autoescape,outtype)
        S+="</a>"
        return(S)


class ColorTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre)

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("fore"):
            self.args["fore"]=""
        if not self.args.has_key("back"):
            self.args["back"]=""

    def output(self,autoescape,outtype="html"):
        S="<span style=\"color:"+self.args["fore"]+";background-color:"+self.args["back"]+";\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</span>"
        return(S)


class DivTag(Tag):
    def __init__(self,lang,padre,style,break_to_par=True):
        Tag.__init__(self,lang,padre,inline=False)
        self.style=style
        self.break_to_par=break_to_par

    def output(self,autoescape,outtype="html"):
        S="<div class=\""+self.style+"\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</div>"
        return(S)

class AlignTag(Tag):
    def __init__(self,lang,padre,style,break_to_par=True):
        Tag.__init__(self,lang,padre,inline=False)
        self.style=style
        self.break_to_par=break_to_par

    def output(self,autoescape,outtype="html"):
        S="<div class=\""+self.style+"\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</div>"
        return(S)

class QuoteTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre,inline=False)
        self.break_to_par=True

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("name"):
            if len(self.args)>=1:
                self.args["name"]=self.args[0]
            else:
                self.args["name"]=""
        if not self.args.has_key("name_url"):
            self.args["name_url"]=""
        if not self.args.has_key("url"):
            self.args["url"]=""
        if not self.args.has_key("ts"):
            self.args["ts"]=""

    def output(self,autoescape,outtype="html"):
        S="<div class=\"quotediv\">"
        S+="<div class=\"quoteheader\">"
        S+="quote: "
        if self.args["name"]:
            if self.args["name_url"]:
                S+=" <a href=\""+str(self.args["name_url"])+"\">"
                S+=self.args["name"]
                S+="<span class=\"tooltip\">View author info</span></a>"
            else:
                S+=" "+self.args["name"]
        if self.args["ts"]:
            S+=" "+self.args["ts"]
        if self.args["url"]:
            S+=" <a href=\""+self.args["url"]+"\"><i class=\"icon-circle-arrow-right\"></i>"
            S+="<span class=\"tooltip\">View original text</span></a>"
        S+="</div>"
        S+="<div class=\"quotetext\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</div>"
        S+="</div>"
        return(S)

class CiteTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre,inline=False)
        self.break_to_par=True

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("ref"):
            self.args["ref"]=""

        if self.args.has_key("page"):
            self.args["page"]="p. "+self.args["page"]
        else:
            self.args["page"]=""

        if not self.args.has_key("url"):
            if self.args["ref"]:
                self.args["url"]="#ref"+self.args["ref"].lower().replace(" ","").replace(",","")
            else:
                self.args["url"]=""

        if not self.args.has_key("label"):
            if self.args["ref"]:
                self.args["label"]="["+self.args["ref"]+"]"

        if self.args.has_key("label"):
            self.args["label"]=self.args["label"]
            if self.args["page"]:
                self.args["label"]+=", "+self.args["page"]
        else:
            if self.args["page"]:
                self.args["label"]="["+self.args["page"]+"]"
            elif self.args["url"]:
                self.args["label"]="<i class=\"icon-circle-arrow-right\"></i>"
            else:
                self.args["label"]=""

        self.args["show_reference"]=False
        for k in ["ref","url","label","page"]:
            if self.args[k]:
                self.args["show_reference"]=True
                return

    def output(self,autoescape,outtype="html"):
        S="<div class=\"citediv\">"
        S+="<div class=\"citetext\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</div>"

        if not self.args["show_reference"]:
            S+="</div>"
            return(S)
            
        S+="<div class=\"citefooter\">"
        if self.args["url"]:
            S+=" <a href=\""+self.args["url"]+"\">"
        S+=self.args["label"]
        if self.args["url"]:
            S+="<span class=\"tooltip\">View original text</span></a>"
        S+="</div>"

        S+="</div>"
        return(S)


class SpanTag(Tag):
    def __init__(self,lang,padre,style):
        Tag.__init__(self,lang,padre)
        self.style=style

    def output(self,autoescape,outtype="html"):
        S="<span class=\""+self.style+"\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</span>"
        return(S)

class PreTag(Tag):
    def __init__(self,lang,padre,style):
        Tag.__init__(self,lang,padre,inline=False)
        self.style=style

    def output(self,autoescape,outtype="html"):
        S="<pre class=\""+self.style+"\">"
        S+=Tag.output(self,autoescape,outtype)
        S+="</pre>"
        return(S)

class SingleTag(Tag):
    def __init__(self,lang,padre,tid):
        Tag.__init__(self,lang,padre,inline=False)
        self.tid=tid

    def output(self,autoescape,outtype="html"):
        S="<"+self.tid+"/>"
        return(S)

class LineBreakTag(SingleTag):
    def __init__(self,lang,padre):
        SingleTag.__init__(self,lang,padre,"br")

    def pdf(self,autoescape,outtype="pdf"):
        return([])
        
class SpaceTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre)

    def output(self,autoescape,outtype="html"):
        S="&nbsp;"
        return(S)

class VSpaceTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre,inline=False)

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("h"):
            if len(self.args)>=1:
                self.args["h"]=self.args[0]
            else:
                self.args["h"]="1em"

    def output(self,autoescape,outtype="html"):
        S='<p class="vspace" style="height:'+self.args["h"]+';">&nbsp;</p>'
        return(S)

class HSpaceTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre)

    def set_args(self,args):
        Tag.set_args(self,args)
        if not self.args.has_key("w"):
            if len(self.args)>=1:
                self.args["w"]=self.args[0]
            else:
                self.args["w"]="1em"

    def output(self,autoescape,outtype="html"):
        S='<span class="hspace" style="padding-left:'+self.args["w"]+';"></span>'
        return(S)

