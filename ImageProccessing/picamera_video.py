import argparse
import os
import tracemalloc
import picamera
import time

parser = argparse.ArgumentParser(
    description="Records a video from PiCamera.")
parser.add_argument('--frame_rate', default=15, type=int,
                    help="Input frame rate in FPS.")
parser.add_argument('--width', default=640, type=int,
                    help="Frame width.")
parser.add_argument('--height', default=480, type=int,
                    help="Frame height.")
parser.add_argument('--record_time', default=10, type=int,
                    help="Recording time in seconds.")
parser.add_argument('--output_dir', default='out',
                    help="Output directory with RGB frames.")

class Output(object):
    def __init__(self, out_dir=None):
        self.out_dir = out_dir
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.frame_count = 0
        self.total_write_time = 0

    def write(self, s):
        t_stamp = time.time_ns() // 1000
        filename = os.path.join(self.out_dir, '%d.jpg' % t_stamp)
        with open(filename, 'wb') as f:
            f.write(s)
        self.frame_count += 1
        t_stamp_end = time.time_ns() // 1000
        self.total_write_time += t_stamp_end - t_stamp

    def flush(self):
        print('%d frames are written' % self.frame_count)
        print("Avg. write time per frame: %d us" %
              self.total_write_time / self.frame_count)

if __name__ == "__main__":
    args = parser.parse_args()

    tracemalloc.start()
    with picamera.PiCamera() as camera:
        camera.resolution = (args.width, args.height)
        camera.framerate = args.frame_rate
        camera.start_recording(Output(args.output_dir), format='mjpeg',
                               quality=100)
        camera.wait_recording(args.record_time)
        camera.stop_recording()
    print("Peak memory usage: %d MB" %
          (tracemalloc.get_traced_memory()[1] // 10**6))
    tracemalloc.stop()
