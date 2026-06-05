# GIS Data

## Hehuan East Peak DEM

### Purpose

Provide the terrain baseline for the Hehuan East Peak Greybox prototype.

The processed DEM will be used to generate a UE5 Landscape Heightmap.

### Primary Dataset

- Dataset: 2025 Taiwan 20 m Grid Digital Terrain Model
- Provider: Department of Land Administration, Ministry of the Interior
- Resolution: 20 m
- Coordinate system: TWD97
- License: Government Open Data License, Version 1.0
- Dataset page: recorded in `data/metadata/source-registry.csv`

### Downloaded Packages

- Nantou County 20 m DTM
- Hualien County 20 m DTM
- DTM schema and header definition

### Why Two County Packages Are Required

Hehuan East Peak is located near the Nantou County and Hualien County boundary.

Both packages are downloaded locally to ensure that DEM cropping does not remove terrain on the eastern side of the trail.

### Local File Policy

Raw downloaded DEM packages and extracted files are stored locally under:

`data/gis/local/`

They are not committed to the repository.

Processed outputs intended for UE5 may be committed later under:

`data/gis/processed/`

### Next Step

Use QGIS to:

1. Load the local Hikingbook GPX reference.
2. Inspect the downloaded DEM files.
3. Confirm the coordinate reference system.
4. Select the tiles covering the Hehuan East Peak route.
5. Merge the required tiles if necessary.
6. Create a buffer around the GPX route.
7. Crop the DEM for Heightmap generation.