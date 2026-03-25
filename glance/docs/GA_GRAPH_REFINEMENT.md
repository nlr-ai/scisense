# GLANCE GA — Graph Refinement Process

## What this is
The GA's information architecture expressed as an L3 graph. Each design element
is a node with physics dimensions. The graph is the single source of truth for
what the GA communicates.

## Refinement loop

1. **Map** — Every information vector becomes an L3 node (actor/moment/narrative/space/thing)
2. **Dimension** — Assign weight (importance), stability (confidence), energy (needs work)
3. **Link** — Connect nodes with relational dimensions (hierarchy, trust, friction, affinity, aversion)
4. **Contain** — Place nodes inside space nodes (zone_left, zone_right) with hierarchy:-1 links
5. **Identify tension** — High energy + low stability = unresolved. The graph shows what to fix.
6. **Design** — Marco translates the graph to visual elements. Each node = a visual element. Each link = a visual relationship.
7. **Test** — GLANCE protocol measures if the hierarchy was perceived (S9b). Data flows back to update stability.
8. **Iterate** — Stability grows with data. Energy drops when resolved. The graph converges.

## Current tensions (2026-03-25)

| Node | Weight | Stability | Energy | Status |
|------|--------|-----------|--------|--------|
| thing:glance | 1.00 | 0.40 | 0.90 | CRITICAL — ≥80% is a target, not a result |
| thing:ga_thumbnail | 0.85 | 0.70 | 0.80 | OPEN — which GA to show? Loupe deformation? |
| narrative:spin | 0.50 | 0.65 | 0.75 | FUZZY — Vorland extrapolation not direct |

## What stabilizes the graph
- **Data from crash test** (N=5-10) → thing:glance stability rises from 0.40 to 0.70+
- **Marco's visual execution** → thing:ga_thumbnail energy drops to 0.15
- **Stronger spin citation** or **reframe** → narrative:spin stability rises to 0.80+

## Invariants
- permanence = 1.0 on both spaces (the message is permanent scientific fact)
- ambivalence = 0.0 (no ambiguity — problem is clear, solution is clear)
- hierarchy is the critical dimension (V7) — encoded by P32 (length)
- S9b measures hierarchy perception — graph and protocol are aligned

## Files
- Graph: `data/glance_ga_graph.yaml`
- Math: `GLANCE_Mathematics.md`
- Paper: `GLANCE_Paper_Draft.md`
- Design spec: `GLANCE_GA_Design_Spec.md` (Marco's brief)
