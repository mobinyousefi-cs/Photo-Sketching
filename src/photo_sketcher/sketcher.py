#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Photo Sketching using Computer Vision
File: sketcher.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-11-10
Updated: 2025-11-10
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Core functionality for converting RGB/BGR images into pencil sketches using
OpenCV. Provides a configurable `SketchConfig` dataclass and helper functions
for reading and writing images.

Usage:
from pathlib import Path

from photo_sketcher import SketchConfig, read_image, to_pencil_sketch, save_image

config = SketchConfig(kernel_size=21, sigma=0.0, blend_scale=256.0)
image = read_image(Path("input.jpg"))
sketch = to_pencil_sketch(image, config)
save_image(sketch, Path("input_sketch.png"))

Notes:
- Uses a grayscale + inversion + Gaussian blur + color-dodge style blending
  pipeline implemented via `cv2.divide`.
- Designed to be deterministic and reproducible across runs for a fixed
  configuration.
=========================================================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


@dataclass
class SketchConfig:
    """Configuration parameters for the pencil sketch effect.

    Attributes
    ----------
    kernel_size:
        Size of the Gaussian blur kernel. Must be a positive odd integer.
    sigma:
        Standard deviation for the Gaussian kernel. If set to 0.0, OpenCV
        computes it from the kernel size.
    blend_scale:
        Scaling factor used in `cv2.divide` for the color-dodge style blending.
    """

    kernel_size: int = 21
    sigma: float = 0.0
    blend_scale: float = 256.0

    def __post_init__(self) -> None:
        if self.kernel_size <= 0 or self.kernel_size % 2 == 0:
            raise ValueError("kernel_size must be a positive odd integer.")
        if self.blend_scale <= 0:
            raise ValueError("blend_scale must be a positive value.")


def read_image(path: Path) -> np.ndarray:
    """Read an image from disk using OpenCV.

    Parameters
    ----------
    path:
        Path to the input image.

    Returns
    -------
    np.ndarray
        Image array in BGR color space.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If OpenCV fails to read the image.
    """

    if not path.is_file():
        raise FileNotFoundError(f"Input image not found: {path}")

    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Failed to read image: {path}")

    return image


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert an image to grayscale.

    Parameters
    ----------
    image:
        Input image in BGR or grayscale format.

    Returns
    -------
    np.ndarray
        Grayscale image with shape (H, W).
    """

    if image.ndim == 2:
        return image

    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    raise ValueError(
        "Unsupported image format: expected 2D grayscale or 3-channel BGR array."
    )


def to_pencil_sketch(
    image: np.ndarray, config: Optional[SketchConfig] = None
) -> np.ndarray:
    """Convert an image to a pencil sketch.

    Parameters
    ----------
    image:
        Input image as a NumPy array (BGR or grayscale).
    config:
        Optional :class:`SketchConfig` instance; if omitted, default
        configuration values are used.

    Returns
    -------
    np.ndarray
        A grayscale image representing the pencil sketch.
    """

    if config is None:
        config = SketchConfig()

    gray = to_grayscale(image)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(
        inverted, (config.kernel_size, config.kernel_size), config.sigma
    )

    # Color dodge-style blending using cv2.divide.
    sketch = cv2.divide(gray, 255 - blurred, scale=config.blend_scale)

    # Ensure uint8 output.
    if sketch.dtype != np.uint8:
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)

    return sketch


def save_image(image: np.ndarray, output_path: Path) -> None:
    """Save an image to disk.

    Parameters
    ----------
    image:
        Image array to save.
    output_path:
        Target file path. Parent directories are created if necessary.

    Raises
    ------
    ValueError
        If OpenCV fails to write the image.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = cv2.imwrite(str(output_path), image)
    if not success:
        raise ValueError(f"Failed to save image to: {output_path}")
