from django.conf import settings

from santaclara_editor.santaclara_lang.tags import HTag,FormatTag,ListTag,ItemTag,SingleTag,AlignTag,DivTag,SpanTag,PreTag

class mk_h_tag(object):
    def __init__(self,level,parent):
        self.level=level
        self.parent=parent
        self.the=0
        self.prev=None
        self.next=None

    def get_the(self):
        the=""
        if self.prev:
            the+=self.prev.get_the()+"."
        the+=str(self.the)
        return the

    def reset(self): self.the=0

    def __call__(self,lang,padre):
        self.the+=1
        #if self.next: self.next.reset()
        i=self.level+int(self.parent.ind)
        tid="h"+str(i)
        print "F",tid,self.the
        return(HTag(lang,padre,tid,self.get_the()))

class mk_format_tag(object):
    def __init__(self,tid):
        self.tid=tid

    def __call__(self,lang,padre):
        return(FormatTag(lang,padre,self.tid))

class mk_list_tag(object):
    def __init__(self,tid):
        self.tid=tid

    def __call__(self,lang,padre):
        return(ListTag(lang,padre,self.tid))

class mk_item_tag(object):
    def __init__(self,tid):
        self.tid=tid

    def __call__(self,lang,padre):
        return(ItemTag(lang,padre,self.tid))

class mk_class_tag(object):
    def __init__(self,myclass):
        self.myclass=myclass

    def __call__(self,lang,padre):
        return(self.myclass(lang,padre))

class mk_single_tag(object):
    def __init__(self,tid):
        self.tid=tid

    def __call__(self,lang,padre):
        return(SingleTag(lang,padre,self.tid))

class mk_align_tag(object):
    def __init__(self,style):
        self.style=style

    def __call__(self,lang,padre):
        return(AlignTag(lang,padre,self.style))

class mk_div_tag(object):
    def __init__(self,style):
        self.style=style

    def __call__(self,lang,padre):
        return(DivTag(lang,padre,self.style))

class mk_span_tag(object):
    def __init__(self,style):
        self.style=style

    def __call__(self,lang,padre):
        return(SpanTag(lang,padre,self.style))

class mk_pre_tag(object):
    def __init__(self,style):
        self.style=style

    def __call__(self,lang,padre):
        return(PreTag(lang,padre,self.style))
