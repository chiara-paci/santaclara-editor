# -*- coding: utf-8 -*-

from santaclara_editor.santaclara_lang.tags import Tag

class Table(list):
    def __init__(self,style=""):
        list.__init__(self)
        self.style=style
    
    def html(self):
        S=u"<center><table"
        if self.style:
            S+=u' class="'+self.style+'"'
        S+=u">\n"
        for row in self:
            S+=row.html()
        S+=u"</table></center>\n"
        return(S)

class Row(list):
    def __init__(self):
        list.__init__(self)
        self.prop=u""
    
    def html(self):
        S=u"<tr"
        if self.prop: S+=u" "+self.prop
        S+=u">\n"
        for cell in self:
            S+=cell.html()
        S+=u"</tr>\n"
        return(S)

    def set_properties(self,txt): 
        txt=txt[1:-1]
        token=txt.split(",")
        p=[]
        for s in token:
            x=s.split("=")
            if len(x)==1: 
                p.append(s)
                continue
            p.append(x[0]+'="'+x[1]+'"')
        self.prop=" ".join(p)

class Cell(unicode):
    def __new__(cls,txt=u""):
        self=unicode.__new__(Cell,txt)
        self.prop=u""
        self.td=u"td"
        return(self)

    def html(self):
        S=u"<"+self.td
        if self.prop: S+=u" "+self.prop
        S+=u">\n"
        S+=self+u"</"+self.td+">\n"
        return(S)

    def set_properties(self,txt): 
        txt=txt[1:-1]
        token=txt.split(",")
        p=[]
        for s in token:
            if s==u"th": 
                self.td="th"
                continue
            x=s.split("=")
            if len(x)==1: 
                p.append(s)
                continue
            p.append(x[0]+'="'+x[1]+'"')
        self.prop=" ".join(p)

    def __add__(self,other): 
        res=unicode.__add__(self,other)
        ret=Cell(res)
        ret.prop=self.prop
        ret.td=self.td
        return ret

    def __mod__(self,other): 
        res=unicode.__mod__(self,other)
        ret=Cell(res)
        ret.prop=self.prop
        ret.td=self.td
        return ret

    def __mul__(self,other): 
        res=unicode.__mul__(self,other)
        ret=Cell(res)
        ret.prop=self.prop
        ret.td=self.td
        return ret

    def __rmod__(self,other): 
        res=unicode.__rmod__(self,other)
        ret=Cell(res)
        ret.prop=self.prop
        ret.td=self.td
        return ret

    def __rmul__(self,other): 
        res=unicode.__rmul__(self,other)
        ret=Cell(res)
        ret.prop=self.prop
        ret.td=self.td
        return ret

class TableTag(Tag):
    def __init__(self,lang,padre):
        Tag.__init__(self,lang,padre,inline=False)
        lab=r'[a-zA-Z0-9,=:]+'
        prop_td=r'\('+lab+r'\)'
        prop_tr=r'\{'+lab+r'\}'
        txt=r'[^\r\n\|:]+|\r?\n'
        sep=r':|\|'
        regexp=r'('+sep+'|'+prop_td+'|'+prop_tr+'|'+txt+')'
        self.tokenizer=re.compile(regexp)
        self.re_prop_td=re.compile(prop_td)
        self.re_prop_tr=re.compile(prop_tr)

    def output(self,autoescape,outtype="html"):
        txt=Tag.output(self,autoescape,outtype)
        txt=txt.replace(u"\:",u'§a§')
        txt=txt.replace(u'\|',u'§b§')
        txt=txt.replace(u'\{',u'§c§')
        txt=txt.replace(u'\}',u'§d§')
        txt=txt.replace(u'\(',u'§e§')
        txt=txt.replace(u'\)',u'§f§')
        txt=self.filter(txt)
        txt=txt.replace(u'§a§',u":")
        txt=txt.replace(u'§b§',u'|')
        txt=txt.replace(u'§c§',u'{')
        txt=txt.replace(u'§d§',u'}')
        txt=txt.replace(u'§e§',u'(')
        txt=txt.replace(u'§f§',u')')
        return(txt)

    def filter(self,txt):
        L=self.tokenizer.findall(txt)
        if self.args: 
            T=Table(self.args[0])
        else:
            T=Table()
        cell=Cell()
        row=Row()
        for t in L:
            if t==":":
                row.append(cell)
                cell=Cell()
                continue
            if t=="|":
                row.append(cell)
                T.append(row)
                cell=Cell()
                row=Row()
                continue
            if self.re_prop_td.match(t):
                cell.set_properties(t)
                continue
            if self.re_prop_tr.match(t):
                row.set_properties(t)
                continue
            cell+=t
        if cell:
            row.append(cell)
            T.append(row)
        elif row:
            T.append(row)        
        return(T.html())

