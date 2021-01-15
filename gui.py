import tkinter as tk
import tkinter.ttk as ttk

class createW(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.iconbitmap("gray25")

        self.win = ttk.Frame(self.master)
        self.win.pack()

class startPage(createW):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.setVars()
        self.setChoices()

        self.main_frame = tk.Frame(self.master, height = 500, width = 1000)
        self.main_frame.pack()

        self.left_frame = tk.Frame(self.main_frame,padx=10,pady=10,bg="blue",bd = 3, relief = 'groove', height = 500, width = 800)
        self.left_frame.pack(side=tk.LEFT)
        ##
        self.top_left_frame = tk.Frame(self.left_frame,padx=2, pady=2)
        self.top_left_frame.pack()
        #
        self.top_left_button = tk.Button(self.top_left_frame,
                                         text="Water footprint analysis",
                                         command=self.top_left_button_func)
        self.top_left_button.grid(column=0, row=0, sticky="nsew")

        self.top_left_radio = tk.Radiobutton(self.top_left_frame,
                                             text=self.top_left_choices,
                                             padx=20, var=self.top_left_var)
        self.top_left_radio.grid(row=1,column=0, sticky="nsew")

        self.top_left_radio2 = tk.Radiobutton(self.top_left_frame,
                                             text=self.top_left_choices2,
                                             padx=20, var=self.top_left_var2)
        self.top_left_radio2.grid(row=1,column=1, sticky="nsew")

        self.top_left_radio3 = tk.Radiobutton(self.top_left_frame,
                                             text=self.top_left_choices3,
                                             padx=20, var=self.top_left_var3)
        self.top_left_radio.grid(row=1,column=2, sticky="nsew")


        self.mid_left_frame = tk.Frame(self.left_frame,padx=2, pady=2)
        self.mid_left_frame.pack()
        #
        self.mid_left_button = tk.Button(self.mid_left_frame,
                                        text="Distributing crops according to analysis", command=self.mid_left_button_func)
        self.mid_left_button.grid(column=0,row=0)


        self.mid_left_radio = tk.Radiobutton(self.mid_left_frame,
                                             text=self.mid_left_choices,
                                             padx=20, var=self.mid_left_var)
        self.mid_left_radio.grid(row=0,column=1)


        self.bottom_left_frame = tk.Frame(self.left_frame, padx=2, pady=2)
        self.bottom_left_frame.pack()
        #
        self.bottom_left_button = tk.Button(self.bottom_left_frame,
                                           text="Predicting distribution of crops according to WF analysis",
                                        command=self.bottom_left_button_func)
        self.bottom_left_button.grid(column=0,row=0)


        self.bottom_left_radio = tk.Radiobutton(self.bottom_left_frame,
                                             text=self.bottom_left_choices,
                                             padx=20, var=self.bottom_left_var)
        self.bottom_left_radio.grid(row=0,column=1)


        self.right_frame = tk.Frame(self.main_frame,padx=10,pady=10, bg="green")
        self.right_frame.pack(side=tk.RIGHT, anchor=tk.E)
        ##
        self.top_right_frame = tk.Frame(self.right_frame,padx=2, pady=5)
        self.top_right_frame.pack()
        #
        self.top_right_button = tk.Button(self.top_right_frame,
                                        text="Virtual water trade for one crop", command=self.top_right_button_func)
        self.top_right_button.grid(column=0,row=0)

        self.top_right_radio = tk.Radiobutton(self.top_right_frame,
                                             text=self.top_right_choices,
                                             padx=20, var=self.top_right_var)
        self.top_right_radio.grid(row=0,column=1)

        self.bottom_right_frame = tk.Frame(self.right_frame,padx=2, pady=5)
        self.bottom_right_frame.pack()
        #
        self.bottom_right_button = tk.Button(self.bottom_right_frame,
                                        text="Virtual water trades for multi crops", command=self.bottom_right_button_func)
        self.bottom_right_button.grid(column=0,row=0)


        self.bottom_right_radio = tk.Radiobutton(self.bottom_right_frame,
                                             text=self.bottom_right_choices,
                                             padx=20, var=self.bottom_right_var)
        self.bottom_right_radio.grid(row=0,column=1)

    def top_left_button_func(self):
        pass

    def mid_left_button_func(self):
        pass

    def bottom_left_button_func(self):
        pass

    def top_right_button_func(self):
        pass

    def bottom_right_button_func(self):
        pass

    def setVars(self):
        self.top_left_var = tk.IntVar()
        self.top_left_var2 = tk.IntVar()
        self.top_left_var3 = tk.IntVar()
        self.mid_left_var = tk.IntVar()
        self.bottom_left_var = tk.IntVar()
        self.top_right_var = tk.IntVar()
        self.bottom_right_var = tk.IntVar()

    def setChoices(self):
        self.top_left_choices = {
            "one crop":0,
            "Multi crops":1
            }
        self.top_left_choices2 = {
            "one year":0,
            "Multi years":1
        }
        self.top_left_choices3 = {
            "One region":0,
            "Multi region":1
        }
        self.mid_left_choices = {
            "Small Scale":0,
            "Large Scale":1
        }
        self.bottom_left_choices = {
            "Small Scale":0,
            "Large Scale":1
        }
        self.top_right_choices = {
            "one country":0,
            "Two countries":1,
            "Multi countries":2
        }
        self.bottom_right_choices = {
            "one country":0,
            "Two countries":1
        }



root = tk.Tk()
root.geometry("1200x720+0+0")
app = startPage(master=root)
app.mainloop()
