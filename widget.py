import tkinter as tk
from start_page import startPage
from water_analysis import waterAnalysis
from blue_et import blueEt
from grey_water import greyWater



class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.iconbitmap(
            default="E:\\codes\\asmaa ali\\project\\gui\\health.ico")
        self.wm_title("PROJECT")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.generate_frames()

    def generate_frames(self):
        self.frames = {}
        for F in (startPage, waterAnalysis, blueEt, greyWater):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.pack_propagate(False)

        self.show_frame(startPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.geometry("800x600+0+0")
    app.resizable(False, False)
    app.mainloop()
