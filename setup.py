#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates.

import glob
import os
import shutil
from os import path
from setuptools import find_packages, setup
from typing import List



def get_version():
    init_py_path = path.join(path.abspath(path.dirname(__file__)), "detectron2", "__init__.py")
    init_py = open(init_py_path, "r").readlines()
    version_line = [l.strip() for l in init_py if l.startswith("__version__")][0]
    version = version_line.split("=")[-1].strip().strip("'\"")

    # The following is used to build release packages.
    # Users should never use it.
    suffix = os.getenv("D2_VERSION_SUFFIX", "")
    version = version + suffix
    if os.getenv("BUILD_NIGHTLY", "0") == "1":
        from datetime import datetime

        date_str = datetime.today().strftime("%y%m%d")
        version = version + ".dev" + date_str

        new_init_py = [l for l in init_py if not l.startswith("__version__")]
        new_init_py.append('__version__ = "{}"\n'.format(version))
        with open(init_py_path, "w") as f:
            f.write("".join(new_init_py))
    return version


def get_extensions():
    this_dir = path.dirname(path.abspath(__file__))
    extensions_dir = path.join(this_dir, "detectron2", "layers", "csrc")

    main_source = path.join(extensions_dir, "vision.cpp")
    sources = glob.glob(path.join(extensions_dir, "**", "*.cpp"))

    include_dirs = [extensions_dir]

    ext_modules = [
    ]

    return ext_modules





# For projects that are relative small and provide features that are very close
# to detectron2's core functionalities, we install them under detectron2.projects
PROJECTS = {
    "detectron2.projects.point_rend": "projects/PointRend/point_rend",
    "detectron2.projects.deeplab": "projects/DeepLab/deeplab",
    "detectron2.projects.panoptic_deeplab": "projects/Panoptic-DeepLab/panoptic_deeplab",
}

setup(
    name="detectron2",
    version=get_version(),
    author="FAIR",
    url="https://github.com/facebookresearch/detectron2",
    description="Detectron2 is FAIR's next-generation research "
    "platform for object detection and segmentation.",
    packages=find_packages(exclude=("configs", "tests*")) + list(PROJECTS.keys()),
    package_dir=PROJECTS,
    package_data={},
    python_requires=">=3.7",
    install_requires=[
        # These dependencies are not pure-python.
        # In general, avoid adding dependencies that are not pure-python because they are not
        # guaranteed to be installable by `pip install` on all platforms.
        "Pillow>=7.1",  # or use pillow-simd for better performance
        "matplotlib",  # TODO move it to optional after we add opencv visualization
        "pycocotools>=2.0.2",  # corresponds to https://github.com/ppwwyyxx/cocoapi
        # Do not add opencv here. Just like pytorch, user should install
        # opencv themselves, preferrably by OS's package manager, or by
        # choosing the proper pypi package name at https://github.com/skvark/opencv-python
        # Also, avoid adding dependencies that transitively depend on pytorch or opencv.
        # ------------------------------------------------------------
        # The following are pure-python dependencies that should be easily installable.
        # But still be careful when adding more: fewer people are able to use the software
        # with every new dependency added.
        "termcolor>=1.1",
        "yacs>=0.1.8",
        "tabulate",
        "cloudpickle",
        "tqdm>4.29.0",
        "tensorboard",
        # Lock version of fvcore/iopath because they may have breaking changes
        # NOTE: when updating fvcore/iopath version, make sure fvcore depends
        # on compatible version of iopath.
        "fvcore>=0.1.5,<0.1.6",  # required like this to make it pip installable
        "iopath>=0.1.7,<0.1.10",
        "dataclasses; python_version<'3.7'",
        "omegaconf>=2.1,<2.4",
        "hydra-core>=1.1",
        "black",
        "packaging",
        # NOTE: When adding new dependencies, if it is required at import time (in addition
        # to runtime), it probably needs to appear in docs/requirements.txt, or as a mock
        # in docs/conf.py
    ],
    extras_require={
        # optional dependencies, required by some features
        "all": [
            "fairscale",
            "timm",  # Used by a few ViT models.
            "scipy>1.5.1",
            "shapely",
            "pygments>=2.2",
            "psutil",
            "panopticapi @ https://github.com/cocodataset/panopticapi/archive/master.zip",
        ],
        # dev dependencies. Install them by `pip install 'detectron2[dev]'`
        "dev": [
            "flake8==3.8.1",
            "isort==4.3.21",
            "flake8-bugbear",
            "flake8-comprehensions",
            "black==22.3.0",
        ],
    },
    ext_modules=get_extensions(),
    cmdclass={},
)
