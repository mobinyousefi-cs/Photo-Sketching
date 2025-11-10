#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Photo Sketching using Computer Vision
File: test_sketcher.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-11-10
Updated: 2025-11-10
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Basic unit tests for the pencil sketch generation logic.

Usage:
pytest tests/test_sketcher.py

Notes:
- Uses a synthetic gradient image to verify shapes, dtypes, and that the
  output meaningfully differs from the input.
=========================================================================================================
"""

from __future__ import annotations

import numpy as np

from photo_sketcher.sketcher import SketchConfig, to_pencil_sketch


def _make_gradient_image(size: int = 64) -> np.ndarray:
    """Create a simple synthetic gradient image for testing.

    The output is a square BGR image where intensity increases horizontally.
    """

    row = np.linspace(0, 255, size, dtype=np.uint8)
    gray = np.tile(row, (size, 1))
    # Stack into BGR channels
    return np.stack([gray, gray, gray], axis=-1)


def test_to_pencil_sketch_shape_and_type() -> None:
    image = _make_gradient_image(size=64)
    config = SketchConfig(kernel_size=7, sigma=0.0, blend_scale=256.0)

    sketch = to_pencil_sketch(image, config)

    # Sketch must be 2D grayscale with same spatial dimensions.
    assert sketch.shape == image.shape[:2]
    assert sketch.dtype == np.uint8


def test_to_pencil_sketch_differs_from_input() -> None:
    image = _make_gradient_image(size=64)
    config = SketchConfig(kernel_size=7, sigma=0.0, blend_scale=256.0)

    sketch = to_pencil_sketch(image, config)

    # The sketch should not be identical to the original grayscale values.
    gray = image[..., 0]
    assert not np.array_equal(sketch, gray)


def test_invalid_kernel_size_raises() -> None:
    image = _make_gradient_image(size=32)

    # Even kernel size should raise a ValueError
    config = SketchConfig(kernel_size=5, sigma=0.0, blend_scale=256.0)
    _ = to_pencil_sketch(image, config)  # Should work

    try:
        _ = SketchConfig(kernel_size=4, sigma=0.0, blend_scale=256.0)
    except ValueError:
        # Expected path
        return

    raise AssertionError("Expected ValueError for even kernel_size, but none was raised.")
