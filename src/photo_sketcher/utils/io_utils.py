#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Photo Sketching using Computer Vision
File: io_utils.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-11-10
Updated: 2025-11-10
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Helper utilities for discovering image files on disk and constructing output
paths for generated sketches.

Usage:
from pathlib import Path

from photo_sketcher.utils import discover_images, derive_output_path

images = discover_images(Path("./inputs"), recursive=True)
for img_path in images:
    out_path = derive_output_path(img_path, Path("./outputs"))

Notes:
- Centralizes filesystem-related logic away from the core sketching code.
=========================================================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp")


def discover_images(input_dir: Path, recursive: bool = True) -> List[Path]:
    """Discover image files in a directory.

    Parameters
    ----------
    input_dir:
        Directory to scan for image files.
    recursive:
        If ``True``, search subdirectories recursively.

    Returns
    -------
    list of Path
        Sorted list of image paths.
    """

    if not input_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {input_dir}")

    if recursive:
        candidates: Iterable[Path] = input_dir.rglob("*")
    else:
        candidates = input_dir.iterdir()

    images = [
        p
        for p in candidates
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    return sorted(images)


def derive_output_path(input_path: Path, output_dir: Path, suffix: str = "_sketch") -> Path:
    """Construct an output path for a sketch given an input image.

    Parameters
    ----------
    input_path:
        Path to the original image.
    output_dir:
        Root directory where the sketch should be saved.
    suffix:
        Suffix to append to the original stem before the file extension.

    Returns
    -------
    Path
        Target path for the sketch image.
    """

    output_dir = output_dir.resolve()
    stem = f"{input_path.stem}{suffix}"
    return output_dir / f"{stem}{input_path.suffix}"
