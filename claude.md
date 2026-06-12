# CLAUDE.md — Trail Echoes Development Guide

## Mission

You are working on **Trail Echoes**, a Blueprint-first Unreal Engine 5 exploration RPG inspired by Taiwan mountain trails.

Current prototype mountain:

```text
Hehuan East Peak
```

Current milestone:

```text
Milestone 2: Playable Trail Corridor
```

Target gameplay loop:

```text
Spawn at trail entrance
→ See a visible trail
→ Follow the trail
→ Reach the summit marker
→ Trigger the summit badge placeholder
```

Do not expand scope beyond Milestone 2 unless explicitly requested.

---

## Repository Structure

```text
data/
  gis/
  gpx/
  metadata/

docs/
  adr/
  design/

game/
  TrailEchoes/

tools/
  unreal/
```

Important files:

```text
tools/unreal/import_gpx_guide_spline.py
game/TrailEchoes/Content/TrailEchoes/Maps/L_HehuanEastPeak_Greybox.umap
```

Existing Blueprint assets include:

```text
BP_GPXTrailGuide
BP_SummitTrigger
WBP_SummitBadgePlaceholder
```

The level contains:

```text
GPXTrailGuide
├── DefaultSceneRoot
└── TrailSpline
```

---

## Verified Baseline

Milestone 0 and Milestone 1 are complete.

Issue #29 has been manually verified and closed.

Confirmed behavior:

```text
- The UE5 project opens successfully.
- L_HehuanEastPeak_Greybox loads successfully.
- GPXTrailGuide persists after closing and reopening UE5.
- TrailSpline points persist without rerunning the importer.
- The player can walk to the summit triangle marker.
- BP_SummitTrigger still fires in Play Mode.
- WBP_SummitBadgePlaceholder still appears.
```

Current limitation:

```text
TrailSpline is visible in the Editor but not visible in Play Mode.
```

---

## Branch and Commit Policy

Work only on the current integration branch:

```text
feature/m2-playable-trail-corridor
```

Before editing:

```bash
git status
git branch --show-current
git pull --ff-only origin main
git lfs status
```

Create one focused commit per Issue:

```text
#30 feat: add visible greybox trail ribbon mesh
#31 feat: add placeholder trail material
#32 feat: align player start with trail entrance
#33 feat: add temporary summit marker mesh
#34 feat: add fall recovery checkpoint
#35 docs: document GPX-to-UE5 guide spline workflow
```

Do not combine unrelated changes into one commit.

Before every commit:

```bash
git status
git diff --stat
git lfs status
```

Do not commit generated directories such as:

```text
Binaries/
DerivedDataCache/
Intermediate/
Saved/
.vscode/
.idea/
```

Do not force-push, merge into `main`, delete branches, or close Issues.

---

## Unreal Binary Asset Safety Rules

Unreal binary assets cannot be reliably reviewed as text:

```text
.uasset
.umap
```

Never edit, replace, regenerate, or delete existing `.uasset` or `.umap` files without first explaining:

```text
1. Which asset must change
2. Why it must change
3. Whether the change can be performed by script
4. Which manual UE5 verification is required afterward
```

Do not assume binary diffs are meaningful.

Prefer text-based automation where practical:

```text
.py
.md
.csv
.json
.ini
.cpp
.h
```

For Blueprint changes, provide either:

```text
A. A UE5 Python Editor script that creates or updates the asset safely
```

or:

```text
B. Precise UE5 GUI instructions for the user
```

If a Blueprint must be modified manually, stop and request a screenshot after each small group of nodes.

---

## Milestone 2 Scope

### #30 — Add Visible Greybox Trail Ribbon Mesh

Upgrade the existing `BP_GPXTrailGuide`.

Do not create a second independent spline data source.

Preferred design:

```text
BP_GPXTrailGuide
├── DefaultSceneRoot
├── TrailSpline
└── Construction Script
    └── Generate one SplineMeshComponent per spline segment
```

Suggested Blueprint logic:

