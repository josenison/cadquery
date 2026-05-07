"""CadQuery - A parametric 3D CAD scripting framework built on top of Open CASCADE Technology (OCCT).

CadQuery is an intuitive, easy-to-use Python module for building parametric 3D CAD models.
It is inspired by OpenSCAD, but uses a fluent API that allows users to describe their models
in a way that is easy to read and understand.

Basic usage::

    import cadquery as cq

    result = (
        cq.Workplane("XY")
        .box(10, 10, 5)
        .faces(">Z")
        .hole(3)
    )

Personal fork notes:
    - Tracking upstream: CadQuery/cadquery
    - Added __version_info__ tuple for easier programmatic version comparisons
    - Added __author_email__ for completeness
    - Added __description__ for convenience (e.g. useful when introspecting the module)
    - Added __url__ pointing to the upstream docs
    - See also: https://cadquery.readthedocs.io
"""

from .cq import CQ, Workplane
from .occ_impl.geom import Vector, Matrix, Plane, BoundBox
from .occ_impl.shapes import (
    Shape,
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Compound,
)
from .assembly import Assembly, ConstraintKind
from .selectors import (
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    RadiusNthSelector,
    CenterNthSelector,
    LengthNthSelector,
    AreaNthSelector,
    BinarySelector,
    AndSelector,
    SumSelector,
    SubtractSelector,
    InverseSelector,
    StringSyntaxSelector,
)
from .sketch import Sketch
from . import exporters
from . import importers

__version__ = "2.4.0"
__version_info__ = tuple(int(x) for x in __version__.split("."))  # e.g. (2, 4, 0)
__author__ = "CadQuery Contributors"
__author_email__ = "cadquery@cadquery.readthedocs.io"  # added for completeness
__license__ = "Apache License 2.0"
__description__ = "A parametric 3D CAD scripting framework built on top of OCCT"  # handy for quick introspection
__url__ = "https://cadquery.readthedocs.io"  # upstream docs URL, useful for tooling/IDEs

__all__ = [
    # Core workplane
    "CQ",
    "Workplane",
    # Geometry primitives
    "Vector",
    "Matrix",
    "Plane",
    "BoundBox",
    # Topology
    "Shape",
    "Vertex",
    "Edge",
    "Wire",
    "Face",
    "Shell",
    "Solid",
    "Compound",
    # Assembly
    "Assembly",
    "ConstraintKind",
    # Selectors
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "RadiusNthSelector",
    "CenterNthSelector",
    "LengthNthSelector",
    "AreaNthSelector",
    "BinarySelector",
    "AndSelector",
    "SumSelector",
    "SubtractSelector",
    "InverseSelector",
    "StringSyntaxSelector",
    # Sketch
    "Sketch",
    # I/O modules
    "exporters",
    "importers",
    # Version info
    "__version__",
    "__version_info__",
    "__description__",
    "__url__",
]
