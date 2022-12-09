![Kirby Mascot]

# Computational Genomics: Team 42 Final Project<!-- omit in toc -->
**Authors**: Aidan Aug, Mark Tiavas, Karen He, Alan Zhang


<img src="https://raw.githubusercontent.com/jeertmans/manim-slides/main/static/logo.png" alt="drawing" width="200"/> <img src="https://raw.githubusercontent.com/ManimCommunity/manim/main/logo/cropped.png" alt="drawing" width="200"/>

[![Latest Release][pypi-version-badge]][pypi-version-url]
[![Python version][pypi-python-version-badge]][pypi-version-url]

## Probabilistic Data Structures: Teaching Lecture <!-- omit in toc -->

This repository contains the source code for Team 42's Final Project. For our project, we decided to develop a teaching plan for probabilistic data structures with relevance to genomics. Our final deliverable includes a range of supporting materials, such as tutorials, worked examples, pedagogical visualizations or animations, assessments.

This GitHub repository contains the source code for the data structures implemented, as well as the code for the animations created using Manim and Manim Slides.

## Table of contents<!-- omit in toc -->

- [Implementation Code](#implementation-code)
- [Manim Slides](#manim-slides)
  - [Installation](#installation)
    - [Dependencies](#dependencies)
    - [Download source-code for animations](#download-source-code-for-animations)
    - [Install From Repository](#install-from-repository)
  - [Usage](#usage)
    - [Basic Example](#basic-example)
    - [Rendering the bloom filter animation (works for bloom, cuckoo, or countmin)](#rendering-the-bloom-filter-animation-works-for-bloom-cuckoo-or-countmin)
  - [Key Bindings](#key-bindings)
  - [Features and Comparison with original manim-presentation](#features-and-comparison-with-original-manim-presentation)
  - [F.A.Q](#faq)
    - [How to increase quality on Windows](#how-to-increase-quality-on-windows)

# Implementation Code
---
Code for implementations can be found in **prob-data-struct** folder.

There are 3 data structures implemented, BloomFilter, CuckooFilter, and CountMin.

The real implementations are in `BloomFilter.py`, `cuckooFilter.py`, and `CountMin.py`.
Simply run the following command to test them out

```bash
  python BloomFilter.py
```

You may need to `pip install bitstring` to run `cuckooFilter.py`

The homework assignment templates are in the corresponding `Template.Py` files. They also will be run by

```
  python BloomFilterTemplate.py
```

Examples inputs are present in each file. 

# Manim Slides
---

## Installation

Please see the source code for the dependencies used in this project:
* Manim: https://github.com/ManimCommunity/manim
* Manim-slides: https://github.com/jeertmans/manim-slides

For convenience, installation instructions are listed here.

While installing Manim Slides and its dependencies on your global Python is fine, it is recommended to use a [virtualenv](https://docs.python.org/3/tutorial/venv.html) for a local installation. To avoid linting errors, please install both manim and manim-slides in the same virtual environment.

### Dependencies

Manim Slides requires either Manim or ManimGL to be installed. Having both packages installed is fine too.

If none of those packages are installed, please refer to their specific installation guidelines:
- [Manim](https://docs.manim.community/en/stable/installation.html)
- [ManimGL](https://3b1b.github.io/manim/getting_started/installation.html)

### Download source-code for animations

Alternatively, you can install the original manim-slides repository directly, and copy/paste relevant python files for animation.

The recommended way to install the latest release is to use pip:

```bash
pip install manim-slides
```

If you do not have pip, please refer to the docs for installation: https://pip.pypa.io/en/stable/installation/

### Install From Repository

Install this lecture plan by cloning this repository locally, or unzipping the package. Manim Slides is to clone the git repository, and install from there:

```bash
git clone https://github.com/aaug1/GenomicsDataStruct.git
```

> *Note:* the `-e` flag allows you to edit the files, and observe the changes directly when using Manim Slides

## Usage
Tool for live presentations using either [Manim (community edition)](https://www.manim.community/) or [ManimGL](https://3b1b.github.io/manim/). Manim Slides will *automatically* detect the one you are using!

Using Manim Slides is a two-step process:
1. Render animations using `Slide` (resp. `ThreeDSlide`) as a base class instead of `Scene` (resp. `ThreeDScene`), and add calls to `self.pause()` everytime you want to create a new slide.
2. Run `manim-slides` on rendered animations and display them like a *Power Point* presentation.

The command-line documentation is available [online](https://eertmans.be/manim-slides/).

### Basic Example

Wrap a series of animations between `self.start_loop()` and `self.stop_loop()` when you want to loop them (until input to continue):

```python
# example.py

from manim import *
# or: from manimlib import *
from manim_slides import Slide

class Example(Slide):
    def construct(self):
        circle = Circle(radius=3, color=BLUE)
        dot = Dot()

        self.play(GrowFromCenter(circle))
        self.pause()  # Waits user to press continue to go to the next slide

        self.start_loop()  # Start loop
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.end_loop()  # This will loop until user inputs a key

        self.play(dot.animate.move_to(ORIGIN))
        self.pause()  # Waits user to press continue to go to the next slide

        self.wait()
```

You **must** end your `Slide` with a `self.play(...)` or a `self.wait(...)`.

First, render the animation files:

```bash
manim example.py
# or
manimgl example.py
```

To start the presentation using `Scene1`, `Scene2` and so on simply run:

```bash
manim-slides [OPTIONS] Scene1 Scene2...
```

Or in this example:

```bash
manim-slides Example
```

### Rendering the bloom filter animation (works for bloom, cuckoo, or countmin)

First, render the animation files:

```bash
manim bloom.py
# or
manimgl bloom.py
```

To start the interactive manim presentation

```bash
manim-slides Bloom
```

##  Key Bindings

The default key bindings to control the presentation are:

![manim-wizard](https://user-images.githubusercontent.com/27275099/197468787-19c83a81-d757-47b9-8f68-218427d30298.png)


You can run the **configuration wizard** to change those key bindings:

```bash
manim-slides wizard
```

A default file can be created with:

```bash
manim-slides init
```

> **_NOTE:_**  `manim-slides` uses key codes, which are platform dependent. Using the configuration wizard is therefore highly recommended.

## Features and Comparison with original manim-presentation

Below is a non-exhaustive list of features:

| Feature | `manim-slides` | `manim-presentation` |
|:--------|:--------------:|:--------------------:|
| Support for Manim | :heavy_check_mark: | :heavy_check_mark: |
| Support for ManimGL | :heavy_check_mark: | :heavy_multiplication_x: |
| Configurable key bindings | :heavy_check_mark: | :heavy_check_mark: |
| Configurable paths | :heavy_check_mark: | :heavy_multiplication_x: |
| Play / Pause slides | :heavy_check_mark: | :heavy_check_mark: |
| Next / Previous slide | :heavy_check_mark: | :heavy_check_mark: |
| Replay slide | :heavy_check_mark: | :heavy_check_mark: |
| Reverse slide | :heavy_check_mark: | :heavy_multiplication_x: |
| Multiple key per actions | :heavy_check_mark: | :heavy_multiplication_x: |
| One command line tool | :heavy_check_mark: | :heavy_multiplication_x: |
| Robust config file parsing | :heavy_check_mark: | :heavy_multiplication_x: |
| Support for 3D Scenes | :heavy_check_mark: | :heavy_multiplication_x: |
| Documented code | :heavy_check_mark: | :heavy_multiplication_x: |
| Tested on Unix, macOS, and Windows | :heavy_check_mark: | :heavy_multiplication_x: |
| Hide mouse cursor | :heavy_check_mark: | :heavy_multiplication_x: |

## F.A.Q

### How to increase quality on Windows

On Windows platform, one may encounter a lower image resolution than expected. Usually, this is observed because Windows rescales every application to fit the screen.
As found by [@arashash](https://github.com/arashash), in [#20](https://github.com/jeertmans/manim-slides/issues/20), the problem can be addressed by changing the scaling factor to 100%:

![Windows Fix Scaling]

in *Settings*->*Display*.


[pypi-version-badge]: https://img.shields.io/pypi/v/manim-slides?label=manim-slides
[pypi-version-url]: https://pypi.org/project/manim-slides/
[pypi-python-version-badge]: https://img.shields.io/pypi/pyversions/manim-slides
[Kirby Mascot]: ./manim-slides/images/8-bit-kirby.png
[Windows Fix Scaling]: https://i.ibb.co/9tJjZZ6/windows-quality-fix.png