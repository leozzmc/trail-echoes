# ADR-0001: Use Unreal Engine 5 for Trail Echoes

## Status

Accepted

## Context

Trail Echoes is a first-person 3D mountain exploration RPG prototype.

The first vertical slice is based on Hehuan East Peak and requires:

- First-person movement
- DEM-based mountain terrain
- Landscape Heightmap import
- Volumetric Fog
- Environmental storytelling
- Blueprint-first rapid iteration

## Decision

Use Unreal Engine 5 with Blueprint-first development.

Initial development environment:

- Unreal Engine 5.7.x
- macOS development on Apple Silicon
- Windows PC as the intended release target

Initial prototype route:

- Hehuan East Peak

## Rationale

Unreal Engine 5 provides:

- First Person Template
- Landscape tools
- Heightmap import
- Volumetric Fog
- Post Process Volume
- Blueprint scripting
- A suitable foundation for atmospheric 3D environments

## Rejected Alternatives

### Godot

Rejected because the MVP prioritizes 3D Landscape tooling, atmospheric rendering, and rapid first-person environment prototyping.

### Unity

Rejected because Unreal Engine provides a more direct workflow for Landscape-based terrain and atmospheric effects for this prototype.

### 2D / 2.5D implementation

Rejected because the prototype specifically aims to validate first-person immersion while walking through a Taiwanese mountain environment.

## Consequences

- Unreal binary assets must be managed with Git LFS.
- Blueprint assets are binary and cannot be reviewed through standard text diffs.
- macOS is suitable for development and editor testing.
- Windows packaging and performance validation will require a Windows environment later.