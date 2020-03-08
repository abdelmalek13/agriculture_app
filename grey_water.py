import tkinter as tk
import tkinter.ttk as ttk
import water_analysis

NORM_FONT = ("Verdana", 10)


class greyWater(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.saved_flag = False
        self.style = ttk.Style()
        self.style.configure("Forbid.TButton", fg="red",
                             background="red")
        self.style.configure("Save.TButton", fg="green",
                             background="green")
        # self.style.configure("TLabelframe", relief="groove", borderwidth=3)
        # self.style.configure("TLabelframe.Label", font=LARGE_FONT)
        self.start_user_UI()

    def start_user_UI(self):
        main_frame = tk.Frame(self)
        main_frame.place(in_=self, anchor='c', relx=.5, rely=.5)

        top_frame = tk.Frame(main_frame, bd=3, height=250, width=750,
                                   relief="groove")
        top_frame.pack(padx=10, pady=10, ipadx=5, ipady=5)
        # top_frame.grid_propagate(False)
        top_frame.grid_columnconfigure(2)
        top_frame.grid_rowconfigure(2)

        napp_frame = tk.Frame(top_frame)
        napp_frame.grid(row=0, column=0, padx=5, pady=5)
        napp_lbl = tk.Label(napp_frame, text="Nitrogen application",
                            font=NORM_FONT)
        napp_lbl.grid(row=0, columnspan=2, sticky='w')
        napp_lbl = tk.Label(napp_frame, text="rate(kg/na)", font=NORM_FONT)
        napp_lbl.grid(row=1, column=0)
        self.napp_ent = tk.Entry(napp_frame)
        self.napp_ent.grid(row=1, column=1)

        maxconc_frame = tk.Frame(top_frame)
        maxconc_frame.grid(row=0, column=1, padx=5, pady=5)
        maxconc_lbl = tk.Label(maxconc_frame, text="Maximum concentration",
                               font=NORM_FONT)
        maxconc_lbl.grid(row=0, columnspan=2, sticky='w')
        maxconc_lbl = tk.Label(maxconc_frame, text="for Nitrogen (kg/m3)",
                               font=NORM_FONT)
        maxconc_lbl.grid(row=1, column=0)
        self.maxconc_ent = tk.Entry(maxconc_frame)
        self.maxconc_ent.grid(row=1, column=1)

        lrunoff_frame = tk.Frame(top_frame)
        lrunoff_frame.grid(row=1, column=0, padx=5, pady=5)
        lrunoff_lbl = tk.Label(lrunoff_frame, text="Leaching runoff",
                               font=NORM_FONT)
        lrunoff_lbl.grid(row=0, columnspan=2, sticky='w')
        lrunoff_lbl = tk.Label(lrunoff_frame, text="fraction", font=NORM_FONT)
        lrunoff_lbl.grid(row=1, column=0)
        self.lrunoff_ent = tk.Entry(lrunoff_frame)
        self.lrunoff_ent.grid(row=1, column=1)

        nconc_frame = tk.Frame(top_frame)
        nconc_frame.grid(row=1, column=1, padx=5, pady=5)
        nconc_lbl = tk.Label(nconc_frame, text="Natural concentration",
                             font=NORM_FONT)
        nconc_lbl.grid(row=0, columnspan=2, sticky='w')
        nconc_lbl = tk.Label(nconc_frame, text="for Nitrogen (kg/m3)",
                             font=NORM_FONT)
        nconc_lbl.grid(row=1, column=0)
        self.nconc_ent = tk.Entry(nconc_frame)
        self.nconc_ent.grid(row=1, column=1)

        lower_frame = tk.Frame(main_frame, bd=3, relief="groove")
        lower_frame.pack(padx=20, pady=10)

        # cropy_frame = tk.Frame(lower_frame)
        # cropy_frame.grid(padx=2, pady=5, row=0, column=3)
        cropy_lbl = tk.Label(lower_frame, text="Crop yield\n(ton)",
                             font=NORM_FONT)
        cropy_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.cropy_ent = tk.Entry(lower_frame, background="grey")
        self.cropy_ent.config("readonly")
        self.cropy_ent.grid(row=0, column=1, padx=5, pady=5)

        gwf_lbl = tk.Label(lower_frame, text="Grey WF\n(m3/ton)",
                           font=NORM_FONT)
        gwf_lbl.grid(row=0, column=2, padx=5, pady=5)
        self.gwf_ent = tk.Entry(lower_frame, background="grey")
        self.gwf_ent.config("readonly")
        self.gwf_ent.grid(row=0, column=3, padx=5, pady=5)

        but_frame = tk.Frame(main_frame)
        but_frame.pack(side=tk.RIGHT)
        save_but = ttk.Button(but_frame, text="Save")
        save_but.pack(anchor='s')
        next_but = ttk.Button(but_frame, text="Next", command=self.nextPage)
        next_but.pack(anchor='s')

    def nextPage(self):
        self.controller.show_frame(water_analysis.waterAnalysis)
