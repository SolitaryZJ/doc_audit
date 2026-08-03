#!/usr/bin/env python3
"""Build a local embedding index for regulation-pack rules."""
import argparse, json, sqlite3, numpy as np
from sentence_transformers import SentenceTransformer

def build(pack_path, db_path, model_name):
    pack=json.load(open(pack_path,encoding='utf-8')); model=SentenceTransformer(model_name); rows=[]
    for rule in pack.get('rules',[]):
        for citation in rule.get('citations',[]):
            text=' '.join(filter(None,[rule.get('check',''), citation.get('title'), citation.get('locator')]))
            rows.append((rule.get('rule_id'), citation.get('title'), citation.get('locator'), citation.get('source_url'), citation.get('effective_date'), text))
    vectors=model.encode([r[-1] for r in rows], normalize_embeddings=True)
    con=sqlite3.connect(db_path); con.execute('DROP TABLE IF EXISTS vector_rules'); con.execute('CREATE TABLE vector_rules (id INTEGER PRIMARY KEY, rule_id TEXT, title TEXT, locator TEXT, source_url TEXT, effective_date TEXT, text TEXT, vector BLOB, dimension INTEGER, model TEXT)')
    for row, vec in zip(rows,vectors): con.execute('INSERT INTO vector_rules(rule_id,title,locator,source_url,effective_date,text,vector,dimension,model) VALUES (?,?,?,?,?,?,?,?,?)',(*row,vec.astype('float32').tobytes(),len(vec),model_name))
    con.commit(); con.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('pack'); p.add_argument('index'); p.add_argument('--model',default='BAAI/bge-m3'); a=p.parse_args(); build(a.pack,a.index,a.model)
