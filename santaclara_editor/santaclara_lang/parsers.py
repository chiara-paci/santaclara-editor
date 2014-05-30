from django.utils.safestring import mark_safe

from santaclara_editor.santaclara_lang.factories import *
from santaclara_editor.santaclara_lang.tags import Tag,LineBreakTag,HLinkTag
from santaclara_editor.santaclara_lang.utility import shlex_split

import re

class Base(Tag):
    def __init__(self,lang):
        Tag.__init__(self,lang,None)
        self.padre=self
        self.break_to_par=True

class SantaClaraLang(object):
    def __init__(self,tags,hdeep=6):
        lab=r'[a-zA-Z0-9]+'
        args=r'[^\]\[]*?'
        tag=r'\[.*?\]'
        newline='[ \r\n]+'
        txt=r'[^\r\n\[\]]+'
        regexp=r"((?:\[.*?\])|(?:[\n\r ]+))"
        #regexp=r'('+tag+'|'+txt+'|'+newline+')'
        self.tokenizer=re.compile(regexp)
        self.re_newline=re.compile(r'^ *[\r\n]+$')
        self.ind=0
        self.tags=tags
        self.hdeep=hdeep
        if hdeep>=0:
            htags=[]
            for n in range(0,hdeep):
                htags.append(mk_h_tag(n+1,self))
            for n in range(0,hdeep):
                if n>0:
                    htags[n].prev=htags[n-1]
                if n<hdeep-1:
                    htags[n].next=htags[n+1]
                self.tags["h"+str(n+1)]=htags[n]

    def add_tag(self,tag,obj):
        self.tags[tag]=obj

    def mk_base(self,value,ind=0,internal=False):
        #t=map(lambda x: x[0],self.tokenizer.findall(value))
        for n in range(0,self.hdeep):
            self.tags["h"+str(n+1)].reset()
            
        t=self.tokenizer.split(value)
        if not internal and self.tags.has_key("img"):
            self.tags["img"].reset()
        B=Base(self)
        current=B
        self.ind=ind
        for r in t:
            if self.re_newline.match(r):
                obj=mk_class_tag(LineBreakTag)(self,current)
                continue
            if not r: continue
            if r[0]!='[':
                current.add(r)
                continue
            q=r.replace('[','').replace(']','')
            if not q: continue
            singolo=(q[-1]=="/")
            if singolo: q=q[:-1]
            x=shlex_split(q)
            if "=" in x[0]:
                args=x
                tag=x[0].split("=")[0]
            else:
                tag=x[0]
                args=x[1:]
            if not tag:
                current.add("(no_boh) "+r)
                continue
            if tag[0]=="/":
                tag=tag[1:]
                if not self.tags.has_key(tag):
                    current.add("(no_e) "+r)
                    continue
                current.close_last_par()
                current=current.padre
                continue
            t=tag.split('=')
            if len(t)>1:
                args=t[1:]+args
                tag=t[0]
            if not self.tags.has_key(tag):
                current.add("(no_b) "+r)
                continue
            obj=self.tags[tag](self,current)
            obj.set_args(args)
            if singolo: 
                continue
            current=obj
        current.close_last_par()
        return(B)

    def get_tags(self,value):
        B=self.mk_base(value,internal=True)
        return B.elenco

    def filter(self,value,ind=0,autoescape=None):
        B=self.mk_base(value,ind=ind)
        S=B.format["html"](autoescape)
        return(mark_safe(S))

    def filter_pdf(self,value):
        B=self.mk_base(value)
        S=B.format["pdf"](False)
        return(S)

    def get_toc_companion(self):
        return SantaClaraToc(self.tags,self.hdeep)

class SantaClaraToc(SantaClaraLang):
    def __init__(self,tags,hdeep=6):
        SantaClaraLang.__init__(self,tags,hdeep=hdeep)

    def mk_base(self,value,ind=0,internal=False):
        full_B=SantaClaraLang.mk_base(self,value,ind=0,internal=internal)
        B=Base(self)
        for t in full_B.elenco:
            if type(t)!=HTag: continue
            obj=HLinkTag(self,B,t.tid,t.the)
            for el in t.elenco:
                obj.add(el)
        return(B)
