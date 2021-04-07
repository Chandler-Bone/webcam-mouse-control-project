import numpy as np
import cv2 as cv

class CalibrateDetection:

    monitor_dimensions = 1920, 1080
    use_ip_webcam = 0
    webcam_ip = ""
    resolution_width = 1920
    resolution_height = 1080
    lower_skin = np.array([255,255,255])
    upper_skin = np.array([0,0,0])
    is_debug = 0

    IMAGE_DIMENSIONS = 852, 480 

    

    def __init__(self, use_ip_webcam, webcam_ip, resolution_width, resolution_height):

        self.use_ip_webcam = use_ip_webcam
        #change the webcam_ip to 0 if you are using a webcame connected to pc
        self.webcam_ip = webcam_ip
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height

    


    def run(self):
        
        def selectRGBValue(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN: #checks mouse left button down condition
                colors = [0]*3
                colors[0] = img[y,x,0]#R
                colors[1] = img[y,x,1]#G
                colors[2] = img[y,x,2]#B

                for i in range(len(colors)):
                    if colors[i] > 250:
                        colors[i] = 250
                    if colors[i] < 5:
                        colors[i] = 5

                for i in range(len(colors)):
                    if colors[i] < self.lower_skin[i]:
                        self.lower_skin[i] = colors[i]
                    if colors[i] > self.upper_skin[i]:
                        self.upper_skin[i] = colors[i]

                # self.lower_skin = np.array([colors[0]-5, colors[1]-5, colors[2]-5])
                # self.upper_skin = np.array([colors[0]+5, colors[1]+5, colors[2]+5])
                print(colors[0], " ", colors[1], " ", colors[2])
                print(self.lower_skin)
                print(self.upper_skin)

                # colors = [0]*3
                # colors[0] = hsv[y,x,0]#Hue
                # colors[1] = hsv[y,x,1]#Saturation
                # colors[2] = hsv[y,x,2]#Value
                
                # for i in range(len(colors)):
                #      if colors[i] > 250:
                #          colors[i] = 250
                #      if colors[i] < 5:
                #          colors[i] = 5
                # self.lower_skin = np.array([colors[0]-5, colors[1]-5, colors[2]-5])
                # self.upper_skin = np.array([colors[0]+5, colors[1]+5, colors[2]+5])
                # print(hsv[y, x])
                
                

        cap = cv.VideoCapture(self.webcam_ip)
        cv.namedWindow('Calibrate')
        cv.setMouseCallback('Calibrate', selectRGBValue)

        while(True):

            #reads and resizes image
            _, img = cap.read()
            img = cv.resize(img, self.IMAGE_DIMENSIONS)
            img = cv.flip(img, 1)
            img = cv.blur(img, (5,5))

            #converts image rgb -> hsv and removes colors that are not in range
            hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
            mask = cv.inRange(img, self.lower_skin, self.upper_skin)
            mask = cv.bitwise_not(mask)
            res = cv.bitwise_and(img, img, mask = mask)

            cv.imshow('Calibrate', res)

            #press key to stop program
            if cv.waitKey(1) & 0xFF == ord('f'):
                break

        cv.destroyAllWindows()

if __name__ == '__main__':
    hand_detection = CalibrateDetection(1,"https://192.168.0.8:8080/video",1920,1080)
    hand_detection.run()