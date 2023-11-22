"""
Metrics

This script defines a Metrics class that pre-computes and stores the metric
terms given the x- and y-coordinates (Cartesian).

The script requires `numpy` to be installed within the Python environment.
"""

# pylint: disable=invalid-name

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from nptyping import Float, NDArray, Shape

ArrayMxN = NDArray[Shape["*, *"], Float]


@dataclass
class Metrics:
    """
    Metric terms

    Definitions:
    x, y -> Cartesian coordinates
    A, B -> Curvilinear coordinates
    """

    # pylint: disable=too-many-instance-attributes

    x: ArrayMxN
    y: ArrayMxN

    normal_x: ArrayMxN = field(init=False)
    normal_y: ArrayMxN = field(init=False)

    dAdx: ArrayMxN = field(init=False)
    dBdx: ArrayMxN = field(init=False)
    dAdy: ArrayMxN = field(init=False)
    dBdy: ArrayMxN = field(init=False)

    dxdA: ArrayMxN = field(init=False)
    dxdB: ArrayMxN = field(init=False)
    dydA: ArrayMxN = field(init=False)
    dydB: ArrayMxN = field(init=False)

    # scale factors
    h1: ArrayMxN = field(init=False)
    h2: ArrayMxN = field(init=False)

    jacobian: ArrayMxN = field(init=False)

    orientation: Literal["clockwise", "counterclockwise"] = field(init=False)

    def __post_init__(self) -> None:
        # if type(self.x) != np.ndarray or type(self.y) != np.ndarray:
        if not isinstance(self.x, ArrayMxN) or not isinstance(self.y, ArrayMxN):
            raise TypeError("`x` and `y` must be numpy arrays")

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
