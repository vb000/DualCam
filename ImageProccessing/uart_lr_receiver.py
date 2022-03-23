import argparse
import os
import serial
import numpy as np
import cv2

parser = argparse.ArgumentParser(
    description="Reads data from uart and writes PNG output images.")
parser.add_argument('--input_device', default='/dev/tty.usbmodem142103',
                    help="Input directory with RAW pixel data.")
parser.add_argument('--input_rate', default=7e6,
                    help="Input baud rate.")
parser.add_argument('--frame_w', default=162, type=int,
                    help="Frame width.")
parser.add_argument('--frame_h', default=122, type=int,
                    help="Frame height.")
parser.add_argument('--pixel_size', default=1, type=int,
                    help="Pixel size in bytes.")
parser.add_argument('--footer_size', default=3, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--n_frames', default=10, type=int,
                    help="Number of frames to read.")
parser.add_argument('--output_dir', default='uart_lr_output',
                    help="Output directory with RGB frames.")

if __name__ == "__main__":
    args = parser.parse_args()

    frame_size = (args.frame_w+3)*args.frame_h*args.pixel_size

    def find_footer(buf):
        i = 0
        while True:
            if buf[i] == 121 and buf[i+1] == 1 and buf[i+2] == 1:
                return i+3
            i = i+1
    
    with serial.Serial(
            args.input_device, args.input_rate,
            timeout=args.n_frames+1) as ser:
        data_buffer = ser.read(
                (frame_size + args.footer_size)*(args.n_frames+1))
    
    print("Serial Done!")
    
    start_index = find_footer(data_buffer)
    
    print("Start found at %d!" % start_index)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    for i in range(args.n_frames):
        frame_offset = start_index + (frame_size+args.footer_size)*i
        frame = np.frombuffer(data_buffer, dtype=np.uint8, count=frame_size,
                              offset=frame_offset)
        img = np.reshape(frame, (args.frame_h, args.frame_w+3, args.pixel_size))
        img = img[:, :-3, :]
        # Write rgb to output file
        out_file_path = os.path.join(args.output_dir, 'frame%d.png' % i)
        cv2.imwrite(out_file_path, img)
 
