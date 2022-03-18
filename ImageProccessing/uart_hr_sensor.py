import serial
import numpy as np
import cv2

frame_w = 638
frame_h = 480
bytes_per_pixel = 2
footer_bytes = 3
n_frames = 10

bytes_per_frame = frame_w*frame_h*bytes_per_pixel

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
                return i + 1;
            elif val == 13:
                state = "1"
            else:
                state = "0"

with serial.Serial('/dev/tty.usbmodem142103', 7e6, timeout=20) as ser:
    data_buffer = ser.read((bytes_per_frame + footer_bytes)*n_frames)

print("Serial Done!")

start_index = find_footer(data_buffer)

print("Start found at %d!" % start_index)

frame = np.frombuffer(data_buffer, dtype=np.uint8, count=bytes_per_frame,
                      offset=start_index)
img = np.reshape(frame, (480, 638, 2))
img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_YUY2)
cv2.imwrite('frame%d.png' % 0, img)

#for i in range(n_frames):
#    frame = np.frombuffer(data_buffer, dtype=np.uint8, count=bytes_per_frame,
#                          offset=(bytes_per_frame+footer_bytes)*i)
#    footer = np.frombuffer(data_buffer, dtype=np.uint8, count=footer_bytes,
#                           offset=((bytes_per_frame+footer_bytes)*i + bytes_per_frame))
#    #assert footer[0] == 13 and footer[1] == 0 and footer[2] == 10, \
#    #        "Wrong footer at frame %d" % i
#    img = np.reshape(frame, (480, 638, 2))
#    img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_YUY2)
#    cv2.imwrite('frame%d.png' % i, img)

