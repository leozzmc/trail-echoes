#!/usr/bin/env python3
"""
Import QGIS-generated GPX guide points into an Unreal Engine Spline Component.

Run this script inside the Unreal Editor Python environment:

    py "/Users/kuangsin/trail-echoes/tools/unreal/import_gpx_guide_spline.py"

Expected setup in the current Unreal level:
- A Landscape actor labeled: Landscape
- An Actor labeled: GPXTrailGuide
- GPXTrailGuide contains a Spline Component
"""

from __future__ import annotations

import csv
from pathlib import Path

import unreal


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GUIDE_ACTOR_LABEL = "GPXTrailGuide"
LANDSCAPE_ACTOR_LABEL = "Landscape"

# EPSG:3826 square extent used when exporting the UE5 heightmap.
GIS_X_MIN = 277070.0
GIS_Y_MIN = 2668570.0
GIS_X_MAX = 280630.0
GIS_Y_MAX = 2672130.0

# The GIS raster is north-up. Keep this enabled initially.
# Toggle to False only if the imported guide appears mirrored vertically.
FLIP_Y = True

# Keep the guide slightly above the terrain to prevent z-fighting.
GUIDE_Z_OFFSET_CM = 120.0

# Raycast margin above and below the imported Landscape.
TRACE_MARGIN_CM = 50000.0

# Unreal HitResult tuple indexes. The order follows Unreal's HitResult struct
# constructor order:
# 0 blocking_hit
# 1 initial_overlap
# 2 time
# 3 distance
# 4 location
# 5 impact_point
HIT_RESULT_LOCATION_INDEX = 4
HIT_RESULT_IMPACT_POINT_INDEX = 5


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def log(message: str) -> None:
    unreal.log(f"[GPXTrailGuide] {message}")


def fail(message: str) -> None:
    raise RuntimeError(f"[GPXTrailGuide] {message}")


def get_editor_world() -> unreal.World:
    subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = subsystem.get_editor_world()

    if world is None:
        fail("Unable to access the current Unreal Editor world")

    return world


def find_actor_by_label(label: str) -> unreal.Actor:
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    for actor in subsystem.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor

    fail(f"Actor not found in current level: {label}")


def get_actor_bounds(actor: unreal.Actor) -> tuple[unreal.Vector, unreal.Vector]:
    try:
        origin, extent = actor.get_actor_bounds(
            only_colliding_components=False,
            include_from_child_actors=False,
        )
    except TypeError:
        origin, extent = actor.get_actor_bounds(False)

    return origin, extent


def get_route_csv_path() -> Path:
    project_dir = Path(unreal.Paths.project_dir()).resolve()

    # Unreal project path: <repo>/game/TrailEchoes/
    repo_root = project_dir.parent.parent

    csv_path = (
        repo_root
        / "data"
        / "gis"
        / "local"
        / "qgis"
        / "hehuan-east-peak-route-points-30m.csv"
    )

    if not csv_path.exists():
        fail(f"CSV not found: {csv_path}")

    return csv_path


def read_route_points(csv_path: Path) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        required_fields = {"x", "y"}
        actual_fields = set(reader.fieldnames or [])

        if not required_fields.issubset(actual_fields):
            fail(
                "CSV must contain x and y columns. "
                f"Found: {sorted(actual_fields)}"
            )

        for row in reader:
            points.append((float(row["x"]), float(row["y"])))

    if len(points) < 2:
        fail("At least two route points are required")

    return points


def map_gis_to_unreal_xy(
    gis_x: float,
    gis_y: float,
    landscape_origin: unreal.Vector,
    landscape_extent: unreal.Vector,
) -> tuple[float, float]:
    u = (gis_x - GIS_X_MIN) / (GIS_X_MAX - GIS_X_MIN)
    v = (gis_y - GIS_Y_MIN) / (GIS_Y_MAX - GIS_Y_MIN)

    if not (0.0 <= u <= 1.0 and 0.0 <= v <= 1.0):
        fail(
            "GIS point outside heightmap extent: "
            f"x={gis_x}, y={gis_y}, u={u:.4f}, v={v:.4f}"
        )

    unreal_x_min = landscape_origin.x - landscape_extent.x
    unreal_x_max = landscape_origin.x + landscape_extent.x
    unreal_y_min = landscape_origin.y - landscape_extent.y
    unreal_y_max = landscape_origin.y + landscape_extent.y

    unreal_x = unreal_x_min + u * (unreal_x_max - unreal_x_min)

    if FLIP_Y:
        unreal_y = unreal_y_max - v * (unreal_y_max - unreal_y_min)
    else:
        unreal_y = unreal_y_min + v * (unreal_y_max - unreal_y_min)

    return unreal_x, unreal_y


def vector_from_hit_value(value: object, field_name: str) -> unreal.Vector:
    """
    Convert a HitResult tuple value into an Unreal Vector.

    In normal UE Python output this value is already unreal.Vector.
    Tuple/list handling is retained as a defensive fallback.
    """
    if isinstance(value, unreal.Vector):
        return value

    if isinstance(value, (tuple, list)) and len(value) >= 3:
        return unreal.Vector(float(value[0]), float(value[1]), float(value[2]))

    fail(
        f"HitResult {field_name} has an unexpected value: {value!r} "
        f"(type={type(value)!r})"
    )


