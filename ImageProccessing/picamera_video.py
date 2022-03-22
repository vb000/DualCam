import picamera
import numpy as np
from PIL import Image

class Output(object):
    def __init__(self, resolution=(640, 480)):
        self.frames = 0
        self.resolution = resolution
        self.images = []

    def write(self, s):
        frame = np.frombuffer(s, dtype=np.uint8)
        frame.shape = (self.resolution[1], self.resolution[0], 3)
        self.images.append(Image.fromarray(frame, 'RGB'))
        self.frames += 1

    def flush(self):
        #for i, img in enumerate(self.images):
        #    img.save('frame%d.png' % i)
        print('%d frames are written' % self.frames)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 15
    camera.start_recording(Output(camera.resolution), format='rgb')
    camera.wait_recording(100)
    camera.stop_recording()
