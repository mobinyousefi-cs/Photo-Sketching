# Photo Sketching using Computer Vision

Convert your photos into clean pencil sketches using OpenCV and Python.

This project provides a small yet professional command-line tool and library for generating pencil-sketch versions of images. It is designed with modern Python packaging practices so you can use it as a standalone app or as a reusable module in your own projects.

---

## Features

- ✅ **High-quality pencil sketch effect** using OpenCV
- 🎛️ **Configurable parameters** (Gaussian blur kernel size, sigma, blend scale)
- 🖼️ **Single-image and batch processing** via a clean CLI (powered by Typer)
- 📁 Supports common image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`
- 🧩 Well-structured Python package (`src/` layout) with tests
- 🧪 Basic unit tests using `pytest`
- 📦 Modern packaging using `pyproject.toml`

You can use your own images as a dataset. For experimentation, any collection of natural images will work (e.g., landscapes, portraits, objects).

---

## How it works

The core sketching pipeline is:

1. Read the input image using OpenCV
2. Convert the image to grayscale
3. Invert the grayscale image
4. Apply a Gaussian blur to the inverted image
5. Blend the grayscale and blurred images using `cv2.divide` to produce a pencil sketch effect

Mathematically, the last step approximates a color dodge blend:

```python
sketch = cv2.divide(gray, 255 - blurred, scale=blend_scale)
```

This enhances edges and fine structures while suppressing flat regions, producing a hand-drawn pencil sketch appearance.

---

## Project structure

```text
photo-sketching/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ pyproject.toml
├─ requirements.txt
├─ src/
│  └─ photo_sketcher/
│     ├─ __init__.py
│     ├─ sketcher.py
│     └─ utils/
│        ├─ __init__.py
│        └─ io_utils.py
└─ tests/
   └─ test_sketcher.py
```

- `src/photo_sketcher/sketcher.py` – Core sketch generation logic
- `src/photo_sketcher/utils/io_utils.py` – Helper utilities for discovering and naming image files
- `src/photo_sketcher/cli.py` – Command-line interface (exposed as the `photo-sketch` command)
- `tests/test_sketcher.py` – Minimal unit tests

> Note: Depending on your editor, `cli.py` may also appear under `src/photo_sketcher/`.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mobinyousefi-cs/photo-sketcher.git
cd photo-sketcher
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

### 3. Install in editable mode

Using `pip` with `pyproject.toml`:

```bash
pip install -e .
```

Or, using `requirements.txt` directly:

```bash
pip install -r requirements.txt
```

---

## Command-line usage

After installation, the `photo-sketch` command becomes available.

### Convert a single image

```bash
photo-sketch single input.jpg -o output_sketch.png
```

Optional arguments:

- `--kernel-size`, `-k` – Gaussian blur kernel size (odd integer, e.g. 11, 21)
- `--sigma`, `-s` – Gaussian blur sigma (0 lets OpenCV choose a default)
- `--blend-scale`, `-b` – Scaling factor for blending (default: 256.0)
- `--show` – Display original and sketch in OpenCV windows

Example:

```bash
photo-sketch single input.jpg \
  -o input_sketch.png \
  -k 21 \
  -s 0.0 \
  -b 256.0 \
  --show
```

### Batch convert a directory of images

```bash
photo-sketch batch ./input_images ./output_sketches
```

Options:

- `--recursive / --no-recursive` – Recursively search subdirectories (default: recursive)
- `--kernel-size`, `--sigma`, `--blend-scale` – Same as for `single`

Example:

```bash
photo-sketch batch ./dataset/raw_photos ./dataset/sketches \
  --recursive \
  -k 19 \
  -s 0.0 \
  -b 256.0
```

---

## Python API usage

You can also import and use the sketching logic directly in your own Python projects:

```python
from pathlib import Path

from photo_sketcher import SketchConfig, read_image, to_pencil_sketch, save_image

input_path = Path("input.jpg")
output_path = Path("input_sketch.png")

config = SketchConfig(kernel_size=21, sigma=0.0, blend_scale=256.0)
image = read_image(input_path)
sketch = to_pencil_sketch(image, config)
save_image(sketch, output_path)
```

---

## Dataset

This project does **not** depend on a specific dataset. You can:

- Use your own photos (portraits, objects, landscapes, etc.)
- Download any open image dataset (e.g., generic image collections) and run the batch mode

The sketching pipeline is fully deterministic for a given configuration, so it is suitable for reproducible experiments.

---

## Development

### Run tests

```bash
pytest
```

### Code style

This project is configured for:

- [`black`](https://github.com/psf/black) for code formatting
- [`ruff`](https://github.com/astral-sh/ruff) for linting

You can run them manually, for example:

```bash
black src tests
ruff check src tests
```

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- OpenCV for powerful and efficient image processing primitives
- NumPy for numerical operations
- Typer and Rich for a clean and friendly command-line experience

If you use or extend this project, a star on the GitHub repository is always appreciated 😊

