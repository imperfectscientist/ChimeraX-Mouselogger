# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 14 nodes · 19 edges · 3 communities (0 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `72de900c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MouseTracker
- _MyAPI
- cmd.py

## God Nodes (most connected - your core abstractions)
1. `MouseTracker` - 8 edges
2. `_MyAPI` - 4 edges
3. `handle_mouselogger()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `handle_mouselogger()` --calls--> `MouseTracker`  [EXTRACTED]
  src/cmd.py → src/cmd.py  _Bridges community 0 → community 2_

## Import Cycles
- None detected.

## Communities (3 total, 3 thin omitted)

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MouseTracker` connect `MouseTracker` to `cmd.py`?**
  _High betweenness centrality (0.603) - this node is a cross-community bridge._
- **Why does `_MyAPI` connect `_MyAPI` to `cmd.py`?**
  _High betweenness centrality (0.423) - this node is a cross-community bridge._
- **Why does `handle_mouselogger()` connect `cmd.py` to `MouseTracker`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._