def extract_hit_location(hit_result: unreal.HitResult) -> unreal.Vector:
    """
    Read the impact point from Unreal's HitResult wrapper.

    In UE 5.7 the generated Python wrapper may expose only StructBase helpers
    such as to_tuple(), while direct properties and get_editor_property()
    access are unavailable. Use the documented HitResult field order:
    location is index 4 and impact_point is index 5.
    """
    try:
        values = hit_result.to_tuple()
    except Exception as error:
        fail(f"Unable to convert HitResult to tuple: {error}")

    if len(values) <= HIT_RESULT_IMPACT_POINT_INDEX:
        fail(
            "HitResult tuple is shorter than expected: "
            f"length={len(values)}, values={values!r}"
        )

    try:
        return vector_from_hit_value(
            values[HIT_RESULT_IMPACT_POINT_INDEX],
            "impact_point",
        )
    except RuntimeError:
        # For a vertical Landscape raycast, location is also a suitable
        # fallback when impact_point cannot be decoded.
        return vector_from_hit_value(
            values[HIT_RESULT_LOCATION_INDEX],
            "location",
        )


def trace_landscape_z(
    world_context: unreal.Object,
    unreal_x: float,
    unreal_y: float,
    landscape_origin: unreal.Vector,
    landscape_extent: unreal.Vector,
) -> float:
    start = unreal.Vector(
        unreal_x,
        unreal_y,
        landscape_origin.z + landscape_extent.z + TRACE_MARGIN_CM,
    )

    end = unreal.Vector(
        unreal_x,
        unreal_y,
        landscape_origin.z - landscape_extent.z - TRACE_MARGIN_CM,
    )

    result = unreal.SystemLibrary.line_trace_single(
        world_context,
        start,
        end,
        unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
        False,
        [],
        unreal.DrawDebugTrace.NONE,
        False,
        unreal.LinearColor.RED,
        unreal.LinearColor.GREEN,
        0.0,
    )

    # Current wrappers normally return HitResult or None.
    # Retain tuple support for compatibility with older wrapper behavior.
    if result is None:
        fail(
            "Landscape trace missed at UE coordinates: "
            f"x={unreal_x:.3f}, y={unreal_y:.3f}"
        )

    if isinstance(result, tuple):
        if len(result) != 2:
            fail(f"Unexpected line trace tuple: {result!r}")

        hit_success, hit_result = result

        if not hit_success or hit_result is None:
            fail(
                "Landscape trace missed at UE coordinates: "
                f"x={unreal_x:.3f}, y={unreal_y:.3f}"
            )
    else:
        hit_result = result

    hit_location = extract_hit_location(hit_result)

    return float(hit_location.z)


def get_spline_component(actor: unreal.Actor) -> unreal.SplineComponent:
    components = actor.get_components_by_class(unreal.SplineComponent)

    if not components:
        fail(
            f"Actor {GUIDE_ACTOR_LABEL} does not contain a Spline Component"
        )

    return components[0]


def try_enable_spline_debug_draw(spline: unreal.SplineComponent) -> None:
    """
    Enable editor debug rendering when supported by the current wrapper.
    The guide still imports successfully if this optional property is absent.
    """
    try:
        spline.set_editor_property("draw_debug", True)
    except Exception as error:
        log(f"Optional draw_debug property was not applied: {error}")


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

def main() -> None:
    csv_path = get_route_csv_path()

    editor_world = get_editor_world()
    landscape = find_actor_by_label(LANDSCAPE_ACTOR_LABEL)
    guide_actor = find_actor_by_label(GUIDE_ACTOR_LABEL)
    spline = get_spline_component(guide_actor)

    landscape_origin, landscape_extent = get_actor_bounds(landscape)
    route_points = read_route_points(csv_path)

    log(f"CSV: {csv_path}")
    log(f"Route points: {len(route_points)}")
    log(
        "Landscape bounds: "
        f"origin=({landscape_origin.x:.3f}, "
        f"{landscape_origin.y:.3f}, "
        f"{landscape_origin.z:.3f}), "
        f"extent=({landscape_extent.x:.3f}, "
        f"{landscape_extent.y:.3f}, "
        f"{landscape_extent.z:.3f})"
    )

    guide_actor.modify()
    spline.modify()

    spline.clear_spline_points(update_spline=False)
    spline.set_closed_loop(False, update_spline=False)

    for gis_x, gis_y in route_points:
        unreal_x, unreal_y = map_gis_to_unreal_xy(
            gis_x,
            gis_y,
            landscape_origin,
            landscape_extent,
        )

        unreal_z = trace_landscape_z(
            editor_world,
            unreal_x,
            unreal_y,
            landscape_origin,
            landscape_extent,
        )

        spline.add_spline_point(
            unreal.Vector(
                unreal_x,
                unreal_y,
                unreal_z + GUIDE_Z_OFFSET_CM,
            ),
            unreal.SplineCoordinateSpace.WORLD,
            update_spline=False,
        )

    spline.update_spline()
    try_enable_spline_debug_draw(spline)

    log(f"Imported {len(route_points)} spline points")
    log("Select GPXTrailGuide in the Outliner and press F to inspect the route")
    log("Use File -> Save All after visual verification")


if __name__ == "__main__":
    main()
