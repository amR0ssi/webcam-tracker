# import the necessary packages
from threading import Thread
import cv2
from collections import deque
import time
from imutils.video import FPS

class WebcamVideoStream:
    def __init__(self, src=0, pending=deque()):
        # initialize the video camera stream and read the first frame
        # from the stream
        print('Object created')
        self.pending = pending
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.pending.append((self.grabbed, self.frame))
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.halted = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the threadq
            if self.stopped:
                print('Releasing capture')
                self.stream.release()
                return
            # Check if there should be a pause
            if not self.halted:
                self.grabbed, self.frame = self.stream.read()
#                if self.grabbed:
                self.pending.append((self.grabbed, self.frame))
            cv2.waitKey(1)

    def read(self):
        # return the frame most recently read
        if len(self.pending) > 0:
            print(len(self.pending))
            return self.pending.popleft()
        else:
            return False, None

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def halt(self, halt):
        # indicate that queue collection should be halted
        self.halted = halt


if __name__ == '__main__':
    pending = deque()

    cap = WebcamVideoStream(0, pending)
    time.sleep(1)
    cap.start()
    fps = FPS().start()
    while True:
        ok, frame = cap.read()
        if frame is not None:
            cv2.imshow('frame', frame)
            fps.update()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.stop()
            fps.stop()
            break
    print(fps.fps())
    cv2.destroyAllWindows()
