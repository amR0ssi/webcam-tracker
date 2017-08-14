# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:59:20 2017

@author: Antti Rossi
"""
import cv2
from collections import deque

class Tracker():
    def __init__(self, kind='KCF'):
        self.kind = kind
        self.tracker = cv2.Tracker_create(kind)
        self.bbox = None
        self.frame = None
        self.ret = False
        self.track = False

    def selectRoi(self):

        self.track = True
        try:
            self.bbox = cv2.selectROI('Selector', self.frame, False, False)
            self.tracker = cv2.Tracker_create(self.kind)
            self.ret = self.tracker.init(self.frame, self.bbox)
        except Exception as e:
            print(e, self.frame is None)

        cv2.destroyWindow('Selector')

    def update_bbox(self, frame):
        try:
            self.frame = frame
            if self.track:
                if self.bbox is None:
                    self.selectRoi()
                self.ret, self.bbox = self.tracker.update(self.frame)
                if self.ret:
                    frame = self.draw_box(frame)
            return frame
        except Exception as e:
            print(e)

    def draw_box(self, frame):
        p1 = (int(self.bbox[0]), int(self.bbox[1]))
        p2 = (int(self.bbox[0] + self.bbox[2]),
              int(self.bbox[1] + self.bbox[3]))
        return cv2.rectangle(frame, p1, p2, (0, 0, 255))

if __name__ == '__main__':
    import sys
    import time
    from camerastream import WebcamVideoStream
    video = WebcamVideoStream(0, deque())
    time.sleep(1)

    # Create a tracker
    tracker = Tracker()

    while True:
        try:
            # Read a new frame
            ok, frame = video.read()
            cv2.imshow("Tracking", frame)

#            if not ok:
#                break
            # Call the update method. Should this return something?
#            if ok:
#                image = tracker.update_bbox(frame)

                # Display result
#            if frame is not None:

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
            if k == ord('s'):
                tracker.selectRoi()
#                print('ROI selector set to ', select_roi)
            if k == ord('t'):
                tracker.track = not tracker.track
                print('Tracking set to ', tracker.track)
        except Exception as e:
            print(e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
#            break
#            video.stop()
#            cv2.destroyAllWindows()

    cv2.destroyAllWindows()
    video.stop()
