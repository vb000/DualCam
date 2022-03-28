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
parser.add_argument('--frame_width', default=638, type=int,
                    help="Frame width.")
parser.add_argument('--frame_height', default=480, type=int,
                    help="Frame height.")
parser.add_argument('--pixel_size', default=2, type=int,
                    help="Pixel size in bytes.")
parser.add_argument('--timeout_per_frame', default=1.0, type=float,
                    help="Timeout per frame.")
parser.add_argument('--footer_size', default=3, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--timestamp_size', default=4, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--n_frames', default=10, type=int,
                    help="Number of frames to read.")
parser.add_argument('--output_dir', default=None,
                    help="Output directory with RGB frames.")

def find_footer(buf):
    i = 0
    while True:
        if buf[i] == 13 and buf[i+1] == 0 and buf[i+2] == 10:
            return i+3
        i = i+1

def uart_read_video(dev, rate, width, height, pix_depth, footer_size,
                    timestamp_size, timeout, n_frames, frame_decoder,
                    output_dir):
    frame_size = width * height * pix_depth

    with serial.Serial(
            dev, rate, timeout=timeout*(n_frames+1)) as ser:
        data_buffer = ser.read(
                (frame_size+footer_size+timestamp_size)*(n_frames+1))
    
    print("Serial read done!")
 
    start_index = find_footer(data_buffer)
    
    print("Start found at %d!" % start_index)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    offset = start_index
    for i in range(n_frames):
        frame = np.frombuffer(data_buffer, dtype=np.uint8, count=frame_size,
                              offset=offset)
        offset += frame_size
        time_stamp = np.frombuffer(data_buffer, dtype=np.uint8, count=timestamp_size,
                                   offset=offset)
        time_stamp = int.from_bytes(time_stamp.tobytes(), "little",
                                    signed="False")
        offset += timestamp_size
        footer = np.frombuffer(data_buffer, dtype=np.uint8, count=footer_size,
                               offset=offset)
        offset += footer_size
        assert footer[0] == 13 and footer[1] == 0 and footer[2] == 10, \
                "Wrong footer (%d, %d, %d) at frame %d" % (footer[0], footer[1], footer[2], i)

        if output_dir is not None:
            # Write rgb to output file
            frame = frame_decoder(frame, width, height, pix_depth)
            out_file_path = os.path.join(output_dir, '%08d_%08d.png' % (i, time_stamp))
            cv2.imwrite(out_file_path, frame)

def yuv_decoder(frame, w, h, bpp):
    frame = np.reshape(frame, (w, h, bpp))
    frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUY2)
    return frame 

if __name__ == "__main__":
    args = parser.parse_args()
    uart_read_video(args.input_device, args.input_rate, args.frame_width,
                    args.frame_height, args.pixel_size, args.footer_size,
                    args.timestamp_size, args.timeout_per_frame, args.n_frames,
                    yuv_decoder, args.output_dir)
