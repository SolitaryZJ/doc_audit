#!/usr/bin/env python3
"""Retrieve regulation rules by cosine similarity from a local embedding index."""
import argparse, json, sqlite3, numpy as np
from sentence_transformers import SentenceTransformer

def retrieve(db_path, query, k, model_name):
    model=SentenceTransformer(model_name); q=model.encode([query],normalize_embeddings=True)[0]; con=sqlite3.connect(db_path); con.row_factory=sqlite3.Row
    hits=[]
    for row in con.execute('SELECT * FROM vector_rules WHERE model=?',(model_name,)):
        v=np.frombuffer(row['vector'],dtype='float32'); hits.append((float(np.dot(q,v)),dict(row)))
    con.close(); hits.sort(key=lambda x:x[0],reverse=True)
    for score,item in hits[:k]: item.pop('vector',None); item['score']=score
    return [item for _,item in hits[:k]]

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('index'); p.add_argument('query'); p.add_argument('-k',type=int,default=5); p.add_argument('--model',default='all-MiniLM-L6-v2'); a=p.parse_args(); print(json.dumps(retrieve(a.index,a.query,a.k,a.model),ensure_ascii=False,indent=2))
