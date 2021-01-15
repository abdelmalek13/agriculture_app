import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style

style.use("ggplot")
NORM_FONT = ("verdana", 10)

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.iconbitmap(default="E:\\codes\\asmaa ali\\project\\gui\\health.ico")
        self.wm_title("PROJECT")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (startPage, pageOne, pageTwo, graphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(startPage)

    def show_frame(self, cont):
        print(cont)
        frame = self.frames[cont]
        frame.tkraise()

class startPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.left_frame = tk.Frame(self,padx=10,pady=10,bd = 3, relief = 'groove')
        self.left_frame.pack(side=tk.LEFT, expand=True)

        self.right_frame = tk.Frame(self,padx=10,pady=10,bd = 3, relief = 'groove')
        self.right_frame.pack(side=tk.RIGHT, expand=True)

        self.top_left_frame = tk.Frame(self.left_frame,padx=2, pady=2)
        self.top_left_frame.pack()

        label = tk.Label(self.left_frame, text="Start Page")
        label.pack(pady=10, padx=10)


        button = ttk.Button(self.right_frame, text="Visit page 2",
                           command=lambda: controller.show_frame(pageTwo))
        button.pack(pady=10, padx=10)


        button2 = ttk.Button(self.left_frame, text="Visit Page 1",
                           command=lambda: controller.show_frame(pageOne))
        button2.pack(pady=10, padx=10)

        button3 = ttk.Button(self.left_frame, text="Visit Page Graph",
                           command=self.popupmsg)
        button3.pack(pady=10, padx=10)

    def qf(self, msg):
        print(msg)

    def popupmsg(self):
        popup = tk.Tk()
        def leavemini():
            self.controller.show_frame(graphPage)
            popup.destroy()
        popup.wm_title("Are you sure")
        label = ttk.Label(popup, text="Are you sure you want to open the graph page, it may take ages", font=NORM_FONT)
        label.pack(side="top", fill='x', pady=10)
        B1 = ttk.Button(popup, text = "Okay", command= leavemini)
        B1.pack()
        popup.mainloop()



class pageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="page One !!!")
        label.pack(padx=10, pady=10)

        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(pageTwo))
        button2.pack()




class pageTwo(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="page two!!!")
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(pageOne))
        button2.pack()



class graphPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(startPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi =100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6],[1,2,3,4,5,6])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)






if __name__ == "__main__":
    app = App()
    app.geometry("1200x720+0+0")
    app.mainloop()
