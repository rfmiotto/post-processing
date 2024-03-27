import hypothesis.extra.numpy as nps
import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from post_process.metrics import Metrics
from post_process.vector_operations import (
    ContravariantBaseComponents,
    Vectors,
    contravariant_from_cartesian,
    gradient_of_scalar,
)


class TestVector:
    float_values = st.floats(allow_infinity=False, allow_nan=False)

    shapes1D = nps.array_shapes(max_dims=1)
    array_of_floats = nps.arrays(dtype=float, shape=shapes1D, elements=float_values)

    shapes2D = nps.array_shapes(min_dims=2, max_dims=2)
    field_2D_of_floats = nps.arrays(dtype=float, shape=shapes2D, elements=float_values)

    args = st.one_of(float_values, array_of_floats, field_2D_of_floats)

    @given(args)
    def test_instantion_with_different_types(self, coordinate_value):
        component_x = coordinate_value
        component_y = coordinate_value
        Vectors(component_x, component_y)

    def test_instantiation_wrong_shape_raises_error(self):
        pass

    # def test_instantiation_raises_error_with_wrong_types(self, not_coordinate_values):
    #     ...


# class TestContravariantBaseComponents:
#     def test_instantion_with_different_types(self):
#         ...

#     def test_instantiation_raises_error_with_wrong_types(self):
#         ...


@pytest.mark.usefixtures("cartesian_mesh", "cylinder_mesh")
class TestGradient:
    @pytest.mark.parametrize("mesh", ["cartesian_mesh", "cylinder_mesh"])
    def test_gradient_of_uniform_field_is_zero(
        self, mesh, request: pytest.FixtureRequest
    ):
        mesh = request.getfixturevalue(mesh)
        x, y = mesh
        metrics = Metrics(x, y)
        basis = ContravariantBaseComponents(
            dAdx=metrics.dAdx,
            dAdy=metrics.dAdy,
            dBdx=metrics.dBdx,
            dBdy=metrics.dBdy,
        )
        uniform_scalar_field = np.ones_like(x)
        gradient = gradient_of_scalar(uniform_scalar_field, basis)
        all_zeros = not np.all(gradient)
        assert all_zeros

    def test_duck_typing_pass_metrics_instance_instead_of_basis(self, cartesian_mesh):
        x, y = cartesian_mesh
        metrics = Metrics(x, y)
        uniform_scalar_field = np.ones_like(x)
        gradient = gradient_of_scalar(uniform_scalar_field, metrics)
        all_zeros = not np.all(gradient)
        assert all_zeros

    def test_gradient_of_scalar(self, cartesian_mesh):
        x, y = cartesian_mesh
        metrics = Metrics(x, y)
        scalar_field = np.ones_like(x) * x
        gradient = gradient_of_scalar(scalar_field, metrics)

        np.testing.assert_array_equal(gradient[0], np.ones_like(x))
        np.testing.assert_array_equal(gradient[1], np.zeros_like(x))

    def test_gradient_of_scalar_2(self, cartesian_mesh):
        x, y = cartesian_mesh
        metrics = Metrics(x, y)
        scalar_field = np.ones_like(x) * y
        gradient = gradient_of_scalar(scalar_field, metrics)

        np.testing.assert_array_equal(gradient[0], np.zeros_like(x))
        np.testing.assert_array_equal(gradient[1], np.ones_like(x))


@pytest.mark.usefixtures("cartesian_mesh")
class TestCovariantFromCartesian:
    def test_contravariant_from_cartesian_for_a_single_vector(self, cartesian_mesh):
        x, y = cartesian_mesh
        metrics = Metrics(x, y)
        components_single_vector = Vectors(1.0, 1.0)
        indices_where_vector_is_applied = (5, 5)
        basis = ContravariantBaseComponents(
            dAdx=metrics.dAdx[indices_where_vector_is_applied],
            dAdy=metrics.dAdy[indices_where_vector_is_applied],
            dBdx=metrics.dBdx[indices_where_vector_is_applied],
            dBdy=metrics.dBdy[indices_where_vector_is_applied],
        )
        component1, component2 = contravariant_from_cartesian(
            vectors=components_single_vector, basis=basis
        )

        assert (
            component1 * metrics.h1[indices_where_vector_is_applied]
            == components_single_vector.component_x
        )
        assert (
            component2 * metrics.h2[indices_where_vector_is_applied]
            == components_single_vector.component_y
        )

    def test_contravariant_from_cartesian_for_an_array_of_vectors(self, cartesian_mesh):
        x, y = cartesian_mesh
        metrics = Metrics(x, y)

        array_vectors = Vectors(
            component_x=[1.0, 1.0, 1.0], component_y=[1.0, 1.0, 1.0]
        )

        # indices where vector is applied
        row_indices = [0, 1, 2]
        col_indices = [0, 0, 0]
        basis = ContravariantBaseComponents(
            dAdx=metrics.dAdx[(row_indices, col_indices)],
            dAdy=metrics.dAdy[(row_indices, col_indices)],
            dBdx=metrics.dBdx[(row_indices, col_indices)],
            dBdy=metrics.dBdy[(row_indices, col_indices)],
        )

        components1, components2 = contravariant_from_cartesian(
            vectors=array_vectors, basis=basis
        )

        np.testing.assert_array_equal(
            components1 * metrics.h1[(row_indices, col_indices)],
            array_vectors.component_x,
        )
        np.testing.assert_array_equal(
            components2 * metrics.h2[(row_indices, col_indices)],
            array_vectors.component_y,
        )

    def test_contravariant_from_cartesian_for_a_field_of_vectors(self, cartesian_mesh):
        x, y = cartesian_mesh
        metrics = Metrics(x, y)

        vector_field = Vectors(component_x=np.ones_like(x), component_y=np.ones_like(x))

        basis = ContravariantBaseComponents(
            dAdx=metrics.dAdx,
            dAdy=metrics.dAdy,
            dBdx=metrics.dBdx,
            dBdy=metrics.dBdy,
        )

        components1, components2 = contravariant_from_cartesian(
            vectors=vector_field, basis=basis
        )

        np.testing.assert_array_equal(
            components1 * metrics.h1, vector_field.component_x
        )
        np.testing.assert_array_equal(
            components2 * metrics.h2, vector_field.component_y
        )
