from typing import Tuple

import numpy as np
import pytest

from post_process.my_types import Array2D


@pytest.fixture(name="cartesian_mesh", scope="session")
def fixture_cartesian_mesh() -> Tuple[Array2D, Array2D]:
    init_position = 0.0
    final_position = 1.0
    num_points = 9

    spacing = np.linspace(init_position, final_position, num=num_points)

    x_coords_matrix, y_coords_matrix = np.meshgrid(spacing, spacing)

    return x_coords_matrix, y_coords_matrix


@pytest.fixture(name="cylinder_mesh", scope="session")
def fixture_cylinder_mesh() -> Tuple[Array2D, Array2D]:
    init_radius = 0.1
    final_radius = 1.0
    num_points_r = 4
    num_points_theta = 6

    radius = np.linspace(init_radius, final_radius, num=num_points_r)
    theta = np.linspace(0, 2 * np.pi, num=num_points_theta)

    r_matrix, theta_matrix = np.meshgrid(radius, theta)

    x_coords_matrix = r_matrix * np.cos(theta_matrix)
    y_coords_matrix = r_matrix * np.sin(theta_matrix)

    return x_coords_matrix, y_coords_matrix
