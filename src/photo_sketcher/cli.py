#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Photo Sketching using Computer Vision
File: cli.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-11-10
Updated: 2025-11-10
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Command-line interface for converting photos to pencil sketches. Provides both
single-image and batch processing modes, exposing configuration parameters for
the underlying sketching algorithm.

Usage:
photo-sketch single input.jpg -o output_sketch.png
photo-sketch batch ./input_dir ./output_dir --recursive

Notes:
- Implemented using `typer` for modern, typed CLIs.
- Uses `rich` for user-friendly colored console output.
=========================================================================================================
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.progress import track

from .sketcher import SketchConfig, read_image, save_image, to_pencil_sketch
from .utils import derive_output_path, discover_images

app = typer.Typer(help="Convert photos into pencil sketches using OpenCV.")
console = Console()


@app.command()
def single(
    input_path: Path = typer.Argument(
        ..., exists=True, readable=True, help="Path to the input image."
    ),
    output_path: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Where to save the sketch. If omitted, uses "
            "'<stem>_sketch<ext>' next to the input file."
        ),
    ),
    kernel_size: int = typer.Option(
        21,
        "--kernel-size",
        "-k",
        help="Gaussian blur kernel size (positive odd integer).",
    ),
    sigma: float = typer.Option(
        0.0,
        "--sigma",
        "-s",
        help="Gaussian blur standard deviation (0 lets OpenCV choose).",
    ),
    blend_scale: float = typer.Option(
        256.0,
        "--blend-scale",
        "-b",
        help="Scaling factor for color-dodge-style blending.",
    ),
    show: bool = typer.Option(
        False,
        "--show",
        help="Display the original and sketch in OpenCV windows.",
    ),
) -> None:
    """Convert a single image to a pencil sketch."""

    try:
        config = SketchConfig(
            kernel_size=kernel_size,
            sigma=sigma,
            blend_scale=blend_scale,
        )

        image = read_image(input_path)
        sketch = to_pencil_sketch(image, config)

        if output_path is None:
            output_path = input_path.with_name(
                f"{input_path.stem}_sketch{input_path.suffix}"
            )

        save_image(sketch, output_path)
        console.print(f"[green]Saved sketch to:[/green] {output_path}")

        if show:
            import cv2

            cv2.imshow("Original", image)
            cv2.imshow("Sketch", sketch)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    except Exception as exc:  # pragma: no cover - CLI error path
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def batch(
    input_dir: Path = typer.Argument(
        ..., exists=True, file_okay=False, readable=True, help="Input directory."
    ),
    output_dir: Path = typer.Argument(
        ..., file_okay=False, help="Output directory for sketches."
    ),
    recursive: bool = typer.Option(
        True,
        "--recursive/--no-recursive",
        help="Recursively search for images.",
    ),
    kernel_size: int = typer.Option(
        21,
        "--kernel-size",
        "-k",
        help="Gaussian blur kernel size (positive odd integer).",
    ),
    sigma: float = typer.Option(
        0.0,
        "--sigma",
        "-s",
        help="Gaussian blur standard deviation (0 lets OpenCV choose).",
    ),
    blend_scale: float = typer.Option(
        256.0,
        "--blend-scale",
        "-b",
        help="Scaling factor for color-dodge-style blending.",
    ),
) -> None:
    """Convert all images in a directory to pencil sketches."""

    try:
        config = SketchConfig(
            kernel_size=kernel_size,
            sigma=sigma,
            blend_scale=blend_scale,
        )

        images = discover_images(input_dir, recursive=recursive)
        if not images:
            console.print(
                f"[yellow]No images found in directory:[/yellow] {input_dir}"
            )
            raise typer.Exit(code=0)

        output_dir.mkdir(parents=True, exist_ok=True)

        console.print(
            f"[cyan]Found {len(images)} image(s). Generating pencil sketches...[/cyan]"
        )

        for img_path in track(images, description="Sketching"):
            image = read_image(img_path)
            sketch = to_pencil_sketch(image, config)
            out_path = derive_output_path(img_path, output_dir)
            save_image(sketch, out_path)

        console.print(f"[green]Done. Sketches saved in:[/green] {output_dir}")

    except Exception as exc:  # pragma: no cover - CLI error path
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


def main() -> None:
    """Entry point used by the `photo-sketch` console script."""

    app()


if __name__ == "__main__":  # pragma: no cover
    main()
