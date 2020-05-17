from threading import Thread
import cv2
import numpy as np

#class that gets the images from the camera
class Camera:
    #setup the variables
    def __init__(self,url = 'http://192.168.1.254:8080/video'):
        self.url = url
        #self.url = url
        #self.url = input("url: ")
        print("get cap")
        self.cap = cv2.VideoCapture(self.url)
        print("captured")
        self.running = True
        (self.ret, self.frame) = self.cap.read()
    
    #start the 'Update' method but thread it so it runs while the 
    #rest of the program is running otherwise fps is too low for camera
    #and end up being behind as can not jump to latest frame, only next
    def Start(self):
        print("thread")
        Thread(target=self.Update, args=()).start()
        print("started")
    
    #this gets the next image in the camera feed and assigns it to self.frame
    def Update(self):
        while self.running:
            (self.ret, self.frame) = self.cap.read()



def main():
    #import DetectPlane    
    #setup vars
    detect_faces = False
    count = 0
    print("main")
    cam = Camera(0)
    cam.Start()
    a = np.resize(cam.frame,(128,128,3))
    #loop until break
    while(True):
        #get latest frame from camera 
        frame = cam.frame
        #change the size 
        big_frame = cv2.resize(frame,(frame.shape[1]//2,frame.shape[0]//2))
        small_frame = cv2.resize(frame,(frame.shape[1]//4,frame.shape[0]//4))
        #if there is a frame
        if frame is not None:
            #if detect faces
            if detect_faces:      
                #detect if there is a face using smaller frame
                box = DetectPlane.Detect(frame)
                #if there is a face found, put rectangle around it
                if box != None:
                    x,y,w,h = box
                    cv2.rectangle(frame,(x*2,y*2),((x+w)*2,(y+h)*2),255,5)
            #update screen
            cv2.imshow('video',frame)
        else:
            break
        q = cv2.waitKey(1)
        if q == ord("q"):
            break
        if q == ord("w"):
            detect_faces = not detect_faces
    #stop program
    cv2.destroyAllWindows()
    cam.running = False


if __name__ == "__main__":
    main()