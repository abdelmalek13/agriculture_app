import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from blue_et import blueEt
from grey_water import greyWater

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)


class waterAnalysis(tk.Frame):
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

        top_frame = tk.LabelFrame(main_frame, bd=3, height=150, width=750,
                                   relief="groove",
                                   text="General",
                                   font=LARGE_FONT)
        top_frame.pack(padx=2)
        top_frame.pack_propagate(False)
        top_frame.grid_propagate(False)

        country_lbl = tk.Label(top_frame, text="country name")
        country_lbl.grid(row=0, column=0, padx=2, pady=10)

        crop_lbl = tk.Label(top_frame, text="crop name")
        crop_lbl.grid(row=1, column=0, padx=2, pady=10)

        self.country_ent = tk.Entry(top_frame)
        self.country_ent.grid(row=0, column=1, padx=2, pady=10)

        self.crop_v = tk.StringVar()
        self.crop_options = self.get_crop_names()
        self.crop_v.set(self.crop_options[0])

        self.crop_ent = tk.OptionMenu(top_frame, self.crop_v,
                                       *self.crop_options)
        self.crop_ent.grid(row=1, column=1, padx=2, pady=10)
        self.crop_ent.config(width=15)

        reg_gov_lbl = tk.Label(top_frame, text="region/governorate")
        reg_gov_lbl.grid(row=0, column=2, padx=2, pady=10)

        yield_lbl = tk.Label(top_frame, text="crop yield")
        yield_lbl.grid(row=1, column=2, padx=2, pady=10)

        self.reg_gov_ent = tk.Entry(top_frame)
        self.reg_gov_ent.grid(row=0, column=3, padx=2, pady=10)

        self.yield_ent = tk.Entry(top_frame)
        self.yield_ent.grid(row=1, column=3, padx=2, pady=10)

        year_lbl = tk.Label(top_frame, text="Year")
        year_lbl.grid(row=0, column=4, padx=2, pady=10)

        date_lbl = tk.Label(top_frame, text="Plant date")
        date_lbl.grid(row=1, column=4, padx=2, pady=10)

        self.year_ent = tk.Entry(top_frame)
        self.year_ent.insert(0, "YYYY")
        self.year_ent.config(fg="grey")
        self.year_ent.bind("<FocusIn>", self.on_entry_click_year)
        self.year_ent.bind("<FocusOut>", self.on_focus_out_year)
        self.year_ent.grid(row=0, column=5, padx=2, pady=10)

        self.date_ent = tk.Entry(top_frame)
        self.date_ent.insert(0, "dd/mm")
        self.date_ent.config(fg="grey")
        self.date_ent.bind("<FocusIn>", self.on_entry_click_date)
        self.date_ent.bind("<FocusOut>", self.on_focus_out_date)
        self.date_ent.grid(row=1, column=5, padx=2, pady=10)

        center_frame = tk.LabelFrame(main_frame, bd=3, height=150, width=750,
                                       relief="groove",
                                       text="Water footprint analysis",
                                       font=LARGE_FONT)
        center_frame.pack(padx=2)
        center_frame.pack_propagate(False)
        center_frame.grid_propagate(False)

        blue_et_but = ttk.Button(center_frame, text="Blue ET",
                                 command=lambda:self.controller.show_frame(blueEt))
        blue_et_but.grid(padx=2, pady=5, row=0, column=0)

        green_et_lbl = tk.Label(center_frame, text="Green ET")
        green_et_lbl.grid(padx=2, pady=5, row=1, column=0)

        grey_wf_but = ttk.Button(center_frame, text="Grey ET",
                                 command=lambda:self.controller.show_frame(greyWater))
        grey_wf_but.grid(padx=2, pady=5, row=2, column=0)

        blue_et_frame = tk.Frame(center_frame)
        blue_et_frame.grid(padx=2, pady=5, row=0, column=1)
        self.blue_et_ent = tk.Entry(blue_et_frame)
        self.blue_et_ent.grid(row=0, column=0)
        blue_et_metrics_lbl = tk.Label(blue_et_frame, text="mm/day")
        blue_et_metrics_lbl.grid(row=0, column=1)

        green_et_frame = tk.Frame(center_frame)
        green_et_frame.grid(padx=2, pady=5, row=1, column=1)
        self.green_et_ent = tk.Entry(green_et_frame)
        self.green_et_ent.grid(row=0, column=0)
        green_et_metrics_lbl = tk.Label(green_et_frame, text="mm/day")
        green_et_metrics_lbl.grid(row=0, column=1)

        grey_wf_frame = tk.Frame(center_frame)
        grey_wf_frame.grid(padx=2, pady=5, row=2, column=1)
        self.grey_wf_ent = tk.Entry(grey_wf_frame)
        self.grey_wf_ent.grid(row=0, column=0)
        grey_wf_metrics_lbl = tk.Label(grey_wf_frame, text="m3/ton")
        grey_wf_metrics_lbl.grid(row=0, column=1)

        blue_cwr_lbl = tk.Label(center_frame, text="Blue CWR")
        blue_cwr_lbl.grid(padx=2, pady=5, row=0, column=2)

        green_cwr_lbl = tk.Label(center_frame, text="Green CWR")
        green_cwr_lbl.grid(padx=2, pady=5, row=1, column=2)

        total_wf_lbl = tk.Label(center_frame, text="Total WF")
        total_wf_lbl.grid(padx=2, pady=5, row=2, column=2)

        blue_cwr_frame = tk.Frame(center_frame)
        blue_cwr_frame.grid(padx=2, pady=5, row=0, column=3)
        self.blue_cwr_outlbl = tk.Entry(blue_cwr_frame, background="grey")
        self.blue_cwr_outlbl.grid(row=0, column=0)
        self.blue_cwr_outlbl.config(state="readonly")
        blue_cwr_metrics_lbl = tk.Label(blue_cwr_frame, text="m3/Fed")
        blue_cwr_metrics_lbl.grid(row=0, column=1)

        green_cwr_frame = tk.Frame(center_frame)
        green_cwr_frame.grid(padx=2, pady=5, row=1, column=3)
        self.green_cwr_outlbl = tk.Entry(green_cwr_frame, background="grey")
        self.green_cwr_outlbl.grid(row=0, column=0)
        self.green_cwr_outlbl.config(state="readonly")
        green_cwr_metrics_lbl = tk.Label(green_cwr_frame, text="m3/Fed")
        green_cwr_metrics_lbl.grid(row=0, column=1)

        total_wf_frame = tk.Frame(center_frame)
        total_wf_frame.grid(padx=2, pady=5, row=2, column=3)
        self.total_wf_outlbl = tk.Entry(total_wf_frame, background="grey")
        self.total_wf_outlbl.grid(row=0, column=0)
        self.total_wf_outlbl.config(state="readonly")
        total_wf_metrics_lbl = tk.Label(total_wf_frame, text="m3/ton")
        total_wf_metrics_lbl.grid(row=0, column=1)

        blue_wf_lbl = tk.Label(center_frame, text="Blue WF")
        blue_wf_lbl.grid(padx=2, pady=5, row=0, column=4)

        green_wf_lbl = tk.Label(center_frame, text="Green WF")
        green_wf_lbl.grid(padx=2, pady=5, row=1, column=4)

        blue_wf_frame = tk.Frame(center_frame)
        blue_wf_frame.grid(padx=2, pady=5, row=0, column=5)
        self.blue_wf_outlbl = tk.Entry(blue_wf_frame, background="grey")
        self.blue_wf_outlbl.grid(row=0, column=0)
        self.blue_wf_outlbl.config(state="readonly")
        blue_wf_metrics_lbl = tk.Label(blue_wf_frame, text="m3/ton")
        blue_wf_metrics_lbl.grid(row=0, column=1)

        green_wf_frame = tk.Frame(center_frame)
        green_wf_frame.grid(padx=2, pady=5, row=1, column=5)
        self.green_wf_outlbl = tk.Entry(green_wf_frame, background="grey")
        self.green_wf_outlbl.grid(row=0, column=0)
        self.green_wf_outlbl.config(state="readonly")
        green_wf_metrics_lbl = tk.Label(green_wf_frame, text="m3/ton")
        green_wf_metrics_lbl.grid(row=0, column=1)

        water_calc_but = ttk.Button(center_frame, text="Calculate",
                                    command=self.calculate)
        water_calc_but.grid(padx=5, pady=5, row=2, column=5, sticky=tk.W)

        self.status_v = tk.StringVar()
        self.status_v.set("Welcome...")
        self.status_bar = tk.Label(main_frame, relief="groove", anchor=tk.W,
                                    textvariable=self.status_v, font=NORM_FONT)
        self.status_bar.pack(side=tk.BOTTOM, fill='x', anchor='s')
        self.status_bar.config(fg="black")

        lower_left_frame = tk.Frame(main_frame, height=150, width=400,
                                    relief="groove", bd=3)
        lower_left_frame.pack(side=tk.LEFT, padx=2, pady=5)

        prod_frac_lbl = tk.Label(lower_left_frame, text="Product fraction")
        prod_frac_lbl.grid(padx=2, pady=5, row=0, column=0)

        energy_out_lbl = tk.Label(lower_left_frame, text="Energy output")
        energy_out_lbl.grid(padx=2, pady=5, row=1, column=0)

        energy_p_lbl = tk.Label(lower_left_frame, text="Energy price")
        energy_p_lbl.grid(padx=2, pady=5, row=2, column=0)

        self.prod_frac_ent = tk.Entry(lower_left_frame)
        self.prod_frac_ent.grid(row=0, column=1, padx=2, pady=5, sticky="w")

        energy_out_frame = tk.Frame(lower_left_frame)
        energy_out_frame.grid(padx=2, pady=5, row=1, column=1)
        self.energy_out_ent = tk.Entry(energy_out_frame)
        self.energy_out_ent.grid(row=0, column=0, sticky="w")
        energy_out_lbl = tk.Label(energy_out_frame, text="Kcal/ton")
        energy_out_lbl.grid(row=0, column=1)

        energy_p_frame = tk.Frame(lower_left_frame)
        energy_p_frame.grid(padx=2, pady=5, row=2, column=1)
        self.energy_p_ent = tk.Entry(energy_p_frame)
        self.energy_p_ent.grid(row=0, column=0, sticky="w")
        energy_p_lbl = tk.Label(energy_p_frame, text=" $/Kcal")
        energy_p_lbl.grid(row=0, column=1)

        prod_wf_lbl = tk.Label(lower_left_frame, text="Product WF")
        prod_wf_lbl.grid(padx=2, pady=5, row=0, column=2)

        energy_wp_lbl = tk.Label(lower_left_frame, text="Energetic WP")
        energy_wp_lbl.grid(padx=2, pady=5, row=1, column=2)

        economy_wp_lbl = tk.Label(lower_left_frame, text="Economic WP")
        economy_wp_lbl.grid(padx=2, pady=5, row=2, column=2)

        prod_wf_frame = tk.Frame(lower_left_frame)
        prod_wf_frame.grid(padx=2, pady=5, row=0, column=3)
        self.prod_wf_outlbl = tk.Entry(prod_wf_frame, background="grey")
        self.prod_wf_outlbl.config(state="readonly")
        self.prod_wf_outlbl.grid(row=0, column=0, sticky="w")
        prdo_wf_lbl = tk.Label(prod_wf_frame, text="m3/ton")
        prdo_wf_lbl.grid(row=0, column=1)

        energy_wp_frame = tk.Frame(lower_left_frame)
        energy_wp_frame.grid(padx=2, pady=5, row=1, column=3)
        self.energy_wp_outlbl = tk.Entry(energy_wp_frame, background="grey")
        self.energy_wp_outlbl.config(state="readonly")
        self.energy_wp_outlbl.grid(row=0, column=0, sticky="w")
        energy_wp_lbl = tk.Label(energy_wp_frame, text="Kcal/m3")
        energy_wp_lbl.grid(row=0, column=1)

        economy_wp_frame = tk.Frame(lower_left_frame)
        economy_wp_frame.grid(padx=2, pady=5, row=2, column=3)
        self.economy_wp_outlbl = tk.Entry(economy_wp_frame, background="grey")
        self.economy_wp_outlbl.config(state="readonly")
        self.economy_wp_outlbl.grid(row=0, column=0, sticky="w")
        economy_wf_lbl = tk.Label(economy_wp_frame, text=" $/m3")
        economy_wf_lbl.grid(row=0, column=1)

        ext_calc_but = ttk.Button(lower_left_frame, text="Calculate",
                                  command=self.calculate)
        ext_calc_but.grid(padx=5, pady=5, row=3, column=1)

        lower_right_frame = tk.Frame(main_frame, borderwidth=3, height=150,
                                      width=100)
        lower_right_frame.pack(side=tk.LEFT, padx=15, pady=10)
        lower_right_frame.pack_propagate(False)
        self.new_but = ttk.Button(lower_right_frame, text="New",
                                  style="Forbid.TButton",
                                  command=lambda: self.checkSaveLock(False))
        self.new_but.pack(pady=5, fill="x", anchor="e", expand=True)

        save_but = ttk.Button(lower_right_frame, text="Save",
                              command=self.saveMsg, style="Save.TButton")
        save_but.pack(pady=5, fill='x', anchor="e", expand=True)

        self.next_but = ttk.Button(lower_right_frame, text="Next",
                                   style="Forbid.TButton",
                                   command=lambda: self.checkSaveLock(True))
        self.next_but.pack(pady=5, fill='x', anchor="e", expand=True)

    def on_entry_click_year(self, event):
        if self.year_ent.get() == "YYYY":
            self.year_ent.delete(0, 'end')
            self.year_ent.insert(0, '')
            self.year_ent.config(fg="black")
            self.status_v.set("Please, Be sure to write the year in this format YYYY, like '2012'")
            self.status_bar.config(fg="black")

    def on_focus_out_year(self, event):
        if self.year_ent.get() == '':
            self.year_ent.insert(0, "YYYY")
            self.year_ent.config(fg="grey")


    def on_entry_click_date(self, event):
        if self.date_ent.get() == "dd/mm":
            self.date_ent.delete(0, 'end')
            self.date_ent.insert(0, '')
            self.date_ent.config(fg="black")
            self.status_v.set("Please, Be sure to write the year in this format dd/mm, like '24/12'")
            self.status_bar.config(fg="black")

    def on_focus_out_date(self, event):
        if not self.date_ent.get():
            self.date_ent.insert(0, "dd/mm")
            self.date_ent.config(fg="grey")

    def calculate(self):
        try:
            datetime.strptime(self.year_ent.get(), "%Y")
        except ValueError:
            self.status_v.set("ERROR, The Year isn't in the correct format!!")
            self.status_bar.config(fg="red")
            return None
        try:
            datetime.strptime(self.date_ent.get(), "%d/%m")
        except ValueError:
            self.status_v.set("ERROR, The Date isn't in the correct format!!")
            self.status_bar.config(fg="red")
            return None
        if not (self.blue_et_ent.get() and self.green_et_ent.get()):
            self.status_v.set("ERROR, calculate both Blue ET and Green ET, or enter them manually")
            self.status_bar.config(fg="red")
            return None
        try:
            blue = float(self.blue_et_ent.get())
            green = float(self.green_et_ent.get())
            grey = float()
        except:
            self.status_v.set("ERROR, Blue ET, Green ET and Grey WF should be decimal numbers")
            self.status_bar.config(fg="red")

        self.status_v.set("DONE")
        self.status_bar.config(fg="black")

    def get_crop_names(self):
        df = pd.read_excel("crop_names.xlsx", sheet_name="Sheet1")
        return [x for x in df['Crop1'] if x[1] != '.']

    def popupWarning(self, next_flag):
        msg = """Are you sure you want to
clear the data without saving!!"""
        msgbox = messagebox.askokcancel("Warning!!", msg, icon="warning")
        return msgbox

    def checkSaveLock(self, next_flag):
        if not self.saved_flag:
            res = self.popupWarning(next_flag)
        if self.saved_flag or res:
            self.clear()
            if next_flag:
                pass

    def safeClear(self):
        self.new_but['style'] = "Save.TButton"
        self.next_but['style'] = "Save.TButton"

    def clear(self):
        all_ents = (self.country_ent, self.reg_gov_ent, self.yield_ent,
                    self.blue_et_ent, self.green_et_ent, self.grey_wf_ent,
                    self.energy_out_ent, self.energy_p_ent, self.prod_frac_ent)

        for ent in all_ents:
            ent.delete(0, 'end')

        all_outlbls = (self.blue_cwr_outlbl, self.green_cwr_outlbl,
                       self.total_wf_outlbl, self.blue_wf_outlbl,
                       self.green_wf_outlbl, self.prod_wf_outlbl,
                       self.energy_wp_outlbl, self.economy_wp_outlbl)
        for ent in all_outlbls:
            ent.config(state="normal")
            ent.insert(0, "1331")
            ent.delete(0, 'end')
            ent.config(state="readonly")

        self.year_ent.delete(0, 'end')
        self.year_ent.insert(0, "YYYY")
        self.year_ent.config(fg="grey")
        self.year_ent.bind("<FocusIn>", self.on_entry_click_year)
        self.year_ent.bind("<FocusOut>", self.on_focus_out_year)

        self.date_ent.delete(0, 'end')
        self.date_ent.insert(0, "dd/mm")
        self.date_ent.config(fg="grey")
        self.date_ent.bind("<FocusIn>", self.on_entry_click_date)
        self.date_ent.bind("<FocusOut>", self.on_focus_out_date)

        self.crop_v.set(self.crop_options[0])

    def saveMsg(self):
        path = os.getcwd()
        savebox = filedialog.asksaveasfile(mode='w', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")
        if savebox:
            self.safeClear()
            text_data = str('HEEEEEEYYYYY')
            savebox.write(text_data)
            savebox.close()
            self.saved_flag = True
            self.clear()
