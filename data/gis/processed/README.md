## Processing Notes

The raw XYZ `.grd` tiles were normalized into north-up GeoTIFF files
before VRT generation.

The initial normalization workflow used `gdalwarp -tap`, which introduced
extra aligned boundary pixels and visible horizontal seam artifacts.

The final workflow removes `-tap` and explicitly sets:

- GeoTIFF NoData value: `-9999`
- VRT source NoData value: `-9999`
- VRT output NoData value: `-9999`

Three irregular Hualien XYZ tiles were skipped because they are not
compatible with GDAL's regular XYZ raster driver:

- `97213009dem.grd`
- `97204074dem.grd`
- `97213018dem.grd`

These tiles are outside the Hehuan East Peak prototype area and do not
block the current Greybox.

## UE5 Heightmap Export

The cropped Float32 GeoTIFF is padded to a square extent before being
resampled to a UE5-recommended Landscape resolution.

### Output

- `hehuan-east-peak-heightmap-253.png`
- `hehuan-east-peak-heightmap-253-metadata.md`

### Heightmap Properties

| Property | Value |
|---|---|
| Format | 16-bit grayscale PNG |
| Resolution | 253 x 253 |
| Source CRS | EPSG:3826 |
| Source DEM resolution | 20 m |
| Square terrain span | 3560 m x 3560 m |
| Elevation range | 2454.664 m to 3417.594 m |
| UE5 target | Landscape import |

### Recommended UE5 Landscape Import Parameters

| Parameter | Value |
|---|---:|
| X Scale | 1412.698 cm |
| Y Scale | 1412.698 cm |
| Z Scale | 188.072 |

The source DEM is padded to a square extent before resampling to avoid
distorting the X/Y proportions.