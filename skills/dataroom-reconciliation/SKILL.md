---
name: "dataroom-reconciliation"
description: "Reconcile a seller's data room (VDR) export against Tern's own dataroom index in a Google Sheet: flag Match / Close match / Missing, unreviewed docs, and Tern-only files."
---

# Dataroom reconciliation (seller VDR vs Tern index)

Use when the user wants to check that what the seller has disclosed in their data room matches the documents Tern has indexed and reviewed, usually on the deal master workbook's **DR** tab. Typical asks: "check the DR matches my index", "reconcile the data room", "what's missing from my review", "rerun the DR check on the new export".

The question being answered: **has every disclosed document been reviewed (seller → Tern), and is everything Tern relies on actually in the disclosed data room (Tern → seller)?** The seller export is what gets disclosed, so seller → Tern matters most.

## 1. Inputs and layout

The DR tab normally holds two lists stacked vertically:
- **Tern index** (Google Drive export), header row about row 3: `Parent Folder | Name | Type (File/Folder) | ID | Date Created | Last Updated | MD5 | Reference Number | Description (= review status: Reviewed / In Progress / Not started / N/A - folder) | Person to review | Comments`.
- **Seller VDR export** further down, under a title like "Dataroom index - Per seller data room site <date>": `Fileroom | Index (1.1.93) | Title | Hyperlink | Type (DOCUMENT/FOLDER/FILEROOM) | File Type | Level | Size | Status (Read/Unread) | Date Available | Unique Id`.

The two lists share no ID, so file name is the only key. Ignore the seller's Read/Unread column, which only tracks who opened what. Confirm the actual header rows and column letters by reading the tab, because layouts drift between deals.

If the user gives a Google Sheets link, read it with the Google Sheets connector (`get_values`). If the connector isn't connected, say so and ask them to connect it. A downloaded copy can be analysed instead, but writing back needs the connector.

## 2. How names differ (why a VLOOKUP fails)

- Tern names carry file extensions (sometimes doubled: `.xlsx.xlsx`, `.docx.pdf`); seller titles don't.
- VDR download prefixes on Tern names: `1.1.93_`, `1.15.2_1.15.2 `, `260806 - 1.1.92_`.
- Leading numbers from the "Post Meeting Info" fileroom: `10 General commentary.pdf` vs seller `General commentary`. Also `89 15 C - 87. ...`.
- `&` vs `-` (`Q & A` vs `Q - A`), `(1)`/`(2)` suffixes, double spaces, `merged_`.
- Reference codes the seller adds to files Tern saved without them: `15 C - 3.4 H&W G Cloud Variation` vs `H&W G Cloud Variation Aug 2026.pdf`.
- macOS junk in the Tern index: `._filename` and `.DS_Store`. The real file is listed separately, so exclude these.
- The seller export shows index `1.10` as `1.1` (number formatting). Match on titles, never on index.

## 3. Matching method (tiered, one-to-one)

1. Exclude folders and macOS junk.
2. **Match:** names identical after removing extensions, download prefixes, punctuation and `(n)` suffixes.
3. **Close match:** names identical apart from a reference code or prefix (`15 C - 87.`, leading `10 `).
4. **Fuzzy:** similarity ≥ 0.88, but **only if the dates and numbers in the names agree**. A 30/09 balance sheet is NOT a match for a 31 Aug one; it is Missing (a newer version). This rule matters: without it, new monthly accounts look already reviewed.
5. Everything else is **Missing**. Add a note "Newer/different version of Tern file: X" when a similar Tern file exists (similarity ≥ 0.8, or the title contains Updated/Revised/Final).
6. Where Tern holds several copies of a document, match to the copy with the **best review status**, so a Reviewed copy isn't flagged as Not started.
7. If the seller uploaded the same document twice, both seller rows point to one Tern row; note "Uploaded twice by seller".
8. Tern-only files are categorised as: **Duplicate copy** (an identical name is already matched), **Possible other version** (similarity 0.8–0.999), **Mac system file - exclude**, or **Not in seller DR** (received outside the data room, or a Tern working file).

Run the script below rather than matching by hand. Save it as `dr_match.py`. Build `tern.json` and `seller.json` from `get_values` reads, using the **sheet row numbers**, then run `python3 dr_match.py tern.json seller.json out.json`.

