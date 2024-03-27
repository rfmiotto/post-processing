# pylint: disable=invalid-name

from dataclasses import dataclass
from typing import Tuple, Union

import numpy as np

from post_process.my_types import Array1D, Array2D

# TODO: Colocar checagem se os argumentos tem mesmas dimensoes sao iguais e os testes pra isso.

# Allowed types are: a scalar, a vector of scalars or a 2D scalar field
DataType = Union[float, Array1D, Array2D]


@dataclass
class ContravariantBaseComponents:
    """
    Components of the contravariant base vectors.
    It stores float values for single point, an array of points, of a 2D field
    of points.
    """

    dAdx: DataType
    dAdy: DataType
    dBdx: DataType
    dBdy: DataType


@dataclass
class Vectors:
    """
    Components of vectors.
    It stores float values for single point, an array of points, of a 2D field
    of points.
    """
    component_x: DataType
    component_y: DataType

    def __post_init__(self) -> None:
        if isinstance(self.component_x, )
        assert self.component_x.shape == self.component_y.shape, "Shape must match"


def contravariant_from_cartesian(
    vectors: Vectors, basis: ContravariantBaseComponents
) -> Tuple[DataType, DataType]:
    """
    Compute the contravariant components of a Cartesian vector.
    """
    component_1 = vectors.component_x * basis.dAdx + vectors.component_y * basis.dAdy
    component_2 = vectors.component_x * basis.dBdx + vectors.component_y * basis.dBdy

    return component_1, component_2


def gradient_of_scalar(
    scalar: DataType, basis: ContravariantBaseComponents
) -> Tuple[DataType, DataType]:
    """
    Compute the gradient vector from a scalar.
    """
    dsdA, dsdB = np.gradient(scalar, edge_order=2)

    dsdx = dsdA * basis.dAdx + dsdB * basis.dBdx
    dsdy = dsdA * basis.dAdy + dsdB * basis.dBdy

    return dsdx, dsdy
