import json
songs = json.load(open("songs.json", encoding="utf-8"))

# Repair mis-mapped font glyphs from PDF extraction (accented Latin/Portuguese letters).
FIX = {"¡":"Á","·":"á","Á":"ç","È":"é",
       "Ì":"í","Ò":"ñ","Û":"ó","…":"Ô"}
def repair(t): return "".join(FIX.get(c, c) for c in t)
nfix = 0
for s in songs:
    r = repair(s["title"])
    if r != s["title"]: nfix += 1
    s["title"] = r
print("titles repaired:", nfix)
books = {
 "01":"The Real Book – Volume I","02":"The Real Book – Volume II","03":"The Real Book – Volume III",
 "04":"The Real Book – Volume IV","05":"The Real Book – Volume V","06":"The Real Book – Volume VI",
 "08":"The Real Pat Metheny Book","09":"Miles Davis Real Book",
 "10":"The Charlie Parker Real Book (The Bird Book)","11":"The Duke Ellington Real Book",
 "12":"The Bud Powell Real Book","13":"The Real Christmas Book (2nd Edition)",
 "14":"The Real Rock Book","15":"The Real Rock Book – Volume II","16":"The Real Tab Book – Volume I",
 "17":"The Real Bluegrass Book","18":"The Real Dixieland Book","19":"The Real Latin Book",
 "20":"The Real Worship Book","21":"The Real Blues Book","22":"The Real Bebop Book",
 "23":"The Real Jazz Solos Book","24":"The Real R&B Book","25":"The Real Country Book",
 "30":"The Real Vocal Book – Volume I","31":"The Real Vocal Book – Volume II",
 "32":"The Real Vocal Book – Volume III",
}
# verify every book number used has a name
used = {b for s in songs for b in s["books"]}
missing = used - set(books)
assert not missing, f"missing book names: {missing}"
print("songs:", len(songs), "| book codes used:", len(used), "| all named:", not missing)

DATA = {"books": books, "songs": songs}
blob = json.dumps(DATA, ensure_ascii=False, separators=(",",":"))

TEMPLATE = open("template.html", encoding="utf-8").read()
html = TEMPLATE.replace("/*__DATA__*/", blob)
open("index.html","w",encoding="utf-8").write(html)
import os
print("index.html:", round(os.path.getsize("index.html")/1024), "KB")
