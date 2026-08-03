#!/usr/bin/env python3
"""Build a local SQLite FTS5 index from a regulation-pack JSON file."""
import argparse, json, sqlite3

def build(pack_path, db_path):
    pack=json.load(open(pack_path,encoding='utf-8')); con=sqlite3.connect(db_path)
    con.executescript('DROP TABLE IF EXISTS rules; DROP TABLE IF EXISTS rules_fts; CREATE TABLE rules (id INTEGER PRIMARY KEY, rule_id TEXT, title TEXT, locator TEXT, source_url TEXT, effective_date TEXT, text TEXT); CREATE VIRTUAL TABLE rules_fts USING fts5(text, content=rules, content_rowid=id);')
    for r in pack.get('rules',[]):
        c=(r.get('citations') or [{}])[0]; text=' '.join([r.get('check',''), r.get('scope',{}).get('document_type',''), c.get('title',''), c.get('locator','')])
        cur=con.execute('INSERT INTO rules(rule_id,title,locator,source_url,effective_date,text) VALUES (?,?,?,?,?,?)',(r.get('rule_id'),c.get('title'),c.get('locator'),c.get('source_url'),c.get('effective_date'),text)); con.execute('INSERT INTO rules_fts(rowid,text) VALUES (?,?)',(cur.lastrowid,text))
    con.commit(); con.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('pack'); p.add_argument('index'); a=p.parse_args(); build(a.pack,a.index)
