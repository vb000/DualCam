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
parser.add_argument('--frame_w', default=638, type=int,
                    help="Frame width.")
parser.add_argument('--frame_h', default=480, type=int,
                    help="Frame height.")
parser.add_argument('--pixel_size', default=2, type=int,
                    help="Pixel size in bytes.")
parser.add_argument('--footer_size', default=3, type=int,
                    help="Size of the footer sent after each frame in bytes.")
parser.add_argument('--n_frames', default=10, type=int,
                    help="Number of frames to read.")
parser.add_argument('--output_dir', default='uart_output',
                    help="Output directory with RGB frames.")

if __name__ == "__main__":
    args = parser.parse_args()

    frame_size = args.frame_w*args.frame_h*args.pixel_size
    
    def find_footer(ser):
        state = "0"
        i = 0
        while(True):
            val = ser[i]
            i = i + 1
            if state == "0":
                if val == 13:
                    state = "1"
            elif state == "1":
                if val == 0:
                    state = "2"
                elif val == 13:
                    state == "1"
                else:
                    state = "0"
            elif state == "2":
                if val == 10:
                    return i;
                elif val == 13:
                    state = "1"
                else:
                    state = "0"
    
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
        footer = np.frombuffer(data_buffer, dtype=np.uint8, count=args.footer_size,
                               offset=frame_offset + frame_size)
        assert footer[0] == 13 and footer[1] == 0 and footer[2] == 10, \
                "Wrong footer (%d, %d, %d) at frame %d" % (footer[0], footer[1], footer[2], i)
        img = np.reshape(frame, (args.frame_h, args.frame_w, args.pixel_size))
        img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_YUY2)
        # Write rgb to output file
        out_file_path = os.path.join(args.output_dir, 'frame%d.png' % i)
        cv2.imwrite(out_file_path, img)
 
