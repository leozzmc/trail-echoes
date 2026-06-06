# Hehuan East Peak UE5 Heightmap Metadata

## Output

`hehuan-east-peak-heightmap-253.png`

## Format

- Bit depth: 16-bit grayscale
- Resolution: 253 x 253
- Source CRS: EPSG:3826 - TWD97 / TM2 zone 121
- Source DEM resolution: 20 m
- Square terrain span: 3560.000 m
- Source elevation minimum: 2454.664 m
- Source elevation maximum: 3417.594 m
- Elevation range: 962.930 m

## Recommended UE5 Landscape Import Parameters

| Parameter | Value |
|---|---:|
| Heightmap resolution | 253 x 253 |
| X Scale | 1412.698 cm |
| Y Scale | 1412.698 cm |
| Z Scale | 188.072 |
| Optional Landscape Location Z | 293612.900 cm |

## Notes

The PNG maps the minimum source elevation to `0` and the maximum source
elevation to `65535`.

The source DEM is padded to a square extent before resampling to avoid
distorting the X/Y proportions.

For the first Greybox, the optional Landscape Location Z offset is not
required. Use it only if absolute elevation alignment is needed later.
