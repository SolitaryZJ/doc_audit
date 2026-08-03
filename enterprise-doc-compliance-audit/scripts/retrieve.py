#!/usr/bin/env python3
"""Retrieve top regulation citations for a query using local SQLite FTS5."""
import argparse, json, sqlite3
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('index'); p.add_argument('query'); p.add_argument('-k',type=int,default=5); a=p.parse_args(); con=sqlite3.connect(a.index); con.row_factory=sqlite3.Row
    rows=con.execute('SELECT r.* FROM rules_fts f JOIN rules r ON r.id=f.rowid WHERE rules_fts MATCH ? ORDER BY bm25(rules_fts) LIMIT ?', (a.query,a.k)).fetchall(); print(json.dumps([dict(x) for x in rows],ensure_ascii=False,indent=2)); con.close()
