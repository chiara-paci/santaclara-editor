import shlex

### utility

def shlex_split(S):
    def s(x):
        return unicode(x,'utf-8')
    return map(s,shlex.split(S.encode('utf-8')))
