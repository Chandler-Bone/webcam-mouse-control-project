import os
import tkinter as tk
import tkinter.ttk as ttk
from configparser import ConfigParser

import cv2 as cv
import numpy as np
from PIL import Image, ImageTk


class CalibrateDetection:

    webcam_ip = ""
    lower_skin = np.array([255, 255, 255])
    upper_skin = np.array([0, 0, 0])
    is_debug = 0
    IMAGE_DIMENSIONS = 852, 480

    def __init__(self, use_ip_webcam, webcam_ip):

        # change the webcam_ip to 0 if you are using a webcame connected to pc
        # constructor
        self.webcam_ip = webcam_ip
        if use_ip_webcam == 1:
            self.cap = cv.VideoCapture(self.webcam_ip) #ip webcam connect
        else:
            self.cap = cv.VideoCapture(0) #integrated webcam connect

    def loadGUI(self):
        # building GUI
        self.root = tk.Tk()
        cur_path = os.path.dirname(os.path.abspath(__file__))
        self.root.iconbitmap(cur_path + "\\hand_icon.ico")
        self.root.title("Calibration Menu")
        self.root.resizable(False, False)

        self.frame1 = ttk.Frame(self.root)
        self.canvas1 = tk.Canvas(self.frame1)
        self.canvas1.configure(height="480", width="1127")
        self.canvas1.pack(side="top")
        self.scale1 = ttk.Scale(self.frame1)
        self.upper_hue = tk.IntVar(value=self.upper_skin[0])
        self.scale1.configure(
            from_="0", orient="horizontal", to="255", variable=self.upper_hue
        )
        self.scale1.place(anchor="nw", relwidth=".16", x="15", y="40")
        self.scale1.configure(command=self.updateHSV)
        self.entry1 = ttk.Entry(self.frame1)
        self.entry1.configure(justify="center", textvariable=self.upper_hue)
        self.entry1.delete("0", "end")
        self.entry1.insert("0", self.upper_skin[0])
        self.entry1.place(anchor="nw", relwidth=".024", x="205", y="40")
        self.label1 = ttk.Label(self.frame1)
        self.label1.configure(text="Upper")
        self.label1.place(anchor="nw", x="238", y="40")
        self.label2 = ttk.Label(self.frame1)
        self.label2.configure(text="_____")
        self.label2.place(anchor="nw", x="15", y="17")
        self.label3 = ttk.Label(self.frame1)
        self.label3.configure(text="Hue")
        self.label3.place(anchor="nw", x="15", y="13")
        self.scale2 = ttk.Scale(self.frame1)
        self.lower_hue = tk.IntVar(value=self.lower_skin[0])
        self.scale2.configure(
            from_="0", orient="horizontal", to="255", variable=self.lower_hue
        )
        self.scale2.place(anchor="nw", relwidth=".16", x="15", y="62")
        self.scale2.configure(command=self.updateHSV)
        self.entry3 = ttk.Entry(self.frame1)
        self.entry3.configure(justify="center", textvariable=self.lower_hue)
        self.entry3.delete("0", "end")
        self.entry3.insert("0", self.lower_skin[0])
        self.entry3.place(anchor="nw", relwidth=".024", x="205", y="62")
        self.label4 = ttk.Label(self.frame1)
        self.label4.configure(text="Lower")
        self.label4.place(anchor="nw", x="238", y="62")
        self.label5 = ttk.Label(self.frame1)
        self.label5.configure(text="___________")
        self.label5.place(anchor="nw", x="15", y="89")
        self.label6 = ttk.Label(self.frame1)
        self.label6.configure(text="Saturation")
        self.label6.place(anchor="nw", x="15", y="85")
        self.scale3 = ttk.Scale(self.frame1)
        self.upper_saturation = tk.IntVar(value=self.upper_skin[1])
        self.scale3.configure(
            from_="0", orient="horizontal", to="255", variable=self.upper_saturation
        )
        self.scale3.place(anchor="nw", relwidth=".16", x="15", y="112")
        self.scale3.configure(command=self.updateHSV)
        self.scale4 = ttk.Scale(self.frame1)
        self.lower_saturation = tk.IntVar(value=self.lower_skin[1])
        self.scale4.configure(
            from_="0", orient="horizontal", to="255", variable=self.lower_saturation
        )
        self.scale4.place(anchor="nw", relwidth=".16", x="15", y="134")
        self.scale4.configure(command=self.updateHSV)
        self.entry4 = ttk.Entry(self.frame1)
        self.entry4.configure(justify="center", textvariable=self.upper_saturation)
        self.entry4.delete("0", "end")
        self.entry4.insert("0", self.upper_skin[1])
        self.entry4.place(anchor="nw", relwidth=".024", x="205", y="112")
        self.entry5 = ttk.Entry(self.frame1)
        self.entry5.configure(justify="center", textvariable=self.lower_saturation)
        self.entry5.delete("0", "end")
        self.entry5.insert("0", self.lower_skin[1])
        self.entry5.place(anchor="nw", relwidth=".024", x="205", y="134")
        self.label7 = ttk.Label(self.frame1)
        self.label7.configure(text="Upper")
        self.label7.place(anchor="nw", x="238", y="112")
        self.label8 = ttk.Label(self.frame1)
        self.label8.configure(text="Lower")
        self.label8.place(anchor="nw", x="238", y="134")
        self.label9 = ttk.Label(self.frame1)
        self.label9.configure(text="______")
        self.label9.place(anchor="nw", x="15", y="162")
        self.label10 = ttk.Label(self.frame1)
        self.label10.configure(text="Value")
        self.label10.place(anchor="nw", x="15", y="158")
        self.scale5 = ttk.Scale(self.frame1)
        self.upper_value = tk.IntVar(value=self.upper_skin[2])
        self.scale5.configure(
            from_="0", orient="horizontal", to="255", variable=self.upper_value
        )
        self.scale5.place(anchor="nw", relwidth=".16", x="15", y="184")
        self.scale5.configure(command=self.updateHSV)
        self.scale6 = ttk.Scale(self.frame1)
        self.lower_value = tk.IntVar(value=self.lower_skin[2])
        self.scale6.configure(
            from_="0", orient="horizontal", to="255", variable=self.lower_value
        )
        self.scale6.place(anchor="nw", relwidth=".16", x="15", y="206")
        self.scale6.configure(command=self.updateHSV)
        self.entry6 = ttk.Entry(self.frame1)
        self.entry6.configure(justify="center", textvariable=self.upper_value)
        self.entry6.delete("0", "end")
        self.entry6.insert("0", self.upper_skin[2])
        self.entry6.place(anchor="nw", relwidth=".024", x="205", y="184")
        self.entry7 = ttk.Entry(self.frame1)
        self.entry7.configure(justify="center", textvariable=self.lower_value)
        self.entry7.delete("0", "end")
        self.entry7.insert("0", self.lower_skin[2])
        self.entry7.place(anchor="nw", relwidth=".024", x="205", y="206")
        self.label11 = ttk.Label(self.frame1)
        self.label11.configure(text="Upper")
        self.label11.place(anchor="nw", x="238", y="184")
        self.label12 = ttk.Label(self.frame1)
        self.label12.configure(text="Lower")
        self.label12.place(anchor="nw", x="238", y="206")
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text="Save & Exit")
        self.button1.place(anchor="nw", relwidth="0.14", x="100", y="238")
        self.button1.configure(command=self.saveExit)
        self.button2 = ttk.Button(self.frame1)
        self.button2.configure(text="Exit")
        self.button2.place(anchor="nw", x="15", y="238")
        self.button2.configure(command=self.exit)
        self.video_panel = ttk.Label(self.frame1)
        self.video_panel.place(anchor="nw", height="480", width="852", x="275", y="0")
        self.current_image = None
        self.frame1.configure(height="200", width="200")
        self.frame1.pack(side="top")

        # Main widget
        self.mainwindow = self.frame1

        self.videoLoop()

    def videoLoop(self):
        # used to display the video in the config menu
        _, img = self.cap.read()
        img = cv.resize(img, self.IMAGE_DIMENSIONS)
        img = cv.flip(img, 1)
        img = cv.GaussianBlur(img, (5, 5), 0)

        # converts image bgr -> hsv and removes colors that are not in range
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, self.lower_skin, self.upper_skin)
        mask = cv.bitwise_not(mask)
        res = cv.bitwise_and(img, img, mask=mask)

        #puts image into tk window
        cvimage = cv.cvtColor(res, cv.COLOR_BGR2RGBA)
        self.current_image = Image.fromarray(cvimage)
        imgtk = ImageTk.PhotoImage(image=self.current_image)
        self.video_panel.imgtk = imgtk
        self.video_panel.config(image=imgtk)

        self.root.after(30, self.videoLoop)

    def updateHSV(self, scale_value):
        # when value sliders are moved

        # keeps set values to whole numbers
        self.lower_hue.set(round(self.lower_hue.get()))
        self.upper_hue.set(round(self.upper_hue.get()))
        self.lower_saturation.set(round(self.lower_saturation.get()))
        self.upper_saturation.set(round(self.upper_saturation.get()))
        self.lower_value.set(round(self.lower_value.get()))
        self.upper_value.set(round(self.upper_value.get()))

        # make sure values dont overlap
        if self.lower_hue.get() > self.upper_hue.get():
            self.upper_hue.set(self.lower_hue.get())
        if self.lower_saturation.get() > self.upper_saturation.get():
            self.upper_saturation.set(self.lower_saturation.get())
        if self.lower_value.get() > self.upper_value.get():
            self.upper_value.set(self.lower_value.get())

        # sets upper and lower hsv values
        self.lower_skin = np.array(
            [self.lower_hue.get(), self.lower_saturation.get(), self.lower_value.get()]
        )
        self.upper_skin = np.array(
            [self.upper_hue.get(), self.upper_saturation.get(), self.upper_value.get()]
        )

    def saveExit(self):
        #saves calibration values on save & exit
        config = ConfigParser()
        file = "config.ini"
        config.read(file)

        config.set("Calibration", "lower_hue", str(self.lower_hue.get()))
        config.set("Calibration", "lower_saturation", str(self.lower_saturation.get()))
        config.set("Calibration", "lower_value", str(self.lower_value.get()))
        config.set("Calibration", "upper_hue", str(self.upper_hue.get()))
        config.set("Calibration", "upper_saturation", str(self.upper_saturation.get()))
        config.set("Calibration", "upper_value", str(self.upper_value.get()))

        with open(file, "w") as configfile:
            config.write(configfile)

        self.root.destroy()

    def exit(self):
        self.root.destroy()

    def initalCalibration(self):

        # this is used for giving the user an estimate for the calibration settings when they left click on their hand
        def selectRGBValue(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN:  # checks mouse left button down condition

                colors = [0] * 3
                colors[0] = hsv[y, x, 0]  # Hue
                colors[1] = hsv[y, x, 1]  # Saturation
                colors[2] = hsv[y, x, 2]  # Value

                # making sure guesstimated hue isnt going to be out of bounds
                if colors[0] > 240:
                    colors[0] = 240
                elif colors[0] < 15:
                    colors[0] = 15

                self.lower_skin = np.array([colors[0] - 15, 20, 80])
                self.upper_skin = np.array([colors[0] + 15, 255, 230])

        # initializing capture window
        cap = cv.VideoCapture(self.webcam_ip)
        cv.namedWindow("Calibration Menu")
        cv.setMouseCallback("Calibration Menu", selectRGBValue)

        while True:

            # reads and resizes image
            _, img = cap.read()
            img = cv.resize(img, self.IMAGE_DIMENSIONS)
            img = cv.flip(img, 1)
            img = cv.blur(img, (5, 5))

            # converts image rgb -> hsv and removes colors that are not in range
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, self.lower_skin, self.upper_skin)
            mask = cv.bitwise_not(mask)
            res = cv.bitwise_and(img, img, mask=mask)

            res = cv.putText(
                res,
                "Click around your hand till its nearly completely black and press the key 'f'",
                (19, 19),
                cv.FONT_HERSHEY_PLAIN,
                1.25,
                (0, 0, 0),
                1,
                cv.LINE_AA,
            )
            res = cv.putText(
                res,
                "Click around your hand till its nearly completely black and press the key 'f'",
                (21, 21),
                cv.FONT_HERSHEY_PLAIN,
                1.25,
                (0, 0, 0),
                1,
                cv.LINE_AA,
            )
            res = cv.putText(
                res,
                "Click around your hand till its nearly completely black and press the key 'f'",
                (20, 20),
                cv.FONT_HERSHEY_PLAIN,
                1.25,
                (0, 0, 255),
                1,
                cv.LINE_AA,
            )
            cv.imshow("Calibration Menu", res)

            # press key to stop program
            if cv.waitKey(1) & 0xFF == ord("f"):
                break

        cv.destroyAllWindows()
