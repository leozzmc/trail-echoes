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