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
parser.add_argument('--n_frames', default=10, type=int,
                    help="Number of frames to read divided by 3.")
parser.add_argument('--output_dir', default=None,
                    help="Output directory with RGB frames.")
parser.add_argument('--csv_dir', default=None, type=int,
                    help="Write raw csv files along with the images.")

if __name__ == "__main__":
    args = parser.parse_args()

    frame_size = args.frame_w*args.frame_h*args.pixel_size

    def find_footer(buf):
        i = 0
        while True:
            if buf[i] == 13 and buf[i+1] == 0 and buf[i+2] == 10:
                return i+3
            i = i+1

    with serial.Serial(
            args.input_device, args.input_rate,
            timeout=args.n_frames+1) as ser:
        data_buffer = ser.read(
                (frame_size + args.footer_size + 4)*(args.n_frames+1))

    print("Serial Done!")

    start_index = find_footer(data_buffer)

    print("Start found at %d!" % start_index)

    offset = start_index
    for i in range(args.n_frames):
        if args.csv_dir is not None:
            if not os.path.exists(args.csv_dir):
                os.makedirs(args.csv_dir)

            raw_data = np.frombuffer(data_buffer, dtype=np.uint8,
                              count=(frame_size+args.footer_size+args.timestamp_size),
                              offset = offset)
            out_file_path = os.path.join(args.csv_dir, 'frame%d.csv' % i)
            np.savetxt(out_file_path, raw_data, delimiter=',')
        frame = np.frombuffer(data_buffer, dtype=np.uint8, count=frame_size,
                              offset=offset)
        offset += frame_size
        time_stamp = np.frombuffer(data_buffer, dtype=np.uint8, count=args.timestamp_size,
                                   offset=offset)
        time_stamp = int.from_bytes(time_stamp.tobytes(), "little",
                                    signed="False")
        offset += args.timestamp_size
        footer = np.frombuffer(data_buffer, dtype=np.uint8, count=args.footer_size,
                               offset=offset)
        offset += args.footer_size
        assert footer[0] == 13 and footer[1] == 0 and footer[2] == 10, \
                "Wrong footer (%d, %d, %d) at frame %d" % (footer[0], footer[1], footer[2], i)
        if args.output_dir is not None:
            if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir)
            frame.shape = (args.frame_h, args.frame_w)
            out_file_path = os.path.join(args.output_dir, '%08d_%08d.png' % (i, time_stamp))
            cv2.imwrite(out_file_path, frame) 
