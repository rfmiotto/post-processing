from typing import Tuple

import numpy as np
import pytest

from post_process.metrics import Metrics
from post_process.my_types import Array2D


@pytest.mark.parametrize(
    ["x", "y"],
    [
        ["not an array", "also not an array"],
        ["not an array", np.array([1, 2, 3])],
        [np.array([1, 2, 3]), "not an array"],
        [np.array([1, 2, 3]), np.array([1, 2, 3])],  # not 2D arrays
        [np.array([[1, 2], [1, 2]]), np.array([[1, 2], [1, 2]])],  # not float
    ],
)
def test_error_if_inputs_are_not_numpy_arrays_of_floats(x, y) -> None:
    with pytest.raises(TypeError):
        Metrics(x, y)


@pytest.fixture
def cylinder_mesh(request) -> Tuple[Array2D, Array2D]:
    init_radius = 0.1
    final_radius = 1.0
    num_points_r = 4
    num_points_theta = 6

    radius = np.linspace(init_radius, final_radius, num=num_points_r)
    if request.param:  # clockwise
        theta = np.linspace(0, 2 * np.pi, num=num_points_theta)
    else:  # counterclockwise
        theta = np.linspace(2 * np.pi, 0, num=num_points_theta)

    r_matrix, theta_matrix = np.meshgrid(radius, theta)

    x_coords_matrix = r_matrix * np.cos(theta_matrix)
    y_coords_matrix = r_matrix * np.sin(theta_matrix)

    return x_coords_matrix, y_coords_matrix


@pytest.mark.parametrize("cylinder_mesh", [True], indirect=True)
def test_mesh_is_clockwise(cylinder_mesh):
    metrics = Metrics(*cylinder_mesh)
    assert metrics.orientation == "clockwise"


@pytest.mark.parametrize("cylinder_mesh", [False], indirect=True)
def test_mesh_is_counterclockwise(cylinder_mesh):
    metrics = Metrics(*cylinder_mesh)
    assert metrics.orientation == "counterclockwise"


@pytest.mark.parametrize("cylinder_mesh", [True], indirect=True)
def test_dx_alias(cylinder_mesh):
    metrics = Metrics(*cylinder_mesh)
    assert isinstance(metrics.dx, Array2D)


@pytest.mark.parametrize("cylinder_mesh", [True], indirect=True)
def test_dy_alias(cylinder_mesh):
    metrics = Metrics(*cylinder_mesh)
    assert isinstance(metrics.dy, Array2D)
