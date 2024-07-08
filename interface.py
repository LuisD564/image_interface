import time
import threading
import tkinter as tk
from PIL import ImageTk, Image
import psutil
import gc

from get_images import GetImages
from cnn_model import MLModel


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._looping    = False
        self.check_FRONT = False

        #_________Start/Stop button_____________________
        self.frame0 = tk.Frame(self)
        self.frame0.grid(row = 0, column = 0)
        self.frame1 = tk.Frame(self)
        self.frame1.grid(row = 1, column = 0)
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row = 2, column = 0)
        self.frame3 = tk.Frame(self)
        self.frame3.grid(row = 3, column = 0)

        button1 = tk.Button(self.frame0, text = "Start/Stop", command = self._on_button1)
        button1.pack()

        #________Filter selection and type of illumination device_______________
        # filter
        self.type_filter = tk.Label(self.frame0, text = "Select the type of light:", bd=10)
        self.type_filter.pack()
        self.var_filter = tk.StringVar()
        radio_button1 = tk.Radiobutton(self.frame0, text = "IR  ", variable = self.var_filter, value = "IR")
        radio_button1.pack()
        radio_button2 = tk.Radiobutton(self.frame0, text = "VIS ", variable  = self.var_filter, value = "VIS")
        radio_button2.pack()
        radio_button3 = tk.Radiobutton(self.frame0, text = "UV  ", variable = self.var_filter, value = "UV")
        radio_button3.pack()


        #_________________Illumination device_______________
        #type of illumination
        self.type_filter = tk.Label(self.frame0, text = "Select your device:", bd = 10)
        self.type_filter.pack()
        TOP_button = tk.Checkbutton(self.frame0, text = "TOP  ", command=self._TOP_light)
        TOP_button.pack()
        FRONT_button = tk.Checkbutton(self.frame0, text = "FRONT", command=self._FRONT_light)
        FRONT_button.pack()
        BACK_button = tk.Checkbutton(self.frame0, text="BACK", command=self._BACK_light)
        BACK_button.pack()

        #_______________________Adjust Time Sleep_____________________
        #Time Sleep
        self.time_to_sleep = tk.Label(self.frame1, text = "Adjust Time Sleep:", bd=10)
        self.time_to_sleep.pack()
        self.time_to_sleep_entry = tk.Entry(self.frame1, width = 5)
        self.time_to_sleep_entry.pack()

        #Brightness
        self.front_brightness_label = tk.Label(self.frame1, text = "FRONT(U) TOP(M) BACK(D) brightness:", bd = 10)
        self.front_brightness_label.pack()
        self.brightness_front_entry = tk.Scale(self.frame1, from_= 0, to = 100, orient = 'horizontal', sliderlength = 15)
        self.brightness_front_entry.pack()
        # self.top_brightness_label = tk.Label(self.frame1, text = "TOP brightness value:", bd = 10)
        # self.top_brightness_label.pack()
        self.brightness_top_entry = tk.Scale(self.frame1, from_ = 0, to = 100, orient = 'horizontal', sliderlength = 15)
        self.brightness_top_entry.pack()
        self.brightness_back_entry = tk.Scale(self.frame1, from_=0, to=100, orient='horizontal', sliderlength=15)
        self.brightness_back_entry.pack()

        #Exposition Time
        self.exposition_time_front_label = tk.Label(self.frame2, text = "FRONT(U) TOP(M) BACK(D) Exp.time (ms):", bd = 10)
        self.exposition_time_front_label.pack()
        self.exposition_time_front = tk.Entry(self.frame2, text="FRONT", width = 5)
        self.exposition_time_front.pack()
        self.exposition_time_top = tk.Entry(self.frame2, text="TOP", width = 5)
        self.exposition_time_top.pack()
        self.exposition_time_back = tk.Entry(self.frame2, text="BACK", width=5)
        self.exposition_time_back.pack()

        #_____________________Analog Gain________________________
        self.gain_label = tk.Label(self.frame3, text = "Analog gain value:", bd = 10)
        self.gain_label.pack()
        self.gain = tk.Scale(self.frame3, from_=0, to = 4, orient='horizontal')
        self.gain.pack()

        #_______________Display Smartex Logo__________________
        self.smartex_image = ImageTk.PhotoImage(file = 'logo.png')
        self.smx_label = tk.Label(self, image = self.smartex_image)
        self.smx_label.grid(row=4, column=0, padx = 0, pady = 0)


        #____________________Load Cameras____________________________
        self.lp = GetImages()
        self.ml_model = MLModel()
        self._display_photos()

    def _on_button1(self):
        self._looping = not self._looping

    def _check_filter(self):
        return self.var_filter.get()

    def _TOP_light(self):
        self.check_TOP = not self.check_TOP

    def _FRONT_light(self):
        self.check_FRONT = not self.check_FRONT

    def _BACK_light(self):
        self.check_BACK = not self.check_BACK

    def _brightness_front(self):
        return int(self.brightness_front_entry.get())

    def _brightness_top(self):
        return int(self.brightness_top_entry.get())

    def _brightness_back(self):
        return int(self.brightness_back_entry.get())

    def _exposition_time_front(self):
        return int(self.exposition_time_front.get())

    def _exposition_time_top(self):
        return int(self.exposition_time_top.get())

    def _exposition_time_back(self):
        return int(self.exposition_time_back.get())

    def _gain(self):
        return int(self.gain.get())

    def _time_to_sleep(self):
        return int(self.time_to_sleep_entry.get())

    def _clean_labels(self):
        if self.check_FRONT == True:
            self.master.unbind("<Button-1>")
            for label in self.labels_FRONT:
                label.destroy()
            gc.collect()

    def _display_photos(self):
        if self._looping:
            if not self._check_filter() or (self.check_FRONT == False):
                print('Not all parameters were filled in!')
                self._looping == False
                pass

            if self.check_FRONT:
                batch = self.lp.loop()

                front_top_threading = threading.Thread(target=self.show_front, args=(batch, ))
                front_top_threading.start()

        self.after(10000, self._display_photos)

    def show_front(self, batch):
        def open_image_window_front_1():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][0])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[0])
            image_label.pack()

        def open_image_window_front_2():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][1])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[1])
            image_label.pack()

        def open_image_window_front_3():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][2])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[2])
            image_label.pack()

        def open_image_window_front_4():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][3])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[3])
            image_label.pack()

        def open_image_window_front_5():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][4])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[4])
            image_label.pack()

        def open_image_window_front_6():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][5])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[5])
            image_label.pack()

        def open_image_window_front_7():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][6])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[6])
            image_label.pack()

        def open_image_window_front_8():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][7])
            image_label = tk.Label(image_window, image=images_to_pop_up_FRONT[7])
            image_label.pack()

        def image_clicked_front_1(event):
            open_image_window_front_1()

        def image_clicked_front_2(event):
            open_image_window_front_2()

        def image_clicked_front_3(event):
            open_image_window_front_3()

        def image_clicked_front_4(event):
            open_image_window_front_4()

        def image_clicked_front_5(event):
            open_image_window_front_5()

        def image_clicked_front_6(event):
            open_image_window_front_6()

        def image_clicked_front_7(event):
            open_image_window_front_7()

        def image_clicked_front_8(event):
            open_image_window_front_8()

        images_to_show_FRONT = []
        images_to_pop_up_FRONT = []
        for filename in batch[0]:
            image_open = Image.open(filename)
            resized_image = image_open.resize((384, 240))
            resized_image_pop_up = image_open.resize((1152, 720))
            images_to_show_FRONT.append(ImageTk.PhotoImage(resized_image))
            images_to_pop_up_FRONT.append(ImageTk.PhotoImage(resized_image_pop_up))

        self.labels_FRONT = []
        for i, image_to_show in enumerate(images_to_show_FRONT):
            label = tk.Label(self, image=image_to_show)
            label.image = image_to_show  # Keep a reference to prevent garbage collection
            row = (i // 4)
            column = (i % 4) + 1
            label.grid(row=row, column=column, padx=0, pady=0)
            self.labels_FRONT.append(label)

        for i in range(self.lp.number_of_cameras):
            self.labels_FRONT[i].bind("<Button-1>", eval(f'image_clicked_front_{i + 1}'))

        self.front_legend_label = tk.Label(self, text=f'Front_{batch[1]}')
        self.front_legend_label.grid(row=0, column=1, sticky='NW')

        print('RAM memory % used:', psutil.virtual_memory()[2])
        print('RAM Used (GB):', psutil.virtual_memory()[3] / 1000000000)
        print('The CPU usage is: ', psutil.cpu_percent(4))
        time.sleep(self._time_to_sleep())
        self._clean_labels()


