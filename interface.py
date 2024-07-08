import time
import threading
import tkinter as tk
from PIL import ImageTk, Image
import psutil
import gc

from get_images import GetImages


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._looping    = False

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

        #_______________________Adjust Time Sleep_____________________
        #Time Sleep
        self.time_to_sleep = tk.Label(self.frame1, text = "Sleep between images:", bd=10)
        self.time_to_sleep.pack()
        self.time_to_sleep_entry = tk.Entry(self.frame1, width = 5)
        self.time_to_sleep_entry.pack()

        #ML settings
        self.probability_of_having_circle = tk.Label(self.frame2, text ="Probability of having a circle (%):", bd = 10)
        self.probability_of_having_circle.pack()
        self.probability_of_having_circle_box = tk.Entry(self.frame2, text="FRONT", width = 5)
        self.probability_of_having_circle_box.pack()

        self.number_of_epochs = tk.Label(self.frame2, text="Number of epochs:", bd=10)
        self.number_of_epochs.pack()
        self.number_of_epochs_box = tk.Entry(self.frame2, text="TOP", width = 5)
        self.number_of_epochs_box.pack()

        self.batch_size = tk.Label(self.frame2, text="Batch size:", bd=10)
        self.batch_size.pack()
        self.batch_size_box = tk.Entry(self.frame2, text="BACK", width=5)
        self.batch_size_box.pack()

        self.validation_split = tk.Label(self.frame2, text="Validation Split:", bd=10)
        self.validation_split.pack()
        self.validation_split_box = tk.Entry(self.frame2, width=5)
        self.validation_split_box.pack()

        #_______________Display Smartex Logo__________________
        self.smartex_image = ImageTk.PhotoImage(file = 'logo.png')
        self.smx_label = tk.Label(self, image = self.smartex_image)
        self.smx_label.grid(row=4, column=0, padx = 0, pady = 0)


        #____________________Initialization____________________________
        self.ml_model_loaded = False
        self._display_photos()

    def _on_button1(self):
        self._looping = not self._looping

    def _probability_of_having_circle(self) -> int:
        return int(self.probability_of_having_circle_box.get())

    def _number_of_epochs(self) -> int:
        return int(self.number_of_epochs_box.get())

    def _batch_size(self) -> int:
        return int(self.batch_size_box.get())

    def _validation_split(self) -> float:
        return float(self.validation_split_box.get())

    def _time_to_sleep(self) -> int:
        return int(self.time_to_sleep_entry.get())

    def _clean_labels(self) -> None:
        self.master.unbind("<Button-1>")
        for label in self.image_labels:
            label.destroy()
        gc.collect()

    def _display_photos(self) -> None:
        if self._looping:
            if not self.ml_model_loaded:
                self.load_ml_model()

            batch = self.lp.loop(self._probability_of_having_circle())
            front_top_threading = threading.Thread(target=self.show_front, args=(batch, ))
            front_top_threading.start()

        self.after(10000, self._display_photos)

    def load_ml_model(self) -> None:
        self.lp = GetImages(number_of_epochs=self._number_of_epochs(),
                            batch_size=self._batch_size(),
                            validation_split=self._validation_split())
        self.ml_model_loaded = True

    def show_front(self, batch) -> None:
        def open_image_window_1():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][0])
            image_label = tk.Label(image_window, image=images_to_pop_up[0])
            image_label.pack()

        def open_image_window_2():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][1])
            image_label = tk.Label(image_window, image=images_to_pop_up[1])
            image_label.pack()

        def open_image_window_3():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][2])
            image_label = tk.Label(image_window, image=images_to_pop_up[2])
            image_label.pack()

        def open_image_window_4():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][3])
            image_label = tk.Label(image_window, image=images_to_pop_up[3])
            image_label.pack()

        def open_image_window_5():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][4])
            image_label = tk.Label(image_window, image=images_to_pop_up[4])
            image_label.pack()

        def open_image_window_6():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][5])
            image_label = tk.Label(image_window, image=images_to_pop_up[5])
            image_label.pack()

        def open_image_window_7():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][6])
            image_label = tk.Label(image_window, image=images_to_pop_up[6])
            image_label.pack()

        def open_image_window_8():
            image_window = tk.Toplevel(self)
            image_window.title(batch[0][7])
            image_label = tk.Label(image_window, image=images_to_pop_up[7])
            image_label.pack()

        def image_clicked_1(event):
            open_image_window_1()

        def image_clicked_2(event):
            open_image_window_2()

        def image_clicked_3(event):
            open_image_window_3()

        def image_clicked_4(event):
            open_image_window_4()

        def image_clicked_5(event):
            open_image_window_5()

        def image_clicked_6(event):
            open_image_window_6()

        def image_clicked_7(event):
            open_image_window_7()

        def image_clicked_8(event):
            open_image_window_8()

        images_to_show = []
        images_to_pop_up = []
        for filename in batch[0]:
            image_open = Image.open(filename)
            resized_image = image_open.resize((384, 240))
            resized_image_pop_up = image_open.resize((1152, 720))
            images_to_show.append(ImageTk.PhotoImage(resized_image))
            images_to_pop_up.append(ImageTk.PhotoImage(resized_image_pop_up))

        self.image_labels = []
        for i, image_to_show in enumerate(images_to_show):
            label = tk.Label(self, image=image_to_show)
            label.image = image_to_show  # Keep a reference to prevent garbage collection
            row = (i // 4)
            column = (i % 4) + 1
            label.grid(row=row, column=column, padx=0, pady=0)
            self.image_labels.append(label)

        for i in range(self.lp.number_of_images):
            self.image_labels[i].bind("<Button-1>", eval(f'image_clicked_{i + 1}'))

        self.label_legend = tk.Label(self, text=f'{batch[1]}')
        self.label_legend.grid(row=0, column=1, sticky='NW')

        print('RAM memory % used:', psutil.virtual_memory()[2])
        print('RAM Used (GB):', psutil.virtual_memory()[3] / 1000000000)
        print('The CPU usage is: ', psutil.cpu_percent(4))
        time.sleep(self._time_to_sleep())
        self._clean_labels()


