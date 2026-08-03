#!/usr/bin/env python3
"""Embed previously fetched official web-source chunks into a local vector index.

Input is JSON: [{"text": "...", "title": "...", "url": "...", "issuer": "...",
"jurisdiction": "CN", "effective_date": "...", "retrieved_at": "...", "locator": "..."}]
The fetcher is intentionally separate so callers can enforce their official-domain allowlist.
"""
import argparse, json, sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

def index_sources(source_path, db_path, model_name):
    sources=json.load(open(source_path,encoding='utf-8')); model=SentenceTransformer(model_name)
    con=sqlite3.connect(db_path); con.execute('CREATE TABLE IF NOT EXISTS vector_rules (id INTEGER PRIMARY KEY, rule_id TEXT, title TEXT, locator TEXT, source_url TEXT, effective_date TEXT, text TEXT, vector BLOB, dimension INTEGER, model TEXT, source_type TEXT, issuer TEXT, jurisdiction TEXT, retrieved_at TEXT)')
    texts=[s.get('text','') for s in sources]; vectors=model.encode(texts,normalize_embeddings=True)
    for s,v in zip(sources,vectors):
        con.execute('INSERT INTO vector_rules(rule_id,title,locator,source_url,effective_date,text,vector,dimension,model,source_type,issuer,jurisdiction,retrieved_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(s.get('rule_id','WEB-'+str(abs(hash(s.get('url',''))))),s.get('title'),s.get('locator'),s.get('url'),s.get('effective_date'),s.get('text',''),v.astype('float32').tobytes(),len(v),model_name,'official_web',s.get('issuer'),s.get('jurisdiction'),s.get('retrieved_at')))
    con.commit(); con.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('sources'); p.add_argument('index'); p.add_argument('--model',default='BAAI/bge-m3'); a=p.parse_args(); index_sources(a.sources,a.index,a.model)
