"""Per-column correction of bubble positions (bent / distorted scans)."""
import numpy as np
import pytest

from omr_app.pipeline import Grader


@pytest.fixture(scope="module")
def aligner():
    return Grader().aligner


def _grid(aligner):
    keys = [(b.question, b.option) for b in aligner.layout.bubbles]
    fitted = np.float32([b.center for b in aligner.layout.bubbles])
    return keys, fitted


def test_shifted_column_is_followed_including_filled_bubbles(aligner):
    keys, fitted = _grid(aligner)
    meas = fitted.copy()
    good = np.ones(len(keys), bool)
    col_d = np.array([k[1] == "D" for k in keys])
    meas[col_d] += (8.0, -3.0)  # the whole printed D column sits 8 px right, 3 px up
    filled = np.array([k in {(2, "D"), (5, "D")} for k in keys])
    good[filled] = False  # filled bubbles cannot be template-matched
    info = {}
    out = aligner._column_correction(keys, fitted, meas, good, info)
    assert np.allclose(out[col_d] - fitted[col_d], (8.0, -3.0), atol=0.01)  # incl. the two filled ones
    assert np.allclose(out[~col_d], fitted[~col_d])  # other columns untouched
    assert "D" in info["column_shift_px"] and len(info["column_shift_px"]) == 1


def test_gradual_drift_along_column(aligner):
    keys, fitted = _grid(aligner)
    meas = fitted.copy()
    good = np.ones(len(keys), bool)
    col_a = np.array([k[1] == "A" for k in keys])
    y = fitted[col_a, 1]
    meas[col_a, 1] += (y - y.mean()) * 0.025  # column slightly stretched (phone photo of a bent page)
    out = aligner._column_correction(keys, fitted, meas, good, {})
    assert np.abs(out[col_a] - meas[col_a]).max() < 0.05


def test_implausible_shift_is_ignored(aligner):
    keys, fitted = _grid(aligner)
    meas = fitted.copy()
    col_b = np.array([k[1] == "B" for k in keys])
    meas[col_b, 1] += 60.0  # matched the neighbouring row's 'O' -> not a distortion
    info = {}
    out = aligner._column_correction(keys, fitted, meas, np.ones(len(keys), bool), info)
    assert np.allclose(out, fitted)
    assert "column_shift_px" not in info


def test_inconsistent_column_is_left_alone(aligner):
    keys, fitted = _grid(aligner)
    meas = fitted.copy()
    col_c = np.where([k[1] == "C" for k in keys])[0]
    rng = np.random.default_rng(0)
    meas[col_c] += rng.uniform(-10, 10, size=(len(col_c), 2))  # random noise, no common offset
    out = aligner._column_correction(keys, fitted, meas, np.ones(len(keys), bool), {})
    assert np.allclose(out, fitted)
