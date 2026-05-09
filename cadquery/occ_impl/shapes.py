"""Core shape classes wrapping OpenCASCADE topology.

This module provides Python wrappers around OCC topological shapes,
offering a more Pythonic interface for geometric operations.
"""

from typing import Optional, Tuple, List, Union
from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Compound,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakeCylinder,
)
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Cut,
    BRepAlgoAPI_Common,
)
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.GProp.GProp_GProps import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties

from .geom import Vector


class Shape:
    """Base class for all topological shapes."""

    def __init__(self, obj: TopoDS_Shape):
        self._shape = obj

    @property
    def wrapped(self) -> TopoDS_Shape:
        """Return the underlying OCC shape."""
        return self._shape

    def is_null(self) -> bool:
        """Return True if the shape is null."""
        return self._shape.IsNull()

    def bounding_box(self) -> Tuple[Vector, Vector]:
        """Return the axis-aligned bounding box as (min_corner, max_corner)."""
        bbox = Bnd_Box()
        brepbndlib_Add(self._shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return Vector(xmin, ymin, zmin), Vector(xmax, ymax, zmax)

    def bounding_box_size(self) -> Vector:
        """Return the size of the bounding box as a Vector (dx, dy, dz).

        Convenience method I added since I kept computing this manually.
        """
        min_pt, max_pt = self.bounding_box()
        return Vector(
            max_pt.x - min_pt.x,
            max_pt.y - min_pt.y,
            max_pt.z - min_pt.z,
        )

    def fuse(self, other: "Shape") -> "Shape":
        """Boolean union of this shape with another."""
        fuse_op = BRepAlgoAPI_Fuse(self._shape, other._shape)
        fuse_op.Build()
        return Shape(fuse_op.Shape())

    def cut(self, other: "Shape") -> "Shape":
        """Boolean subtraction of another shape from this one."""
        cut_op = BRepAlgoAPI_Cut(self._shape, other._shape)
        cut_op.Build()
        return Shape(cut_op.Shape())

    def intersect(self, other: "Shape") -> "Shape":
        """Boolean intersection of this shape with another."""
        common_op = BRepAlgoAPI_Common(self._shape, other._shape)
        common_op.Build()
        return Shape(common_op.Shape())

    def volume(self) -> float:
        """Compute and return the volume of the shape."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        return props.Mass()

    def area(self) -> float:
        """Compute and return the surface area of the shape."""
        props = GProp_GProps()
        brepgprop_SurfaceProperties(self._shape, props)
        return props.Mass()

    def __repr__(self) -> str:
        """Return a helpful string representation showing basic shape info.

        Added this because the default repr was useless during debugging sessions.
        """
        if self.is_null():
            return "Shape(null)"
        min_pt, max_pt = self.bounding_box()
        return (
            f"Shape(bbox=[({min_pt.x:.3f}, {min_pt.y:.3f}, {min_pt.z:.3f}), "
            f"({max_pt.x:.3f}, {max_pt.y:.3f}, {max_pt.z:.3f})])"
        )
