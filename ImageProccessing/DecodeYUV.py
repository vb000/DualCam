"""
Converts YUV422 raw output of the HR image sensor to PNG images.
"""

import argparse
import os, glob
import numpy as np
import cv2

parser = argparse.ArgumentParser(
    description="YUV422 raw output files to PNG images.")
parser.add_argument('--input_dir', default=None,
                    help="Input directory with RAW pixel data.")
parser.add_argument('--output_dir', default=None,
                    help="Output directory with RGB frames.")

if __name__ == "__main__":
    args = parser.parse_args()
    
    # Input file paths
    file_paths = glob.glob(os.path.join(args.input_dir, '*.txt'))
    file_paths.sort()

    # File names
    filenames = [os.path.splitext(os.path.basename(_))[0]
                 for _ in file_paths]

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for inf, i in zip(file_paths, filenames):
        # Convert to rgb
        img = np.fromfile(inf, dtype=np.uint8)
        img = np.reshape(img, (480, 640, 2))
        img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_YUY2)
        # Write rgb to output file
        out_file_path = os.path.join(args.output_dir, str(i) + '.png')
        cv2.imwrite(out_file_path, img)
