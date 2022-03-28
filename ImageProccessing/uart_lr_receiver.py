import argparse
import os
import serial
import numpy as np
import cv2
from uart_hr_receiver import uart_read_video

parser = argparse.ArgumentParser(
    description="Reads data from uart and writes PNG output images.")
parser.add_argument('--input_device', default='/dev/tty.usbserial-FT3NKYBD',
                    help="Input directory with RAW pixel data.")
parser.add_argument('--input_rate', default=2.95e6,
                    help="Input baud rate.")
parser.add_argument('--timeout_per_frame', default=0.07, type=float,
                    help="Timeout per frame.")
parser.add_argument('--frame_width', default=162, type=int,
                    help="Frame width.")
parser.add_argument('--frame_height', default=122, type=int,
                    help="Frame height.")
parser.add_argument('--pixel_size', default=1, type=int,
                    help="Pixel size in bytes.")
parser.add_argument('--footer_size', default=3, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--timestamp_size', default=4, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--n_frames', default=10, type=int,
                    help="Number of frames to read divided by 3.")
parser.add_argument('--output_dir', default='uart_lr_output',
                    help="Output directory with RGB frames.")
parser.add_argument('--csv_dir', default=0, type=int,
                    help="Write raw csv files along with the images.")


def lr_decoder(frame, w, h, bpp):
    frame.shape = w, h
    return frame 

if __name__ == "__main__":
    args = parser.parse_args()
    uart_read_video(args.input_device, args.input_rate, args.frame_width,
                    args.frame_height, args.pixel_size, args.footer_size,
                    args.timestamp_size, args.timeout_per_frame, args.n_frames,
                    lr_decoder, args.output_dir)

