import argparse
import os
import tracemalloc
import picamera
import time
from gpiozero import LED
import threading

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
parser.add_argument('--output_dir', default='data',
                    help="Output directory with RGB frames.")
parser.add_argument('--stats', default=0, type=int,
                    help="Enable stats.")

def save(outfiles):
    for fd in outfiles:
        with open(fd['name'], 'wb') as f:
            f.write(fd['data'])

class Output(object):
    def __init__(self, camera, out_dir=None, stats=0):
        self.camera = camera
        self.out_dir = out_dir
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.out_arrays = [[], []]
        self.out_array = 0
        self.out_files = self.out_arrays[0]
        self.save_thread = None
        self.save_after = 150
        self.stats = stats
        self.led1 = LED(17)
        self.led2 = LED(18)
        self.led1.on()
        self.led2.on()
        self.origin_time = time.time_ns() // 1000
        self.frame_count = 0
        if self.stats != 0:
            self.max_time_period = 0
            self.max_write_time = 0
            self.total_write_time = 0
            self.total_time_period = 0

    def write(self, s):
        #print("%d: len_0=%d, len_1=%d, len=%d" %
        #      (self.frame_count, len(self.out_arrays[0]),
        #       len(self.out_arrays[1]), len(self.out_files)))
        if self.frame_count == 0:
            self.t_stamp_0 = time.time_ns() // 1000
            t_stamp = self.t_stamp_0
            self.prev_t_stamp = self.t_stamp_0
        else:
            t_stamp = self.t_stamp_0 + self.camera.frame.timestamp
            time_period = t_stamp - self.prev_t_stamp

        if self.frame_count > 1 and time_period > 80000:
            print("Frame rate error at frame %d: time period = %d" % (
                self.frame_count, time_period))
        t_delta_ms = (t_stamp - self.origin_time) // 1000
        filename = os.path.join(
            self.out_dir,
            '%09d_%09d.jpg' % (self.frame_count,
                               t_delta_ms))
        self.out_files.append({'name': filename, 'data': s})
        if len(self.out_files) >= self.save_after:
            if self.save_thread is not None:
                assert not self.save_thread.is_alive(), \
                        "Save thread not done before next save."
            self.save_thread = threading.Thread(
                    target=save,
                    args=(self.out_arrays[self.out_array],))
            self.save_thread.start()
            self.out_array = (self.out_array + 1) % 2
            self.out_arrays[self.out_array].clear()
            self.out_files = self.out_arrays[self.out_array]

        if self.stats != 0:
            t_stamp_end = time.time_ns() // 1000
            write_time = t_stamp_end - t_stamp
            if self.frame_count != 0:
                self.total_time_period += time_period
                self.total_write_time += write_time
                if self.max_time_period < time_period:
                    self.max_time_period = time_period
                if self.max_write_time < write_time:
                    self.max_write_time = write_time
        self.prev_t_stamp = t_stamp
        self.frame_count += 1

    def flush(self):
        self.led1.off()
        self.led2.off()
        self.save_thread.join()
        save(self.out_files)
        if self.stats != 0:
            print("%d frames are written" % self.frame_count)
            print("Max time period = %d us" % self.max_time_period)
            print("Max write time = %d us" % self.max_write_time)
            print("Avg. time period between frames = %d us" %
                  (self.total_time_period // (self.frame_count - 1)))
            print("Avg. write time per frame = %d us" %
                  (self.total_write_time // (self.frame_count - 1)))

if __name__ == "__main__":
    args = parser.parse_args()

    tracemalloc.start()
    with picamera.PiCamera() as camera:
        camera.resolution = (args.width, args.height)
        camera.framerate = args.frame_rate
        camera.start_recording(Output(camera, args.output_dir, args.stats),
                               format='mjpeg',
                               quality=100)
        camera.wait_recording(args.record_time)
        camera.stop_recording()
    print("Peak memory usage: %d MB" %
          (tracemalloc.get_traced_memory()[1] // 10**6))
    tracemalloc.stop()