```text
Construction Script
└── For Loop: 0 → GetNumberOfSplinePoints(TrailSpline) - 2
    └── Add Spline Mesh Component
        ├── Static Mesh = /Engine/BasicShapes/Cube
        ├── Forward Axis = X
        ├── Collision = NoCollision
        ├── Set Start and End
        ├── Set Start Scale
        └── Set End Scale
```

Per segment:

```text
Start Point = Index
End Point   = Index + 1
Coordinate Space = Local
```

Initial ribbon values:

```text
TrailMeshOffsetZ = -110 cm
Start Scale      = (2.0, 0.1)
End Scale        = (2.0, 0.1)
```

Reason for offset:

```text
The imported editor guide spline was intentionally raised above the Landscape.
The visible ribbon should remain near the ground.
```

Keep collision disabled. The player should continue walking on Landscape collision.

### #31 — Add Placeholder Trail Material

Create a simple Greybox material:

```text
M_Trail_Greybox
```

Requirements:

```text
- Clearly distinguish trail from checkerboard Landscape
- Use a simple dark-grey or earth-tone appearance
- Avoid textures, normal maps, snow, wetness, or advanced shading
```

### #32 — Align PlayerStart with Trail Entrance

Requirements:

```text
- Place PlayerStart at the first GPX route point
- Keep the player above the Landscape
- Face the first trail segment
- Verify that Play Mode begins with the route visible ahead
```

### #33 — Add Temporary Summit Marker

Requirements:

```text
- Add a visible placeholder marker near the existing summit trigger
- Use simple geometry such as a cube, cylinder, or sign
- Do not block the trigger volume
- Keep Summit Badge behavior unchanged
```

### #34 — Add Fall Recovery

Implement the smallest reliable recovery path:

```text
Player falls below threshold
→ Teleport player back to PlayerStart
```

Do not build a complex checkpoint manager yet.

### #35 — Document GPX-to-UE5 Workflow

Create:

```text
docs/workflows/gpx-to-ue5-guide-spline.md
```

Document:

```text
GPX
→ QGIS
→ Points along geometry
→ CSV
→ Unreal Python importer
→ UE5 TrailSpline
→ Save All
→ Persistence verification
```

Include prerequisites, commands, expected inputs, expected outputs, and common failure modes.

---

## Do Not Implement During Milestone 2

Do not add:

```text
- Final environment art
- Realistic trail meshes
- Landscape sculpting
- Whiteout weather
- Dynamic rain
- Snow
- Day-night cycle
- Complex checkpoint systems
- Save Game
- Multi-mountain pipeline refactors
- Second mountain content
```

These belong to later milestones.

---

## Required Manual Verification

After any `.uasset` or `.umap` change, ask the user to open UE5 and verify:

```text
[ ] Project opens successfully
[ ] L_HehuanEastPeak_Greybox loads successfully
[ ] Existing TrailSpline points remain present
[ ] Closing and reopening the Editor does not remove spline points
[ ] Trail ribbon is visible in Play Mode
[ ] Trail ribbon follows the GPX route
[ ] Trail ribbon is not floating at waist height
[ ] Trail ribbon is not buried across large sections
[ ] Trail ribbon has no major discontinuities
[ ] Player still walks on Landscape collision
[ ] PlayerStart faces the trail entrance
[ ] Summit marker is visible
[ ] Falling below the threshold returns the player safely
[ ] Player can reach the summit
[ ] Summit Trigger still fires
[ ] Badge Placeholder still appears
```

Do not claim an Unreal asset change is complete before the user confirms the Play Mode test.

---

## Final Handoff Format

When Milestone 2 changes are ready for review, stop before merging and report:

```text
1. Current branch
2. Commits grouped by Issue
3. Changed files grouped by commit
4. Text-based diffs worth reviewing
5. Binary assets changed
6. Scripts added or modified
7. Manual UE5 steps still required
8. Manual tests completed
9. Manual tests still pending
10. Known limitations
```

Also provide the output of:

```bash
git status
git log --oneline --decorate main..HEAD
git diff --stat main...HEAD
git lfs status
```
