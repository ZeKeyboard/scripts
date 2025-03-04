from os.path import isdir
import numpy as np
import imageio.v3 as imageio
import argparse
import os
import matplotlib.pyplot as plt

from pathlib import Path

CPP_SKELETON = """
#pragma once

namespace images
{{

constexpr int {array_name}_HEIGHT = {height};
constexpr int {array_name}_WIDTH = {width};

constexpr float {array_name}_RED[]
{{
    {array_red}
}};

constexpr float {array_name}_GREEN[]
{{
    {array_green}
}};

constexpr float {array_name}_BLUE[]
{{
    {array_blue}
}};

}}
"""


def get_image_array(image: np.ndarray) -> str:
    flattened = image.flatten().astype(np.float32) / 255.0
    return ",".join((f"{x}f" for x in flattened))


def process_file(file_path: Path, output_folder: Path):
    image = imageio.imread(str(file_path))
    red = get_image_array(image[:, :, 0])
    green = get_image_array(image[:, :, 1])
    blue = get_image_array(image[:, :, 2])

    output_folder.mkdir(exist_ok=True)

    cpp_file_path = output_folder / (file_path.stem.lower() + ".h")
    array_name = file_path.stem.upper()
    file_contents = CPP_SKELETON.format(
        array_name=array_name,
        array_red=red,
        array_green=green,
        array_blue=blue,
        height=image.shape[0],
        width=image.shape[1],
        )
    with open(cpp_file_path, "w") as f:
        f.write(file_contents)


def main():
    parser = argparse.ArgumentParser(description="Generate CPP from image")
    parser.add_argument("-i", "--input-folder", type=Path, required=True, help="Path to the input folder of images")
    parser.add_argument("-o", "--output-folder", type=Path, required=True, help="Path to the input folder of images")
    args = parser.parse_args()

    folder: Path = args.input_folder
    for filename in os.listdir(folder):
        process_file(folder / filename, args.output_folder)


if __name__ == "__main__":
    main()
