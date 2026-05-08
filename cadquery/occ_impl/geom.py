"""Geometry primitives and transformations for CadQuery.

This module provides Vector, Matrix, and Plane classes used throughout
CadQuery for geometric operations backed by OpenCASCADE Technology (OCCT).
"""

from typing import Optional, Tuple, Union, overload
import math

from OCC.Core.gp import (
    gp_Vec,
    gp_Pnt,
    gp_Dir,
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Trsf,
    gp_GTrsf,
    gp_XYZ,
)
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


class Vector:
    """A 3D vector with x, y, z components.

    Wraps gp_Vec from OCCT and provides convenient arithmetic operations.

    Examples::

        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        v3 = v1 + v2  # Vector(1, 1, 0)
    """

    def __init__(self, *args):
        if len(args) == 3:
            self._wrapped = gp_Vec(*args)
        elif len(args) == 1:
            if isinstance(args[0], gp_Vec):
                self._wrapped = args[0]
            elif isinstance(args[0], gp_Pnt):
                self._wrapped = gp_Vec(args[0].XYZ())
            elif isinstance(args[0], (list, tuple)) and len(args[0]) == 3:
                self._wrapped = gp_Vec(*args[0])
            else:
                raise TypeError(f"Cannot create Vector from {type(args[0])}")
        elif len(args) == 2:
            # 2-arg form: treat as (x, y) with z=0 — more intuitive for 2D work
            self._wrapped = gp_Vec(args[0], args[1], 0.0)
        else:
            raise TypeError(f"Expected 1, 2, or 3 arguments, got {len(args)}")

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def Length(self) -> float:
        """Return the magnitude of the vector."""
        return self._wrapped.Magnitude()

    def Normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._wrapped.Normalized())

    def Cross(self, other: "Vector") -> "Vector":
        """Return the cross product of this vector and another."""
        return Vector(self._wrapped.Crossed(other._wrapped))

    def Dot(self, other: "Vector") -> float:
        """Return the dot product of this vector and another."""
        return self._wrapped.Dot(other._wrapped)

    def sub(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def add(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def multiply(self, scale: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scale))

    def getAngle(self, other: "Vector") -> float:
        """Return the angle in radians between this vector and another."""
        return self._wrapped.Angle(other._wrapped)

    def toTuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def toPnt(self) -> gp_Pnt:
        return gp_Pnt(self._wrapped.XYZ())

    def toDir(self) -> gp_Dir:
        return gp_