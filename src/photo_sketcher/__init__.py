#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Photo Sketching using Computer Vision
File: __init__.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-11-10
Updated: 2025-11-10
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Package initializer for the `photo_sketcher` library. Exposes the main public
API for generating pencil sketches from images.

Usage:
from photo_sketcher import SketchConfig, read_image, to_pencil_sketch, save_image

Notes:
- All heavy lifting is implemented in `sketcher.py`.
- This file simply re-exports the public functions and classes.
=========================================================================================================
"""

from __future__ import annotations

from .sketcher import SketchConfig, read_image, save_image, to_pencil_sketch

__all__ = [
    "SketchConfig",
    "read_image",
    "save_image",
    "to_pencil_sketch",
]

__version__ = "0.1.0"