```python
#!/usr/bin/env python3
"""Reconcile a seller data room export against Tern's own dataroom index.
Usage: python3 dr_match.py tern.json seller.json out.json
tern.json   : [{"row":int,"folder":str,"name":str,"type":"File"|"Folder","status":str}, ...]
seller.json : [{"row":int,"idx":str,"title":str,"type":"DOCUMENT"|"FOLDER"|"FILEROOM"}, ...]
Rows are the sheet row numbers. Output: {"seller":[...],"tern":[...],"summary":{...}}"""
import json,re,sys
from difflib import SequenceMatcher
from collections import Counter
EXT=r'(\.(pdf|xlsx|xlsm|docx|xls|csv|doc|pptx|ppt|png|jpg|jpeg|msg|eml|zip|txt))+$'
RANK={'Reviewed':3,'In Progress':2,'Not started':1}
def base(s):
    s=re.sub(EXT,'',s.strip(),flags=re.I).strip()
    s=re.sub(r'^\._','',s)                    # macOS AppleDouble prefix
    s=re.sub(r'^\d{6}\s*-\s*','',s)           # "260806 - " date prefix
    s=re.sub(r'^(\d+(\.\d+)+_)+','',s)         # "1.1.93_" VDR download prefix (can repeat)
    return s
def clean(s):
    s=s.lower().replace('&','-'); s=re.sub(r'\(\d+\)','',s); s=re.sub(r'\bmerged_','',s)
    return re.sub(r'[^a-z0-9]','',s)
def core(s):                                   # also strip reference codes like "15 C - 87." / "89 15 C - 87." / "10 "
    s=re.sub(r'^\d+\s+(?=\d+\s*[A-Z&]+\.?\s*-)','',s)
    s=re.sub(r'^\d+\s*[A-Z&]+\.?\s*-\s*\d+(\.\d+)*\.?\s*','',s)
    s=re.sub(r'^\d+(\.\d+)*\.?\s+','',s); s=re.sub(r'^[!\s]+','',s)
    return clean(s)
def nums(s):
    s=re.sub(r'^\d+\s*[A-Z&]+\.?\s*-\s*\d+(\.\d+)*\.?\s*','',base(s)); return re.findall(r'\d+',s)
def sim(a,b): return SequenceMatcher(None,a,b).ratio()
def run(tern,seller):
    for t in tern:
        b=base(t['name']); t['full']=clean(b); t['core']=core(b)
        t['junk']=t['name'] in('.DS_Store','._.DS_Store') or t['name'].startswith('._')
    for s in seller:
        b=base(s['title']); s['full']=clean(b); s['core']=core(b)
    files=[t for t in tern if t['type']=='File' and not t['junk']]
    docs=[s for s in seller if s['type']=='DOCUMENT']
    used=set()
    def best_status(c): return max(c,key=lambda t:RANK.get(t.get('status',''),0))
    for key,res in (('full','Match'),('core','Close match')):
        for s in docs:
            if 'm' in s: continue
            c=[t for t in files if t[key] and t[key]==s[key]]
            if not c: continue
            free=[t for t in c if t['row'] not in used]
            m=best_status(free or c); used.add(m['row']); s.update(m=m,res=res)
    cand=sorted(((max(sim(s['core'],t['core']),sim(s['full'],t['full'])),s['row'],t['row'])
                 for s in docs if 'm' not in s for t in files if t['row'] not in used),reverse=True)
    S={s['row']:s for s in docs}; T={t['row']:t for t in files}
    for r,sr,tr in cand:
        s=S[sr]
        if r<0.88 or 'm' in s or tr in used: continue
        if nums(s['title'])!=nums(T[tr]['name']): continue   # different date/version = not a match
        used.add(tr); s.update(m=T[tr],res='Close match')
    seen={}; out_s=[]
    for s in seller:
        if s['type']!='DOCUMENT': out_s.append({'row':s['row'],'result':'N/A - folder','comment':'','tern_row':''}); continue
        if 'm' not in s:
            n=max(files,key=lambda t:sim(s['core'],t['core'])); sc=sim(s['core'],n['core'])
            note=('Newer/different version of Tern file: '+n['name']) if sc>=0.8 or re.search(r'updated|revised|final',s['title'],re.I) and sc>=0.6 else 'No equivalent in Tern index'
            out_s.append({'row':s['row'],'result':'Missing','comment':note,'tern_row':''}); continue
        m=s['m']; note='Same doc - reference number/prefix differs' if s['res']=='Close match' else ''
        if m['row'] in seen: note='Uploaded twice by seller (also index %s)'%seen[m['row']]
        seen.setdefault(m['row'],s['idx'])
        out_s.append({'row':s['row'],'result':s['res'],'comment':note,'tern_row':m['row']})
    matched={s['m']['row']:s for s in docs if 'm' in s}; out_t=[]
    for t in tern:
        if t['type']!='File': out_t.append({'row':t['row'],'result':'N/A - folder','comment':'','seller_row':''}); continue
        if t['row'] in matched: out_t.append({'row':t['row'],'result':'In seller DR','comment':'','seller_row':matched[t['row']]['row']}); continue
        if t['junk']: out_t.append({'row':t['row'],'result':'Mac system file - exclude','comment':'Hidden macOS file','seller_row':''}); continue
        n=max(docs,key=lambda s:sim(t['core'],s['core'])); sc=sim(t['core'],n['core'])
        if sc>=0.999: out_t.append({'row':t['row'],'result':'Duplicate copy','comment':'Other copy is matched','seller_row':n['row']})
        elif sc>=0.8: out_t.append({'row':t['row'],'result':'Possible other version','comment':'Check version/date vs seller doc','seller_row':n['row']})
        else: out_t.append({'row':t['row'],'result':'Not in seller DR','comment':'Received outside DR?','seller_row':''})
    nr=[x for x in out_s if x['tern_row'] and RANK.get(next(t for t in tern if t['row']==x['tern_row']).get('status',''),0)<3]
    summary={'seller':dict(Counter(x['result'] for x in out_s)),'tern':dict(Counter(x['result'] for x in out_t)),'matched_not_reviewed':len(nr)}
    return {'seller':out_s,'tern':out_t,'summary':summary}
if __name__=='__main__':
    tern=json.load(open(sys.argv[1])); seller=json.load(open(sys.argv[2]))
    res=run(tern,seller); json.dump(res,open(sys.argv[3],'w'),indent=0); print(json.dumps(res['summary'],indent=1))
```

