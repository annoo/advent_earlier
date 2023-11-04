import pytest

from solution_template import solve_part1


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ("example_input1", "expected_output1"),
        ("example_input2", "expected_output2"),
        # ... more test cases
    ],
)
def test_solve_part1(input_data, expected_output):
    assert solve_part1(input_data) == expected_output


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ("example_input1", "expected_output1"),
        ("example_input2", "expected_output2"),
        # ... more test cases
    ],
)
def test_solve_part2(input_data, expected_output):
    assert solve_part2(input_data) == expected_output
