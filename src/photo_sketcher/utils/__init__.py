#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Photo Sketching using Computer Vision
File: utils/__init__.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-11-10
Updated: 2025-11-10
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Utility subpackage initializer. Currently re-exports helpers for filesystem
and image I/O related tasks.

Usage:
from photo_sketcher.utils import discover_images

Notes:
- Keep this file lightweight and import only stable public utilities.
=========================================================================================================
"""

from __future__ import annotations

from .io_utils import IMAGE_EXTENSIONS, derive_output_path, discover_images

__all__ = [
    "IMAGE_EXTENSIONS",
    "derive_output_path",
    "discover_images",
]
