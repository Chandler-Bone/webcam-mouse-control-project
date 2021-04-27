import os
import re
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import END
from configparser import ConfigParser
import logging
import webbrowser
import sys

from calibrate_detection import CalibrateDetection
from hand_detection import HandDetection


class WebcamguiApp:
    def __init__(self, master=None):

        self.root = tk.Tk()

        #add icon to window
        icon = "hand_icon.ico" 
        if not hasattr(sys, "frozen"):
            icon = os.path.join(os.path.dirname(__file__), icon) 
        else:  
            icon = os.path.join(sys.prefix, icon)
        self.root.iconbitmap(default=icon)

        #rename window and make window not resizable
        self.root.title("Webcam Hand Control")
        self.root.resizable(False, False)

        # this was UI was built using pygubu and i recommend ignoring this
        self.frame1 = ttk.Frame(master)
        self.canvas = tk.Canvas(self.frame1)
        self.canvas.configure(height="300")
        self.canvas.configure(width="375")
        self.canvas.pack(side="top")
        self.checkbutton1 = ttk.Checkbutton(self.frame1)
        self.use_ip_webcam = tk.IntVar(value=0)
        self.checkbutton1.configure(
            offvalue=0, onvalue=1, takefocus=False, text="IP Webcam"
        )
        self.checkbutton1.configure(variable=self.use_ip_webcam)
        self.checkbutton1.place(anchor="nw", x="15", y="70")
        self.checkbutton2 = ttk.Checkbutton(self.frame1)
        self.checkbutton2.configure(
            cursor="arrow",
            offvalue=1,
            onvalue=0,
            text="Integrated Webcam (Recommended)",
        )
        self.checkbutton2.configure(variable=self.use_ip_webcam)
        self.checkbutton2.place(anchor="nw", x="15", y="45")
        self.entry1 = ttk.Entry(self.frame1)
        self.webcam_ip = tk.StringVar(value="")
        self.entry1.configure(textvariable=self.webcam_ip)
        self.entry1.place(anchor="nw", relwidth="0.6", relx="0.0", x="120", y="70")
        self.label1 = ttk.Label(self.frame1)
        self.label1.configure(font="TkDefaultFont", text="_______________")
        self.label1.place(anchor="nw", x="15", y="22")
        self.label2 = ttk.Label(self.frame1)
        self.label2.configure(text='e.g. "https://192.168.0.11:8080/video"')
        self.label2.place(anchor="nw", x="137", y="92")
        self.label3 = ttk.Label(self.frame1)
        self.label3.configure(
            anchor="e", cursor="arrow", takefocus=False, text="Webcam Type"
        )
        self.label3.place(anchor="nw", x="15", y="18")
        self.label4 = ttk.Label(self.frame1)
        self.label4.configure(font="TkDefaultFont", text="___________________")
        self.label4.place(anchor="nw", x="15", y="121")
        self.label5 = ttk.Label(self.frame1)
        self.label5.configure(text="Screen Resolution")
        self.label5.place(anchor="nw", x="15", y="117")
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text="Detect")
        self.button1.place(anchor="nw", x="175", y="142")
        self.button1.configure(command=self.detectResolution)
        self.entry2 = ttk.Entry(self.frame1)
        self.resolution_width = tk.IntVar(value=1920)
        self.entry2.configure(
            exportselection="true",
            state="normal",
            textvariable=self.resolution_width,
            validate="none",
        )
        self._text_ = """1920"""
        self.entry2.delete("0", "end")
        self.entry2.insert("0", self._text_)
        self.entry2.place(anchor="nw", relwidth="0.16", x="20", y="146")
        self.entry3 = ttk.Entry(self.frame1)
        self.resolution_height = tk.IntVar(value=1080)
        self.entry3.configure(textvariable=self.resolution_height)
        self._text_ = """1080"""
        self.entry3.delete("0", "end")
        self.entry3.insert("0", self._text_)
        self.entry3.place(anchor="nw", relwidth=".16", x="105", y="146")
        self.label6 = ttk.Label(self.frame1)
        self.label6.configure(font="TkDefaultFont", style="Toolbutton", text="x")
        self.label6.place(anchor="nw", x="87", y="144")
        self.checkbutton3 = ttk.Checkbutton(self.frame1)
        self.is_debug = tk.IntVar(value=0)
        self.checkbutton3.configure(
            offvalue=0, onvalue=1, text="Debug", variable=self.is_debug
        )
        self.checkbutton3.place(anchor="nw", x="25", y="256")
        self.label7 = ttk.Label(self.frame1)
        self.label7.configure(text="____________")
        self.label7.place(anchor="nw", x="15", y="184")
        self.entry4 = ttk.Entry(self.frame1)
        self.lower_hue = tk.IntVar(value=0)
        self.entry4.configure(textvariable=self.lower_hue)
        self._text_ = """0"""
        self.entry4.delete("0", "end")
        self.entry4.insert("0", self._text_)
        self.entry4.place(anchor="nw", relwidth=".06", x="35", y="220")
        self.label8 = ttk.Label(self.frame1)
        self.label8.configure(text="Calibration")
        self.label8.place(anchor="nw", x="15", y="180")
        self.label9 = ttk.Label(self.frame1)
        self.label9.configure(text="Lower HSV Bounds")
        self.label9.place(anchor="nw", x="20", y="201")
        self.entry5 = ttk.Entry(self.frame1)
        self.lower_saturation = tk.IntVar(value=0)
        self.entry5.configure(textvariable=self.lower_saturation)
        self._text_ = """0"""
        self.entry5.delete("0", "end")
        self.entry5.insert("0", self._text_)
        self.entry5.place(anchor="nw", relwidth=".06", x="60", y="220")
        self.entry6 = ttk.Entry(self.frame1)
        self.lower_value = tk.IntVar(value=0)
        self.entry6.configure(textvariable=self.lower_value)
        self._text_ = """0"""
        self.entry6.delete("0", "end")
        self.entry6.insert("0", self._text_)
        self.entry6.place(anchor="nw", relwidth=".06", x="85", y="220")
        self.label9 = ttk.Label(self.frame1)
        self.label9.configure(text="-")
        self.label9.place(anchor="nw", x="130", y="220")
        self.label10 = ttk.Label(self.frame1)
        self.label10.configure(text="Upper HSV Bounds")
        self.label10.place(anchor="nw", x="145", y="201")
        self.entry7 = ttk.Entry(self.frame1)
        self.upper_hue = tk.IntVar(value=225)
        self.entry7.configure(textvariable=self.upper_hue)
        self._text_ = """255"""
        self.entry7.delete("0", "end")
        self.entry7.insert("0", self._text_)
        self.entry7.place(anchor="nw", relwidth=".06", x="160", y="220")
        self.entry8 = ttk.Entry(self.frame1)
        self.upper_saturation = tk.IntVar(value=225)
        self.entry8.configure(textvariable=self.upper_saturation)
        self._text_ = """255"""
        self.entry8.delete("0", "end")
        self.entry8.insert("0", self._text_)
        self.entry8.place(anchor="nw", relwidth=".06", x="185", y="220")
        self.entry9 = ttk.Entry(self.frame1)
        self.upper_value = tk.IntVar(value=225)
        self.entry9.configure(textvariable=self.upper_value)
        self._text_ = """255"""
        self.entry9.delete("0", "end")
        self.entry9.insert("0", self._text_)
        self.entry9.place(anchor="nw", relwidth=".06", x="210", y="220")
        self.button2 = ttk.Button(self.frame1)
        self.button2.configure(text="Calibrate")
        self.button2.place(anchor="nw", relwidth="0.25", x="262", y="207")
        self.button2.configure(command=self.calibrateHSVBounds)
        self.button3 = ttk.Button(self.frame1)
        self.button3.configure(text="Website")
        self.button3.place(anchor="nw", relwidth="0.3", x="246", y="15")
        self.button3.configure(command=self.websiteLink)
        self.button4 = ttk.Button(self.frame1)
        self.button4.configure(text="Save Settings")
        self.button4.place(anchor="nw", x="100", y="255")
        self.button4.configure(command=self.saveSettings)
        self.button5 = ttk.Button(self.frame1)
        self.button5.configure(text="START")
        self.button5.place(anchor="nw", relwidth="0.4", x="205", y="255")
        self.button5.configure(command=self.start)
        self.frame1.configure(height="200", width="200")
        self.frame1.pack(side="top")

        # Main widget
        self.mainwindow = self.frame1

        self.loadSettings()

    def detectResolution(self):
        # get screen geometry
        self.root.attributes("-fullscreen", True)
        self.root.state("iconic")
        geometry = self.root.winfo_geometry()
        self.root.state("normal")
        self.root.attributes("-fullscreen", False)

        resolutions = re.findall(r"[0-9]+", geometry)

        self.resolution_width.set(resolutions[0])
        self.resolution_height.set(resolutions[1])

    def calibrateHSVBounds(self):
        self.saveSettings()
        # gets rid of gui and starts calibration menu with settings
        # the calibration menu does not like the main menu still being open
        self.root.destroy()

        hand_calibration = CalibrateDetection(
            self.use_ip_webcam.get(), self.webcam_ip.get()
        )

        hand_calibration.initalCalibration()
        hand_calibration.loadGUI()
        # starts gui
        hand_calibration.root.mainloop()

        # reopens main menu gui and runs it
        self.__init__()
        self.run()

    def websiteLink(self):
        webbrowser.open("https://github.com/ChandlerBoneGSU/SE-Project-Team1")

    def loadSettings(self):
        config = ConfigParser()
        file = "config.ini"
        config.read(file)

        # if config is configured then load values
        if config.sections() != []:

            # loading of values into their respective variables
            self.use_ip_webcam.set(config.getint("Webcam", "use_ip_webcam"))
            self.webcam_ip.set(config.get("Webcam", "webcam_ip"))

            self.resolution_width.set(
                config.get("Screen Resolution", "resolution_width")
            )
            self.resolution_height.set(
                config.get("Screen Resolution", "resolution_height")
            )

            self.lower_hue.set(config.get("Calibration", "lower_hue"))
            self.lower_saturation.set(config.get("Calibration", "lower_saturation"))
            self.lower_value.set(config.get("Calibration", "lower_value"))
            self.upper_hue.set(config.get("Calibration", "upper_hue"))
            self.upper_saturation.set(config.get("Calibration", "upper_saturation"))
            self.upper_value.set(config.get("Calibration", "upper_value"))

            self.is_debug.set(config.get("Debug", "is_debug"))

    def saveSettings(self):
        # this creates a config file and stores all the variables from the user
        config = ConfigParser()
        file = "config.ini"

        config.add_section("Webcam")
        config.set("Webcam", "use_ip_webcam", str(self.use_ip_webcam.get()))
        config.set("Webcam", "webcam_ip", self.webcam_ip.get())

        config.add_section("Screen Resolution")
        config.set(
            "Screen Resolution", "resolution_width", str(self.resolution_width.get())
        )
        config.set(
            "Screen Resolution", "resolution_height", str(self.resolution_height.get())
        )

        config.add_section("Calibration")
        config.set("Calibration", "lower_hue", str(self.lower_hue.get()))
        config.set("Calibration", "lower_saturation", str(self.lower_saturation.get()))
        config.set("Calibration", "lower_value", str(self.lower_value.get()))
        config.set("Calibration", "upper_hue", str(self.upper_hue.get()))
        config.set("Calibration", "upper_saturation", str(self.upper_saturation.get()))
        config.set("Calibration", "upper_value", str(self.upper_value.get()))

        config.add_section("Debug")
        config.set("Debug", "is_debug", str(self.is_debug.get()))

        with open(file, "w") as configfile:
            config.write(configfile)

    def start(self):
        # gets rid of gui and starts cursor movement portion
        self.root.destroy()

        # uses inputs and starts the hand-cursor detection
        hand_detection = HandDetection(
            self.use_ip_webcam.get(),
            self.webcam_ip.get(),
            self.resolution_width.get(),
            self.resolution_height.get(),
            self.lower_hue.get(),
            self.lower_saturation.get(),
            self.lower_value.get(),
            self.upper_hue.get(),
            self.upper_saturation.get(),
            self.upper_value.get(),
            self.is_debug.get(),
        )
        hand_detection.run()

        # reopens main menu gui and runs it
        self.__init__()
        self.run()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    logging.basicConfig(filename="webcamhandcontrol.log", filemode="w")
    try:
        app = WebcamguiApp()
        app.run()
    except:
        logging.exception("failure detected")
