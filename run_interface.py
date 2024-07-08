import tkinter as tk

from interface import MainFrame


def main():
    app = tk.Tk()
    width = app.winfo_screenwidth()
    height = app.winfo_screenheight()
    app.geometry("%dx%d" % (width, height))
    app.title('Interface 2024')
    mainframe = MainFrame(app)
    mainframe.grid()
    app.mainloop()


if __name__ == "__main__":
    main()