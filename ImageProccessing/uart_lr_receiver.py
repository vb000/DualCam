import argparse
import os
import serial
import numpy as np
import cv2

parser = argparse.ArgumentParser(
    description="Reads data from uart and writes PNG output images.")
parser.add_argument('--input_device', default='/dev/tty.usbserial-FT3NKYBD',
                    help="Input directory with RAW pixel data.")
parser.add_argument('--input_rate', default=2.95e6,
                    help="Input baud rate.")
parser.add_argument('--frame_w', default=162, type=int,
                    help="Frame width.")
parser.add_argument('--frame_h', default=122, type=int,
                    help="Frame height.")
parser.add_argument('--pixel_size', default=1, type=int,
                    help="Pixel size in bytes.")
parser.add_argument('--footer_size', default=3, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--n_frame_groups', default=10, type=int,
                    help="Number of frames to read divided by 3.")
parser.add_argument('--group_size', default=3, type=int,
                    help="Number of frames in a frame group.")
parser.add_argument('--output_dir', default='uart_lr_output',
                    help="Output directory with RGB frames.")
parser.add_argument('--write_csv', default=0, type=int,
                    help="Write raw csv files along with the images.")

if __name__ == "__main__":
    args = parser.parse_args()

    frame_size = args.frame_w*args.frame_h*args.pixel_size

    def find_footer(buf):
        i = 0
        while True:
            if buf[i] == 13 and buf[i+1] == 0 and buf[i+2] == 10:
                return i
            i = i+1
    
    with serial.Serial(
            args.input_device, args.input_rate,
            timeout=args.n_frame_groups) as ser:
        data_buffer = ser.read(
                (args.group_size*frame_size + args.footer_size)*(args.n_frame_groups+1))
    
    print("Serial Done!")
    
    start_index = find_footer(data_buffer)
    
    print("Start found at %d!" % start_index)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    offset = start_index
    for i in range(args.group_size*args.n_frame_groups):
        if i % args.group_size == 0:
            footer = np.frombuffer(data_buffer, dtype=np.uint8, count=args.footer_size,
                                   offset=offset)
            offset += args.footer_size
            assert footer[0] == 13 and footer[1] == 0 and footer[2] == 10, \
                    "Wrong footer (%d, %d, %d) at frame %d" % (footer[0], footer[1], footer[2], i)
        frame = np.frombuffer(data_buffer, dtype=np.uint8, count=frame_size,
                              offset=offset)
        if args.write_csv != 0:
            out_file_path = os.path.join(args.output_dir, 'frame%d.csv' % i)
            np.savetxt(out_file_path, frame, delimiter=',')
        offset += frame_size
        # Write rgb to output file
        frame.shape = (args.frame_h, args.frame_w)
        out_file_path = os.path.join(args.output_dir, 'frame%d.png' % i)
        cv2.imwrite(out_file_path, frame)
 