Before writing anything, sanity-check the output: spot-check 5–10 matches, and read every Missing item and every Close match produced by the fuzzy step. If a reference-code pattern isn't handled (a new deal's naming convention), adjust `core()` and rerun.

## 4. Writing back into the DR tab

Load the google-workspace skill and its Sheets reference before writing. Use the Google Sheets connector and write into empty columns to the right of both lists (columns Q onward has worked; check that they're empty first). Don't alter the user's existing columns or filter.

**Next to the seller list** (header on the seller header row):
- Q `Match result` (Match / Close match / Missing / N/A - folder), as values
- R `Basis / comment`, as values
- S `Tern index row` (sheet row number of the matched Tern file), as values
- T `Tern file name`: `=ARRAYFORMULA(IF(S709:S1251="","",VLOOKUP(S709:S1251,{ROW(C1:C704),C1:C704},2,FALSE)))`
- U `Tern review status`: same pattern on the status column (J), with `&""` appended
- V `Action flag`: `=ARRAYFORMULA(IF((Q709:Q1251="Match")+(Q709:Q1251="Close match"),IF(U709:U1251="Reviewed","OK","Not yet reviewed ("&U709:U1251&")"),IF(Q709:Q1251="Missing","Not in Tern index - review","")))`

**Next to the Tern index:**
- Q `Seller DR result`, R `Comment`, S `Seller DR row`, as values
- T `Seller DR index | title`: an ARRAYFORMULA VLOOKUP on the seller Index and Title columns

Adjust the row ranges to the actual lists.

**Summary lines:** use COUNTIF formulas, not typed numbers. Put one on the empty row above the seller list (Match / Close match / Missing / Not yet reviewed) and one in row 1 (In seller DR / Not in seller DR / duplicates, versions and Mac files).

**Formatting:**
- Copy the existing header format onto the new headers (copyPaste PASTE_FORMAT from column B's header cell).
- Colour Match / In seller DR green, Close match / Possible other version amber, and Missing / Not in seller DR red, using conditional formatting with CUSTOM_FORMULA rules.
- Make action flags starting "Not" bold red.
- Set sensible column widths.

**Gotchas:**
- The DR tab often has a filter on. `copyPaste` of formulas fails with "not supported on a range with a filtered-out row", which is why the formula columns use one ARRAYFORMULA per column instead of fill-down.
- Send seller index values only through formulas or as text. Typed into a cell, `1.10` becomes the number 1.1.
- Before writing, re-read the live sheet and confirm its rows still match what was analysed.
- Values are written in one `update_values` call per block, with numbers as numbers.

After writing, read back each block with `get_values`. Check that the summary counts equal the script's summary, the lookups show the right file names, and there are no `#N/A` or `#REF!` values.

If the user wants a standalone file instead, or the connector isn't available, build an .xlsx with three tabs: Summary, Seller DR vs Tern, and Tern only.

## 5. Reporting back

Keep it short and lead with what needs action:
- Counts: Match / Close match / Missing, and matched documents not yet Reviewed (grouped by folder; corporate/stat-book documents are often the gap).
- The Missing list by theme. Note which were added after the Tern index's last-updated date, since those are usually just new uploads.
- Tern-only files that look like documents Tern relies on but which aren't formally disclosed (received by email, older versions). These need adding to the data room before disclosure is finalised.
- Seller-side oddities (duplicate uploads).
- Remind the user that the row-number links break if rows are inserted, deleted or sorted. New rows go below the lists, and the check should be rerun when a new seller export arrives.