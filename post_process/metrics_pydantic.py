"""
Metrics

This script defines a Metrics class that pre-computes and stores the metric
terms given the x- and y-coordinates (Cartesian).

The script requires `numpy` to be installed within the Python environment.
"""

# pylint: disable=invalid-name

from dataclasses import field
from typing import Literal

import numpy as np
from pydantic.dataclasses import dataclass

from post_process.my_types import Array2D


@dataclass
class Metrics:
    """
    Metric terms

    Definitions:
    x, y -> Cartesian coordinates
    A, B -> Curvilinear coordinates
    """

    # pylint: disable=too-many-instance-attributes

    x: Array2D
    y: Array2D

    normal_x: Array2D = field(init=False)
    normal_y: Array2D = field(init=False)

    dAdx: Array2D = field(init=False)
    dBdx: Array2D = field(init=False)
    dAdy: Array2D = field(init=False)
    dBdy: Array2D = field(init=False)

    dxdA: Array2D = field(init=False)
    dxdB: Array2D = field(init=False)
    dydA: Array2D = field(init=False)
    dydB: Array2D = field(init=False)

    # scale factors
    h1: Array2D = field(init=False)
    h2: Array2D = field(init=False)

    jacobian: Array2D = field(init=False)

    orientation: Literal["clockwise", "counterclockwise"] = field(init=False)

    def __post_init__(self) -> None:
        # if type(self.x) != np.ndarray or type(self.y) != np.ndarray:
        # if not isinstance(self.x, Array2D) or not isinstance(self.y, Array2D):
        #     raise TypeError("`x` and `y` must be numpy arrays")

        # if np.isnan(np.sum(self.x)) or np.isnan(np.sum(self.y)):
        #     raise ValueError("NaN appeared in coordinate values")

        # if self.x.shape != self.y.shape:
        #     raise ValueError("x- and y-coordinates must have the same shape")

        self.dxdA, self.dxdB = np.gradient(self.x, edge_order=2)
        self.dydA, self.dydB = np.gradient(self.y, edge_order=2)

        self.jacobian = -self.dxdB * self.dydA + self.dxdA * self.dydB

        self.dAdx = self.dydB / self.jacobian
        self.dAdy = -self.dxdB / self.jacobian
        self.dBdx = -self.dydA / self.jacobian
        self.dBdy = self.dxdA / self.jacobian

        self.h1 = np.sqrt(self.dxdA**2 + self.dydA**2)
        self.h2 = np.sqrt(self.dxdB**2 + self.dydB**2)

        is_grid_counterclockwise = max(self.jacobian[0]) > 0
        if is_grid_counterclockwise:
            self.normal_x = -self.dydA
            self.normal_y = self.dxdA
            self.orientation = "counterclockwise"
        else:
            self.normal_x = self.dydA
            self.normal_y = -self.dxdA
            self.orientation = "clockwise"

    @property
    def dx(self):
        """Alias for dx"""
        return self.dxdA

    @property
    def dy(self):
        """Alias for dy"""
        return self.dydA
