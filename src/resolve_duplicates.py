import argparse, json, re
import pandas as pd
from rapidfuzz.fuzz import ratio

def norm(v):
    s = "" if pd.isna(v) else str(v).lower().strip()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def pair_score(a, b, fields, weights=None):
    weights = weights or {f:1.0 for f in fields}
    total = sum(weights.get(f,1.0) for f in fields)
    score = 0.0
    detail = {}
    for f in fields:
        s = ratio(norm(a.get(f,"")), norm(b.get(f,"")))
        detail[f] = s
        score += s * weights.get(f,1.0)
    return score/total if total else 0.0, detail

def find_duplicates(df, fields, threshold=85):
    rows = df.to_dict("records")
    matches=[]
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            score, detail = pair_score(rows[i], rows[j], fields)
            if score >= threshold:
                matches.append({"row_a":i,"row_b":j,"score":round(score,2),"field_scores":detail})
    return sorted(matches, key=lambda x:x["score"], reverse=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--fields",required=True); ap.add_argument("--threshold",type=float,default=85)
    a=ap.parse_args()
    df=pd.read_csv(a.csv)
    fields=[x.strip() for x in a.fields.split(",")]
    print(json.dumps(find_duplicates(df,fields,a.threshold),indent=2))

if __name__=="__main__": main()
