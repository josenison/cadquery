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

    def center_of_mass(self) -> Vector:
        """Return the center of mass of the shape."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        com = props.CentreOfMass()
        return Vector(com.X(), com.Y(), com.Z())

    def __repr__(self) -> str:
        return f"<Shape: {type(self._shape).__name__}>"


class Solid(Shape):
    """Represents a solid 3D shape."""

    @classmethod
    def make_box(
        cls,
        length: float,
        width: float,
        height: float,
        origin: Optional[Vector] = None,
    ) -> "Solid":
        """Create a box solid with given dimensions.

        Args:
            length: Dimension along X axis.
            width: Dimension along Y axis.
            height: Dimension along Z axis.
            origin: Optional origin point (default is (0, 0, 0)).
        """
        if origin is None:
            pnt = gp_Pnt(0.0, 0.0, 0.0)
        else:
            pnt = gp_Pnt(origin.x, origin.y, origin.z)
        builder = BRepPrimAPI_MakeBox(pnt, length, width, height)
        return cls(builder.Shape())

    @classmethod
    def make_sphere(cls, radius: float, center: Optional[Vector] = None) -> "Solid":
        """Create a sphere solid.

        Args:
            radius: Radius of the sphere.
            center: Optional center point (default is (0, 0, 0)).
        """
        if center is None:
            builder = BRepPrimAPI_MakeSphere(radius)
        else:
            pnt = gp_Pnt(center.x, center.y, center.z)
            builder = BRepPrimAPI_MakeSphere(pnt, radius)
        return cls(builder.Shape())

    @classmethod
    def make_cylinder(
        cls,
        radius: float,
        height: float,
        origin: Optional[Vector] = None,
        direction: Optional[Vector] = None,
    ) -> "Solid":
        """Create a cylinder solid.

        Args:
            radius: Radius of the cylinder.
            height: Height of the cylinder.
            origin: Optional base center point (default is (0, 0, 0)).
            direction: Optional axis direction (default is Z axis).
        """
        if origin is None:
            pnt = gp_Pnt(0.0, 0.0, 0.0)
        else:
            pnt = gp_Pnt(origin.x, origin.y, origin.z)

        if direction is None:
            d = gp_Dir(0.0, 0.0, 1.0)
        else:
            d = gp_Dir(direction.x, direction.y, direction.z)

        axis = gp_Ax2(pnt, d)
        builder = BRepPrimAPI_MakeCylinder(axis, radius, height)
        return cls(builder.Shape())
