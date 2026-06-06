# -*- coding: utf-8 -*-
import json, re, unicodedata, sys
sys.stdout.reconfigure(encoding="utf-8")
D=json.load(open("songs.json",encoding="utf-8"))
FIX={"¡":"Á","·":"á","Á":"ç","È":"é","Ì":"í","Ò":"ñ","Û":"ó","…":"Ô"}
for s in D: s['title']="".join(FIX.get(c,c) for c in s['title'])

QUOTES=re.compile(r"['’‘ʼ`\"“”]")
def foldchar(c):
    c=unicodedata.normalize('NFD',c.lower())
    c=''.join(ch for ch in c if unicodedata.category(ch)!='Mn')
    if QUOTES.match(c): return ''
    return re.sub(r'[^a-z0-9]+',' ',c)
def build(s):
    n='';m=[]
    for i,ch0 in enumerate(s):
        for ch in foldchar(ch0):
            if ch==' ' and (not n or n[-1]==' '): continue
            n+=ch; m.append(i)
    while n and n[-1]==' ': n=n[:-1]; m.pop()
    return n,m
for s in D: s['_n'],s['_map']=build(s['title'])
def fold(q): return build(q)[0]

def search(q):
    qn=fold(q); ex,pf,wd,sb=[],[],[],[]
    for s in D:
        i=s['_n'].find(qn)
        if i<0: continue
        s['_i']=i
        if s['_n']==qn: ex.append(s)
        elif i==0: pf.append(s)
        elif s['_n'][i-1]==' ': wd.append(s)
        else: sb.append(s)
    for g in (ex,pf,wd,sb): g.sort(key=lambda s:s['_n'])
    return ex+pf+wd+sb,qn
def hl(s,qn):
    qi=s['_i']; t=s['title']; m=s['_map']
    a=m[qi]; b=m[qi+len(qn)-1]
    return t[:a]+'['+t[a:b+1]+']'+t[b+1:]

tests=["agua de beber","take the a train","besame mucho","senora","my funny","giant steps",
       "march","quizas","obsesion","ain't mis","aint mis","round midnight"]
for q in tests:
    res,qn=search(q)
    print(f"\nQ={q!r} -> {len(res)}")
    for s in res[:2]: print("   ",hl(s,qn),"|",s['books'])
