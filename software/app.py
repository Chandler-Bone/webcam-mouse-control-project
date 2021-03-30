import tkinter as tk
import tkinter.ttk as ttk
import os


class WebcamguiApp:
    def __init__(self, master=None):
        # build ui
        self.frame1 = ttk.Frame(master)
        self.canvas = tk.Canvas(self.frame1)
        self.canvas.configure(height='300')
        self.canvas.pack(side='top')
        self.checkbutton1 = ttk.Checkbutton(self.frame1)
        use_ip_webcam = tk.BooleanVar(value=False)
        self.checkbutton1.configure(offvalue='False', onvalue='True', takefocus=False, text='IP Webcam')
        self.checkbutton1.configure(variable=use_ip_webcam)
        self.checkbutton1.place(anchor='nw', x='15', y='70')
        self.checkbutton2 = ttk.Checkbutton(self.frame1)
        self.checkbutton2.configure(cursor='arrow', offvalue='True', onvalue='False', text='Integrated Webcam (Recommended)')
        self.checkbutton2.configure(variable=use_ip_webcam)
        self.checkbutton2.place(anchor='nw', x='15', y='45')
        self.entry1 = ttk.Entry(self.frame1)
        webcam_ip = tk.StringVar(value="")
        self.entry1.configure(textvariable=webcam_ip)
        self.entry1.place(anchor='nw', relwidth='0.6', relx='0.0', x='120', y='70')
        self.label1 = ttk.Label(self.frame1)
        self.label1.configure(font='TkDefaultFont', text='_______________')
        self.label1.place(anchor='nw', x='15', y='22')
        self.label2 = ttk.Label(self.frame1)
        self.label2.configure(text='e.g. "https://192.168.0.11:8080/video"')
        self.label2.place(anchor='nw', x='137', y='92')
        self.label3 = ttk.Label(self.frame1)
        self.label3.configure(anchor='e', cursor='arrow', takefocus=False, text='Webcam Type')
        self.label3.place(anchor='nw', x='15', y='18')
        self.label4 = ttk.Label(self.frame1)
        self.label4.configure(font='TkDefaultFont', text='___________________')
        self.label4.place(anchor='nw', x='15', y='121')
        self.label5 = ttk.Label(self.frame1)
        self.label5.configure(text='Screen Resolution')
        self.label5.place(anchor='nw', x='15', y='117')
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text='Detect')
        self.button1.place(anchor='nw', x='175', y='142')
        self.button1.configure(command=self.detectResolution)
        self.entry2 = ttk.Entry(self.frame1)
        resolutionWidth = tk.IntVar(value=1920)
        self.entry2.configure(exportselection='true', state='normal', textvariable=resolutionWidth, validate='none')
        _text_ = '''1920'''
        self.entry2.delete('0', 'end')
        self.entry2.insert('0', _text_)
        self.entry2.place(anchor='nw', relwidth='0.16', x='20', y='146')
        self.entry3 = ttk.Entry(self.frame1)
        resolutionHeight = tk.IntVar(value=1080)
        self.entry3.configure(textvariable=resolutionHeight)
        _text_ = '''1080'''
        self.entry3.delete('0', 'end')
        self.entry3.insert('0', _text_)
        self.entry3.place(anchor='nw', relwidth='.16', x='105', y='146')
        self.label6 = ttk.Label(self.frame1)
        self.label6.configure(font='TkDefaultFont', style='Toolbutton', text='x')
        self.label6.place(anchor='nw', x='87', y='144')
        self.checkbutton3 = ttk.Checkbutton(self.frame1)
        is_debug = tk.BooleanVar(value=False)
        self.checkbutton3.configure(offvalue='False', onvalue='True', text='Debug', variable=is_debug)
        self.checkbutton3.place(anchor='nw', x='25', y='258')
        self.label7 = ttk.Label(self.frame1)
        self.label7.configure(text='____________')
        self.label7.place(anchor='nw', x='15', y='184')
        self.entry4 = ttk.Entry(self.frame1)
        lower_red = tk.IntVar(value=0
)
        self.entry4.configure(textvariable=lower_red)
        _text_ = '''0
'''
        self.entry4.delete('0', 'end')
        self.entry4.insert('0', _text_)
        self.entry4.place(anchor='nw', relwidth='.06', x='35', y='220')
        self.label8 = ttk.Label(self.frame1)
        self.label8.configure(text='Calibration')
        self.label8.place(anchor='nw', x='15', y='180')
        self.label9 = ttk.Label(self.frame1)
        self.label9.configure(text='Lower RGB Bounds')
        self.label9.place(anchor='nw', x='20', y='201')
        self.entry5 = ttk.Entry(self.frame1)
        lower_green = tk.IntVar(value=0)
        self.entry5.configure(textvariable=lower_green)
        _text_ = '''0'''
        self.entry5.delete('0', 'end')
        self.entry5.insert('0', _text_)
        self.entry5.place(anchor='nw', relwidth='.06', x='60', y='220')
        self.entry6 = ttk.Entry(self.frame1)
        lower_blue = tk.IntVar(value=0)
        self.entry6.configure(textvariable=lower_blue)
        _text_ = '''0'''
        self.entry6.delete('0', 'end')
        self.entry6.insert('0', _text_)
        self.entry6.place(anchor='nw', relwidth='.06', x='85', y='220')
        self.label9 = ttk.Label(self.frame1)
        self.label9.configure(text='-')
        self.label9.place(anchor='nw', x='130', y='220')
        self.label10 = ttk.Label(self.frame1)
        self.label10.configure(text='Upper RGB Bounds')
        self.label10.place(anchor='nw', x='145', y='201')
        self.entry7 = ttk.Entry(self.frame1)
        upper_red = tk.IntVar(value=225)
        self.entry7.configure(textvariable=upper_red)
        _text_ = '''225'''
        self.entry7.delete('0', 'end')
        self.entry7.insert('0', _text_)
        self.entry7.place(anchor='nw', relwidth='.06', x='160', y='220')
        self.entry8 = ttk.Entry(self.frame1)
        upper_green = tk.IntVar(value=225)
        self.entry8.configure(textvariable=upper_green)
        _text_ = '''225'''
        self.entry8.delete('0', 'end')
        self.entry8.insert('0', _text_)
        self.entry8.place(anchor='nw', relwidth='.06', x='185', y='220')
        self.entry9 = ttk.Entry(self.frame1)
        upper_blue = tk.IntVar(value=225)
        self.entry9.configure(textvariable=upper_blue)
        _text_ = '''225'''
        self.entry9.delete('0', 'end')
        self.entry9.insert('0', _text_)
        self.entry9.place(anchor='nw', relwidth='.06', x='210', y='220')
        self.button2 = ttk.Button(self.frame1)
        self.button2.configure(text='Calibrate')
        self.button2.place(anchor='nw', relwidth='0.25', x='262', y='207')
        self.button2.configure(command=self.calibrateRGBBounds)
        self.button3 = ttk.Button(self.frame1)
        self.button3.configure(text='Website')
        self.button3.place(anchor='nw', relwidth='0.3', x='246', y='15')
        self.button3.configure(command=self.websiteLink)
        self.button4 = ttk.Button(self.frame1)
        self.button4.configure(text='Save Settings')
        self.button4.place(anchor='nw', x='100', y='255')
        self.button4.configure(command=self.saveSettings)
        self.button5 = ttk.Button(self.frame1)
        self.button5.configure(text='START')
        self.button5.place(anchor='nw', relwidth='0.4', x='205', y='255')
        self.button5.configure(command=self.start)
        self.frame1.configure(height='200', width='200')
        self.frame1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame1

    def detectResolution(self):
        pass

    def calibrateRGBBounds(self):
        pass

    def websiteLink(self):
        pass

    def saveSettings(self):
        pass

    def start(self):
        pass

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()

    cur_path = os.path.dirname(os.path.abspath(__file__))
    root.iconbitmap(cur_path + '\\hand_icon.ico')
    root.title("Webcam Hand Control")

    app = WebcamguiApp(root)
    app.run()

