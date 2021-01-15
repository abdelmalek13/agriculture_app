import tkinter as tk
import tkinter.ttk as ttk
from water_analysis import waterAnalysis
import os
import uuid

LARGE_FONT = ("Verdana", 12)


class startPage(tk.Frame):
    def __init__(self, parent, controller, frames):
        super().__init__(parent)
        self.controller = controller
        self.frames = frames
        # print(self.frames)
        self.generate_session()
        main_frame = tk.Frame(self)
        main_frame.place(in_=self, anchor='c', relx=.5, rely=.5)

        left_frame = tk.LabelFrame(main_frame, bd=3, height=500, width=350,
                                   relief="groove",
                                   text="Water footprint analysis",
                                   font=LARGE_FONT)
        left_frame.pack(side=tk.LEFT, padx=10)
        left_frame.pack_propagate(False)
        right_frame = tk.LabelFrame(main_frame, bd=3,
                                    height=500, width=350, relief='groove',
                                    text="Virtual water trade analysis",
                                    font=LARGE_FONT)
        right_frame.pack(side=tk.LEFT, padx=10)
        right_frame.pack_propagate(False)

        top_left_frame = tk.Frame(left_frame, bd=2, relief="ridge")
        top_left_frame.pack(expand=True, fill="both")
        wfa_but = ttk.Button(top_left_frame, text="Water footprint analysis",
                             command=lambda:self.open_water_analysis(
                                self.wfa_v.get(),self.wfa_v2.get(),
                                self.wfa_v3.get()))
        wfa_but.pack(pady=10, padx=10, expand=True, fill="both")
        tl_bot_frame = tk.Frame(top_left_frame)
        tl_bot_frame.pack(expand=True, fill="both")
        tlbot_left_frame = tk.Frame(tl_bot_frame)
        tlbot_left_frame.pack(side=tk.LEFT, expand=True)

        tlbot_center_frame = tk.Frame(tl_bot_frame)
        tlbot_center_frame.pack(side=tk.LEFT, expand=True)
        tlbot_right_frame = tk.Frame(tl_bot_frame)
        tlbot_right_frame.pack(side=tk.LEFT, expand=True)

        center_left_frame = tk.Frame(left_frame, bd=2, relief="ridge")
        center_left_frame.pack(expand=True, fill="both")
        dwfa_but = ttk.Button(center_left_frame, text="""Distributing crops
according to
WF analysis""")
        dwfa_but.pack(pady=10, padx=10, side=tk.LEFT, expand=True, fill="both")
        cl_right_frame = tk.Frame(center_left_frame)
        cl_right_frame.pack(side=tk.LEFT, expand=True, fill="both")

        bottom_left_frame = tk.Frame(left_frame, bd=2, relief="ridge")
        bottom_left_frame.pack(expand=True, fill="both")
        pwfa_but = ttk.Button(bottom_left_frame, text="""Predicting the
distribution of crops
according to
WF analysis""")
        pwfa_but.pack(pady=10, padx=10, side=tk.LEFT, expand=True, fill="both")
        bl_right_frame = tk.Frame(bottom_left_frame)
        bl_right_frame.pack(side=tk.LEFT, expand=True, fill="both")

        top_right_frame = tk.Frame(right_frame, padx=10, pady=10, bd=2,
                                   relief="ridge")
        top_right_frame.pack(expand=True, fill="both")
        voc_but = ttk.Button(top_right_frame, text="""Virtual water trade
for one crop""")
        voc_but.pack(pady=10, padx=10, side=tk.LEFT, expand=True, fill="both")
        tr_right_frame = tk.Frame(top_right_frame)
        tr_right_frame.pack(side=tk.LEFT, expand=True, fill="both")

        bottom_right_frame = tk.Frame(right_frame, padx=10, pady=10, bd=2,
                                      relief="ridge")
        bottom_right_frame.pack(expand=True, fill="both")
        vmc_but = ttk.Button(bottom_right_frame, text="""Virtual water trade
for Multi crops""")
        vmc_but.pack(pady=10, padx=10, side=tk.LEFT, expand=True, fill="both")
        br_right_frame = tk.Frame(bottom_right_frame)
        br_right_frame.pack(side=tk.LEFT, expand=True, fill="both")

        self.set_radio_vars()

        for self.wfa_val, self.wfa_opt in enumerate(self.wfa_options):
            wfa_rad = ttk.Radiobutton(tlbot_left_frame,
                                      text=self.wfa_opt,
                                      variable=self.wfa_v,
                                      value=self.wfa_val)
            wfa_rad.pack(expand=True, fill="both")

        for self.wfa_val2, self.wfa_opt2 in enumerate(self.wfa_options2):
            wfa_rad2 = ttk.Radiobutton(tlbot_center_frame,
                                       text=self.wfa_opt2,
                                       variable=self.wfa_v2,
                                       value=self.wfa_val2)
            wfa_rad2.pack(expand=True, fill="both")

        for self.wfa_val3, self.wfa_opt3 in enumerate(self.wfa_options3):
            wfa_rad3 = ttk.Radiobutton(tlbot_right_frame,
                                       text=self.wfa_opt3,
                                       variable=self.wfa_v3,
                                       value=self.wfa_val3)
            wfa_rad3.pack(expand=True, fill="both")

        for self.dwfa_val, self.dwfa_opt in enumerate(self.dwfa_options):
            dwfa_rad = ttk.Radiobutton(cl_right_frame,
                                       text=self.dwfa_opt,
                                       variable=self.dwfa_v,
                                       value=self.dwfa_val)
            dwfa_rad.pack(expand=True, fill="both")

        for self.pwfa_val, self.pwfa_opt in enumerate(self.pwfa_options):
            pwfa_rad = ttk.Radiobutton(bl_right_frame,
                                       text=self.pwfa_opt,
                                       variable=self.pwfa_v,
                                       value=self.pwfa_val)
            pwfa_rad.pack(expand=True, fill="both")

        for self.voc_val, self.voc_opt in enumerate(self.voc_options):
            voc_rad = ttk.Radiobutton(tr_right_frame,
                                      text=self.voc_opt,
                                      variable=self.voc_v, value=self.voc_val)
            voc_rad.pack(expand=True, fill="both")

        for self.vmc_val, self.vmc_opt in enumerate(self.vmc_options):
            vmc_rad = ttk.Radiobutton(br_right_frame,
                                      text=self.vmc_opt,
                                      variable=self.vmc_v, value=self.vmc_val)
            vmc_rad.pack(expand=True, fill="both")

    def set_radio_vars(self):
        self.wfa_v = tk.IntVar()
        self.wfa_v2 = tk.IntVar()
        self.wfa_v3 = tk.IntVar()
        self.dwfa_v = tk.IntVar()
        self.pwfa_v = tk.IntVar()
        self.voc_v = tk.IntVar()
        self.vmc_v = tk.IntVar()
        self.wfa_v.set(0)
        self.wfa_v2.set(0)
        self.wfa_v3.set(0)
        self.dwfa_v.set(0)
        self.pwfa_v.set(0)
        self.voc_v.set(0)
        self.vmc_v.set(0)
        self.wfa_options = ["one crop", "Multi crops"]
        self.wfa_options2 = ["one year", "Multi years"]
        self.wfa_options3 = ["one region", "Multi regions"]
        self.dwfa_options = ["small scale", "large scale"]
        self.pwfa_options = ["small scale", "large scale"]
        self.voc_options = ["one country", "two countries", "three countries"]
        self.vmc_options = ["one country", "two countries"]

    def open_water_analysis(self,n_crops, n_years, n_regions):
        if not (n_regions or n_crops or n_years):
            self.controller.show_frame("waterAnalysis")

    def generate_session(self):
        path = os.path.join(os.getcwd(),"sessions")
        last_sessions = [int(x.split()[-1]) for x in os.listdir(path) if x]
        if last_sessions:
            session = "session " + str(max(last_sessions)+1)
            os.mkdir(os.path.join(path,session))
        else:
            session = "session " + str(1)
            os.mkdir(os.path.join(path,session))
