# Profiling & budgets — depth for `performance-optimization`

Detail the body defers here: the Godot profiler walkthrough, the CPU-vs-GPU triage flow, a
pooling manager, batching/instancing rules, allocation/GC guidance, LOD/culling, and asset
budgets. Target: **Godot 4.x**.

## 1. CPU-vs-GPU triage (decide before you fix)

```text
1. Read total frame time vs your budget (16.67 ms @60).
2. Compare CPU-frame time and GPU-frame time:
     GPU >> CPU  → GPU-bound  → draw calls, overdraw, shader cost, resolution, lights/shadows.
     CPU >> GPU  → CPU-bound  → scripts, physics, pathfinding, allocations/GC, too many nodes.
     Both high / alternating → find the per-frame spike in the timeline (one function/system).
3. Within the bound side, sort costs descending and attack the top one only.
4. Re-measure. If it didn't move the frame time, you fixed the wrong thing — revert and re-triage.
```

A GPU-bound game won't speed up from faster C#; a CPU-bound game won't speed up from fewer draw
calls. This split is the single most important decision in performance work.

## 2. Profiler quick start

**Godot 4.x**
- Editor: **Debugger ▸ Profiler** (per-function script + physics time, frame time), and the
  **Monitors** tab (FPS, draw calls, video/static memory, object/node counts).
- Code: `Performance.get_monitor(Performance.TIME_PROCESS)` (process ms),
  `Performance.TIME_PHYSICS_PROCESS`, `Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME`,
  `Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME`, `Performance.MEMORY_STATIC`.
- Visual debugging: viewport **View Information / View Frame Time** overlays.
- **Profile an exported release build** on target hardware, not only the editor.

## 3. Pooling manager (generic)

```text
class Pool<T>:
    free: list
    create_fn, reset_fn
    prewarm(n):  for n → free.push(create_fn())          # allocate up front, off the hot path
    acquire():   t = free.pop() or create_fn(); activate(t); return t
    release(t):  reset_fn(t); deactivate(t); free.push(t)  # never destroy; recycle
```

Pool anything spawned frequently and briefly: bullets, shells, particles, damage numbers,
enemies in waves, audio one-shots. Pre-warm at load to avoid first-use hitches. Cap the pool and
decide an overflow policy (grow, or recycle the oldest).

## 4. Batching & instancing rules

- **What breaks a batch:** a different material, texture, or render state between objects. Share
  materials and **atlas** textures so runs of objects submit as one draw call.
- **Identical meshes, many instances** → `MultiMesh` + `MultiMeshInstance2D/3D`.
- **Static geometry** → mark static; bake where possible.
- **2D** → texture atlases + a shared material batch sprites; avoid per-sprite materials.
- **UI** → a changing element shouldn't dirty the whole canvas.
- **Lights/shadows** → bake static lighting; cap real-time shadow casters; cull small shadows.

## 5. Allocation / GC guidance

- **GDScript:** don't build new `Array`/`Dictionary` each `_process`; reuse them; prefer typed
  arrays; avoid heavy work in `_process` that belongs on a timer/signal.
- **General:** strings are a classic hidden allocator (concatenation, formatting) — build them
  rarely, cache results.

## 6. Do-less techniques (algorithmic wins)

- **Run less often:** update AI/HUD/expensive checks on a timer or every N frames, not every
  frame; stagger across frames (time-slicing).
- **Spatial partition:** grid/quadtree/octree so queries touch nearby objects only, not all N.
- **LOD & culling:** lower detail at distance; frustum/occlusion culling; despawn off-screen
  far entities.
- **Cache results:** memoize pathfinding, line-of-sight, and derived data; invalidate on change.
- **Defer/Amortize:** spread procedural generation and loading across frames to avoid spikes.

## 7. Asset budgets (prevent regressions at the source)

| Asset | Typical desktop budget | Mobile budget | Notes |
|-------|------------------------|---------------|-------|
| Texture max size | 2048–4096 | 1024–2048 | use mipmaps; compress (BCn / ASTC) |
| Character triangles | 30k–80k | 5k–20k | LODs for distance |
| Draw calls / frame | low thousands | a few hundred | the count that matters most on mobile |
| Real-time lights | a few | 1–2 + baked | bake the rest |
| Audio | streamed music, short SFX in memory | same | don't decompress everything at load |

Mobile adds **thermal throttling**: a game that hits 60 FPS for 2 minutes then drops is
overheating — target headroom, cap frame rate, and reduce sustained GPU load.
