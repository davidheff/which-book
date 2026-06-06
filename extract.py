import fitz, re, json
from collections import defaultdict

doc = fitz.open("MiscRealbksongfind2016.pdf")
COL_BOUNDS = [(0, 200), (200, 405), (405, 612)]
# all numeric-only parentheticals; we take the LAST as book numbers
NUM_RE = re.compile(r'\((\d{2}(?:\s*,\s*\d{2})*)\)')

def col_of(x0):
    for i,(a,b) in enumerate(COL_BOUNDS):
        if a <= x0 < b: return i
    return 2

entries = []
for pno in range(len(doc)):
    d = doc[pno].get_text("dict")
    spans = []
    for b in d["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"]
                if not t.strip(): continue
                if s["size"] > 12: continue
                x0,y0,x1,y1 = s["bbox"]
                if y0 > 755 or y0 < 30: continue
                spans.append((col_of(x0), y0, x0, t))
    lines = defaultdict(list)
    for col,y0,x0,t in spans:
        lines[(col, round(y0))].append((x0,t))
    percol = defaultdict(list)
    for (col,ry),parts in lines.items():
        parts.sort()
        percol[col].append((ry, min(p[0] for p in parts), " ".join(p[1] for p in parts).strip()))
    for col in sorted(percol):
        rows = sorted(percol[col])
        if not rows: continue
        base_x = min(r[1] for r in rows)
        buf=None
        for ry,x0,text in rows:
            if x0 > base_x+4 and buf is not None:
                buf += " " + text
            else:
                if buf is not None: entries.append(buf)
                buf=text
        if buf is not None: entries.append(buf)

songs, unparsed, fragments = [], [], []
for raw in entries:
    raw = re.sub(r'\s+',' ',raw).strip()
    ms = list(NUM_RE.finditer(raw))
    if not ms:
        unparsed.append(raw); continue
    m = ms[-1]
    title = raw[:m.start()].strip()
    books = [n.strip() for n in m.group(1).split(',')]
    if not title:
        unparsed.append(raw); continue
    if title[0].islower():
        fragments.append((title,books))
    songs.append({"title":title,"books":books})

# de-dupe identical (title,books) just in case
seen=set(); dedup=[]
for s in songs:
    k=(s["title"],tuple(s["books"]))
    if k in seen: continue
    seen.add(k); dedup.append(s)

print("parsed:",len(songs),"dedup:",len(dedup),"unparsed:",len(unparsed),"lowercase-start(frag?):",len(fragments))
print("\nlowercase-start titles:")
for t,b in fragments: print("  ",repr(t),b)
print("\nnon-song unparsed that AREN'T intro/key:")
for u in unparsed:
    if not re.match(r'(We|Simply|the numbers|song|Real Book Volume|as of|Unless|\d\d\.)',u):
        print("  ",repr(u[:80]))

# book number distribution sanity
from collections import Counter
bc=Counter(b for s in dedup for b in s["books"])
print("\nbook-number usage:", dict(sorted(bc.items())))
json.dump(dedup, open("songs.json","w",encoding="utf-8"), ensure_ascii=False)
print("\nwrote songs.json with",len(dedup),"songs")
