import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta, date
import pandas as pd
import os
from tkinter import filedialog
import water_analysis

NORM_FONT = ("Verdana", 10)
LARGE_FONT = ("Verdana", 12)


def calculateDays(start_date, end_date):
    sdate = date(*cleanDate(start_date))
    edate = date(*cleanDate(end_date))
    delta = edate - sdate
    days_list = []
    for i in range(delta.days+1):
        days_list.append(sdate + timedelta(days=i))
    return days_list


def cleanDate(date):
    date = date.split('/')
    if len(date) < 3:
        date.append(str(datetime.now()).split('-')[0])
    return map(int, date[::-1])


class blueEt(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        s = ttk.Style()
        s.configure("TNotebook.Tab", font=NORM_FONT)
        tab_parent = ttk.Notebook(self)

        tab1 = tabOne(tab_parent, self)
        tab2 = tabTwo(tab_parent, self)
        tab3 = tabThree(tab_parent, self)
        tab4 = tabFour(tab_parent, self)
        tab5 = tabFive(tab_parent, self.controller)
        #
        tab_parent.add(tab1, text="ETo")
        tab_parent.add(tab2, text="ETc")
        tab_parent.add(tab3, text="Rainfall")
        tab_parent.add(tab4, text="Soil data")
        tab_parent.add(tab5, text="Blue ET")

        tab_parent.grid_propagate(False)
        tab_parent.pack(expand=True, fill='both')
        # tab_parent.grid(col=True, fill="both")

LARGE_FONT = ("Verdana", 12)


class tabOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        top_frame = tk.LabelFrame(self, bd=3, height=75, width=750,
                                  text="Location Data", relief="groove",
                                  font=LARGE_FONT)
        top_frame.pack(padx=2, pady=5)
        top_frame.pack_propagate(False)
        top_frame.grid_propagate(False)

        lower_frame = tk.LabelFrame(self, bd=3, height=400, width=750,
                                    text="Climate data", relief="groove",
                                    font=LARGE_FONT)
        lower_frame.pack(padx=2, pady=5)
        lower_frame.pack_propagate(False)

        top_layer = tk.Frame(top_frame)
        top_layer.pack(anchor="c", pady=10)

        alt_frame = tk.Frame(top_layer)
        alt_frame.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        alt_lbl = ttk.Label(alt_frame, text="Altitude")
        alt_lbl.grid(row=0, column=0, sticky="w")
        alt_ent = ttk.Entry(alt_frame)
        alt_ent.grid(row=0, column=1, sticky='nsew')
        alt_metric_lbl = ttk.Label(alt_frame, text="m")
        alt_metric_lbl.grid(row=0, column=2, sticky="e")

        lat_frame = tk.Frame(top_layer)
        lat_frame.grid(row=0, column=1, padx=5, pady=5)
        lat_lbl = ttk.Label(lat_frame, text="Latitude")
        lat_lbl.grid(row=0, column=0, sticky="w")
        lat_ent = ttk.Entry(lat_frame)
        lat_ent.grid(row=0, column=1, sticky='nsew')
        self.lat_metric_v = tk.StringVar()
        self.lat_metric_options = ["N", "S"]
        self.lat_metric_v.set(self.lat_metric_options[0])
        self.lat_metric_menu = ttk.OptionMenu(lat_frame, self.lat_metric_v,
                                              self.lat_metric_options[0],
                                              *self.lat_metric_options)
        self.lat_metric_menu.grid(row=0, column=2, sticky="e")

        long_frame = tk.Frame(top_layer)
        long_frame.grid(row=0, column=2, padx=5, pady=5)
        long_lbl = ttk.Label(long_frame, text="Longitude")
        long_lbl.grid(row=0, column=0, sticky="w")
        long_ent = ttk.Entry(long_frame)
        long_ent.grid(row=0, column=1, sticky='nsew')
        self.long_metric_v = tk.StringVar()
        self.long_metric_options = ["W", "E"]
        self.lat_metric_v.set(self.lat_metric_options[0])
        self.long_metric_menu = ttk.OptionMenu(long_frame, self.long_metric_v,
                                               self.long_metric_options[0],
                                               *self.long_metric_options)
        self.long_metric_menu.grid(row=0, column=2, sticky="e")

        lower_layer = tk.Frame(lower_frame)
        lower_layer.pack(anchor="c", pady=10)

        crop_lbl = ttk.Label(lower_layer, text="Crop name")
        crop_lbl.grid(row=0, column=0, padx=5)
        self.crop_outlbl = ttk.Entry(lower_layer, background="grey")
        self.crop_outlbl.grid(row=0, column=1, padx=5)
        self.crop_outlbl.config(state="readonly")

        plant_lbl = ttk.Label(lower_layer, text="Plant date")
        plant_lbl.grid(row=0, column=2, padx=5)
        self.plant_outlbl = ttk.Entry(lower_layer, background="grey")
        self.plant_outlbl.grid(row=0, column=3, padx=5)
        self.plant_outlbl.config(state="readonly")

        harvest_lbl = ttk.Label(lower_layer, text="Harvesting date")
        harvest_lbl.grid(row=0, column=4, padx=5)
        self.harvest_outlbl = tk.Entry(lower_layer, background="grey")
        self.harvest_outlbl.grid(row=0, column=5, padx=5)

        table_frame = tk.Frame(lower_frame, height=300, width=500, bg="grey",
                               bd=3)
        table_frame.pack(side=tk.LEFT, pady=10)
        scrl_table_frame = ScrollableFrame(table_frame, height=300, width=500,
                                           borderwidth=3, add_x=True)
        scrl_table_frame.pack(fill='both')
        scrl_table_frame.grid_propagate(False)
        scrl_table_frame.pack_propagate(False)
        start_date = "20/02"
        end_date = "15/03"
        days_list = calculateDays(start_date, end_date)
        headers, df = self.format_table(days_list)
        header_units = ["", u'\N{DEGREE SIGN}C', u'\N{DEGREE SIGN}C', "%",
                        "km/day", "hours", "mm/day"]
        self.table_obj = tableWidget(scrl_table_frame.scrollable_frame, df=df,
                                     headers=headers,
                                     header_units=header_units,
                                     rows=len(days_list)+1,
                                     columns=len(headers),
                                     font=False)
        self.table_obj.pack(fill='both', expand=True)

        but_frame = tk.Frame(lower_frame, height=300, width=100)
        but_frame.pack(padx=20)
        but_frame.grid_propagate(False)
        but_frame.pack_propagate(False)

        save_but = ttk.Button(but_frame, text="Save", command=self.saveFile)
        save_but.pack(pady=5, fill="x", side=tk.BOTTOM)

        import_but = ttk.Button(but_frame, text="Import",
                                command=self.importFile)
        import_but.pack(pady=5, fill="x", side=tk.BOTTOM)

        calc_but = ttk.Button(but_frame, text="Calculate",
                              command=self.calculate)
        calc_but.pack(pady=5, fill="x", side=tk.BOTTOM)

        self.status_bar = tk.Label(self, relief="groove",
                                   text="Any missing fields will be asssumed"+\
                                   " equal to zero")
        self.status_bar.pack(side=tk.BOTTOM, fill='x')

    def calculate(self):
        pass

    def importFile(self):
        path = os.getcwd()
        importbox = filedialog.askopenfile(mode='r', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")

        # headers= ["Min\nTemp", "Max\nTemp", "Humidity", "Wind", 'Sun\nhours']
        data = pd.read_csv(importbox, index_col=None, usecols=["Min\nTemp",
                                                               "Max\nTemp",
                                                               "Humidity",
                                                               "Wind",
                                                               'Sun\nhours']
                           ).fillna("0")
        r, c = data.shape
        for row in range(r):
            for col in range(c):
                self.table_obj.insert_text(row=row+1, column=col+1,
                                           value=data.iloc[row, col])
        importbox.close()

    def format_table(self, days_list):
        headers = ["Day", "Min\nTemp", "Max\nTemp", "Humidity", "Wind",
                   'Sun\nhours', "Eto"]
        df = pd.DataFrame({"Day": days_list, "Min\nTemp": ['']*len(days_list),
                           "Max\nTemp": ['']*len(days_list),
                           "Humidity": ['']*len(days_list),
                           "Wind": ['']*len(days_list),
                           'Sun\nhours': ['']*len(days_list),
                           "Eto": ["0"]*len(days_list)}, columns=headers)
        return headers, df

    def saveFile(self):
        path = os.getcwd()
        savebox = filedialog.asksaveasfile(mode='w', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")
        if savebox:
            # text_data = str('HEEEEEEYYYYY')
            # days_list = range(1,10)
            # df=pd.DataFrame({"Day":days_list,"Min\nTemp":['']*len(days_list),
            #                    "Max\nTemp":['']*len(days_list),
            #                    "Humidity":['']*len(days_list),
            #                    "Wind":['']*len(days_list),
            #                    'Sun\nhours':['']*len(days_list),
            #                    "Eto":["0"]*len(days_list)})
            df.to_csv(savebox, index=False)
            savebox.close()


class tabTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        main_frame = tk.Frame(self)
        main_frame.place(in_=self, anchor='c', relx=.5, rely=.5)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT)

        init_frame = tk.LabelFrame(left_frame, bd=3, height=50, width=450,
                                   text="Initial stage", relief="groove",
                                   font=LARGE_FONT)
        init_frame.pack(padx=10, pady=10)
        init_frame.pack_propagate(False)
        init_frame.grid_propagate(False)
        kc_init_lbl = tk.Label(init_frame, text="Kc (tab)")
        kc_init_lbl.grid(row=0, column=0, padx=5, pady=2)
        kc_init_ent = tk.Entry(init_frame)
        kc_init_ent.grid(row=0, column=1, padx=5, pady=2)
        stage_init_lbl = tk.Label(init_frame, text="Stages (day)")
        stage_init_lbl.grid(row=0, column=2, padx=5, pady=2)
        stage_init_ent = tk.Entry(init_frame)
        stage_init_ent.grid(row=0, column=3, padx=5, pady=2)

        mid_frame = tk.LabelFrame(left_frame, bd=3, height=100, width=450,
                                  text="Mid stage", relief="groove",
                                  font=LARGE_FONT)
        mid_frame.pack(padx=10, pady=10)
        mid_frame.pack_propagate(False)
        mid_frame.grid_propagate(False)
        kc_mid_lbl = tk.Label(mid_frame, text="Kc (tab)")
        kc_mid_lbl.grid(row=0, column=0, padx=5, pady=2)
        kc_mid_ent = tk.Entry(mid_frame)
        kc_mid_ent.grid(row=0, column=1, padx=5, pady=2)
        stage_mid_lbl = tk.Label(mid_frame, text="Stages (day)")
        stage_mid_lbl.grid(row=0, column=2, padx=5, pady=2)
        stage_mid_ent = tk.Entry(mid_frame)
        stage_mid_ent.grid(row=0, column=3, padx=5, pady=2)
        kc2_mid_lbl = tk.Label(mid_frame, text="Kc (Cal)")
        kc2_mid_lbl.grid(row=1, column=0, padx=5, pady=2)
        kc2_mid_but = ttk.Button(mid_frame, text="Calculate",
                                 command=self.calculateMid)
        kc2_mid_but.grid(row=1, column=1, padx=5, pady=2)
        crop_mid_lbl = tk.Label(mid_frame, text="Crop height (m)")
        crop_mid_lbl.grid(row=1, column=2, padx=5, pady=2)
        crop_mid_ent = tk.Entry(mid_frame)
        crop_mid_ent.grid(row=1, column=3, padx=5, pady=2)

        late_frame = tk.LabelFrame(left_frame, bd=3, height=100, width=450,
                                   text="Late stage", relief="groove",
                                   font=LARGE_FONT)
        late_frame.pack(padx=10, pady=10)
        late_frame.pack_propagate(False)
        late_frame.grid_propagate(False)
        kc_late_lbl = tk.Label(late_frame, text="Kc (tab)")
        kc_late_lbl.grid(row=0, column=0, padx=5, pady=2)
        kc_late_ent = tk.Entry(late_frame)
        kc_late_ent.grid(row=0, column=1, padx=5, pady=2)
        stage_late_lbl = tk.Label(late_frame, text="Stages (day)")
        stage_late_lbl.grid(row=0, column=2, padx=5, pady=2)
        stage_late_ent = tk.Entry(late_frame)
        stage_late_ent.grid(row=0, column=3, padx=5, pady=2)
        kc2_late_lbl = tk.Label(late_frame, text="Kc (Cal)")
        kc2_late_lbl.grid(row=1, column=0, padx=5, pady=2)
        kc2_late_but = ttk.Button(late_frame, text="Calculate",
                                  command=self.calculateLate)
        kc2_late_but.grid(row=1, column=1, padx=5, pady=2)
        crop_late_lbl = tk.Label(late_frame, text="Crop height (m)")
        crop_late_lbl.grid(row=1, column=2, padx=5, pady=2)
        crop_late_ent = tk.Entry(late_frame)
        crop_late_ent.grid(row=1, column=3, padx=5, pady=2)

        table_frame = tk.Frame(right_frame, height=400, width=300, bg="grey",
                               bd=3)
        table_frame.pack(pady=10)
        table_frame.grid_propagate(False)
        table_frame.pack_propagate(False)
        scrl_table_frame = ScrollableFrame(table_frame, height=400, width=300,
                                           borderwidth=3, add_x=True)
        scrl_table_frame.pack(fill="y", expand=True)
        scrl_table_frame.grid_propagate(False)
        scrl_table_frame.pack_propagate(False)
        start_date = "20/02"
        end_date = "15/03"
        days_list = calculateDays(start_date, end_date)
        headers, df = self.format_table(days_list)
        header_units = ["", "mm/day", "", "mm/day"]
        self.table_obj = tableWidget(scrl_table_frame.scrollable_frame, df=df,
                                     rows=len(days_list)+1,
                                     header_units=header_units,
                                     columns=len(headers), headers=headers,
                                     font=False)
        self.table_obj.pack(side=tk.LEFT)

        but_frame = tk.Frame(left_frame, height=100, width=425)
        but_frame.pack(padx=20, side=tk.BOTTOM, pady=20)
        but_frame.grid_propagate(False)
        but_frame.pack_propagate(False)

        save_but = ttk.Button(but_frame, text="Save", command=self.saveFile)
        save_but.grid(row=0, column=0, padx=5, pady=5)

        import_but = ttk.Button(but_frame, text="Import",
                                command=self.importFile)
        import_but.grid(row=0, column=1, padx=5, pady=5)

        insert_but = ttk.Button(but_frame, text="Insert",
                                command=self.InsertData)
        insert_but.grid(row=0, column=2, padx=5, pady=5)

    def calculate(self):
        pass

    def InsertData(self):
        pass

    def importFile(self):
        path = os.getcwd()
        importbox = filedialog.askopenfile(mode='r', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")
        # headers=["Min\nTemp", "Max\nTemp", "Humidity", "Wind", 'Sun\nhours']
        data = pd.read_csv(importbox, index_col=None, usecols=["Min\nTemp",
                                                               "Max\nTemp",
                                                               "Humidity",
                                                               "Wind",
                                                               'Sun\nhours']
                           ).fillna("0")
        importbox.close()

    def saveFile(self):
        pass

    def calculateMid(self):
        pass

    def calculateLate(self):
        pass

    def format_table(self, days_list):
        headers = ["Day", "ETo", "Kc", "ETc"]
        df = pd.DataFrame({"Day": days_list,
                           "ETo": ["0"]*len(days_list),
                           "Kc": ["0"]*len(days_list),
                           "ETc": ["0"]*len(days_list)}, columns=headers)
        return headers, df


class tabThree(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        main_frame = tk.Frame(self, height=500, width=350)
        main_frame.pack()

        left_frame = tk.Frame(main_frame, width=200, height=200, bd=3,
                              relief="groove")
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

        self.set_radio_vars()

        for self.p_val, self.p_opt in enumerate(self.p_options):
            if not self.p_val:
                temp = tk.Frame(left_frame)
                temp.grid(row=0, column=0, sticky="w", pady=10, padx=10)
                p_rad = ttk.Radiobutton(temp,
                                        text=self.p_opt,
                                        variable=self.p_v,
                                        value=self.p_val)
                p_rad.grid(row=0, column=0, sticky='w')
                perc_ent = tk.Entry(temp, width=5)
                perc_ent.grid(row=0, column=1, sticky='w')
                perc_ent.insert("0", "80")
                perc_lbl = tk.Label(temp, text='%')
                perc_lbl.grid(row=0, column=2)
            else:
                p_rad = ttk.Radiobutton(left_frame,
                                        text=self.p_opt,
                                        variable=self.p_v,
                                        value=self.p_val)
                p_rad.grid(row=self.p_val, column=0, sticky='w', pady=10,
                           padx=10)

        mid_frame = tk.Frame(main_frame)
        mid_frame.pack(side=tk.LEFT)
        table_frame = tk.Frame(mid_frame, height=500, width=225, bg="grey",
                               bd=3)
        table_frame.pack(pady=10)
        table_frame.grid_propagate(False)
        table_frame.pack_propagate(False)
        scrl_table_frame = ScrollableFrame(table_frame, height=500, width=225,
                                           borderwidth=3, add_x=True)
        scrl_table_frame.pack(fill="y", expand=True)
        scrl_table_frame.grid_propagate(False)
        scrl_table_frame.pack_propagate(False)
        start_date = "20/02"
        end_date = "15/03"
        days_list = calculateDays(start_date, end_date)
        headers, df = self.format_table(days_list)
        header_units = ["", "mm", "mm"]
        self.table_obj = tableWidget(scrl_table_frame.scrollable_frame, df=df,
                                     rows=len(days_list)+1,
                                     header_units=header_units,
                                     columns=len(headers), headers=headers,
                                     font=False)
        self.table_obj.pack(side=tk.LEFT)

        but_frame = tk.Frame(main_frame, height=300, width=100)
        but_frame.pack(padx=20, side=tk.BOTTOM, pady=20)
        but_frame.grid_propagate(False)
        but_frame.pack_propagate(False)

        save_but = ttk.Button(but_frame, text="Save", command=self.saveFile)
        save_but.pack(pady=5, fill="x", side=tk.BOTTOM)

        import_but = ttk.Button(but_frame, text="Import",
                                command=self.importFile)
        import_but.pack(pady=5, fill="x", side=tk.BOTTOM)

        calc_but = ttk.Button(but_frame, text="Calculate",
                              command=self.calculate)
        calc_but.pack(pady=5, fill="x", side=tk.BOTTOM)

    def format_table(self, days_list):
        headers = ["Day", "P", "Pe"]
        df = pd.DataFrame({"Day": days_list,
                           "P": ["0"]*len(days_list),
                           "Pe": ["0"]*len(days_list)}, columns=headers)
        return headers, df

    def set_radio_vars(self):
        self.p_v = tk.IntVar()
        self.p_v.set(0)
        self.p_options = ["Fixed percentage", "Dependable rain",
                          "USDA soil conservation service"]

    def calculate(self):
        pass

    def importFile(self):
        path = os.getcwd()
        importbox = filedialog.askopenfile(mode='r', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")

        # headers=["Min\nTemp", "Max\nTemp", "Humidity", "Wind", 'Sun\nhours']
        data = pd.read_csv(importbox, index_col=None, usecols=["Min\nTemp",
                                                               "Max\nTemp",
                                                               "Humidity",
                                                               "Wind",
                                                               'Sun\nhours']
                           ).fillna("0")

        importbox.close()

    def saveFile(self):
        path = os.getcwd()
        savebox = filedialog.asksaveasfile(mode='w', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")
        if savebox:
            df.to_csv(savebox, index=False)
            savebox.close()


class tabFour(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        main_frame = tk.Frame(self, height=500, width=350, bd=0,
                              relief="groove")
        main_frame.pack()

        temp_frame = tk.Frame(main_frame, width=200, height=25,
                             relief="groove", bd=0)
        temp_frame.pack(padx=5, pady=5)

        top_frame = tk.Frame(main_frame, width=200, height=75,
                             relief="groove", bd=1)
        top_frame.pack(padx=5, pady=5)

        self.std_v = tk.IntVar()
        self.std_v.set(0)
        self.std_check = tk.Checkbutton(top_frame,
                                        text="Under standard\nconditions",
                                        variable=self.std_v,
                                        command=self.checkState,
                                        font=NORM_FONT)
        self.std_check.grid(row=0, column=0, padx=5, pady=5)

        self.stress_v = tk.IntVar()
        self.stress_v.set(0)
        self.stress_check = tk.Checkbutton(top_frame,
                                           text="Under soil water\nstress"+\
                                           "conditions",
                                           variable=self.stress_v,
                                           command=self.checkState,
                                           font=NORM_FONT)
        self.stress_check.grid(row=0, column=1, padx=5, pady=5)

        self.saint_v = tk.IntVar()
        self.saint_v.set(0)
        self.saint_check = tk.Checkbutton(top_frame, text="Soil sainity",
                                          variable=self.saint_v,
                                          command=self.checkState,
                                          font=NORM_FONT)
        self.saint_check.grid(row=0, column=2, padx=5, pady=5)

        temp_frame = tk.Frame(main_frame, width=200, height=20,
                              relief="groove", bd=0)
        temp_frame.pack(padx=5, pady=5)

        mid_frame = tk.Frame(main_frame, width=550, height=100,
                             relief="groove", bd=1)
        mid_frame.pack(padx=5, pady=5)
        mid_frame.pack_propagate(False)
        mid_frame.grid_propagate(False)

        soil_frame = tk.Frame(mid_frame)
        soil_frame.grid(row=0, column=0, padx=5, pady=2)
        soil_lbl = tk.Label(soil_frame, text="Soil name", font=NORM_FONT)
        soil_lbl.grid(row=0, columnspan=2, sticky='w')
        self.soil_v = tk.StringVar()
        self.soil_options = ["Coarse sand", "Fine sand", "Loamy sand",
                             "Sandy loam", "Fine sandy loam", "Silt loam",
                             "Silty clay loam", "Silty clay", "Clay"]
        self.soil_v.set(self.soil_options[0])
        self.soil_menu = ttk.OptionMenu(soil_frame, self.soil_v,
                                        *self.soil_options)
        self.soil_menu.grid(row=1, column=1, sticky="e")
        self.soil_menu.config(width=20)

        maxrd_frame = tk.Frame(mid_frame)
        maxrd_frame.grid(row=0, column=1, padx=5, pady=2)
        maxrd_lbl = tk.Label(maxrd_frame, text="Maximum rooting depth",
                             font=NORM_FONT)
        maxrd_lbl.grid(row=0, columnspan=2, sticky='w')
        maxrd_metrics_lbl = tk.Label(maxrd_frame, text="(mm)", font=NORM_FONT)
        maxrd_metrics_lbl.grid(row=1, column=0)
        self.maxrd_outlbl = tk.Entry(maxrd_frame, bg="grey")
        self.maxrd_outlbl.config(state="readonly")
        self.maxrd_outlbl.grid(row=1, column=1)

        dep_frec_frame = tk.Frame(mid_frame)
        dep_frec_frame.grid(row=0, column=2, padx=5, pady=2)
        dep_frec_lbl = tk.Label(dep_frec_frame, text="Depletion fraction",
                                font=NORM_FONT)
        dep_frec_lbl.grid(row=0, columnspan=2, sticky='w')
        dep_frec_lbl = tk.Label(dep_frec_frame, text="(%)", font=NORM_FONT)
        dep_frec_lbl.grid(row=1, column=0)
        self.dep_frec_outlbl = tk.Entry(dep_frec_frame, bg="grey")
        self.dep_frec_outlbl.config(state="readonly")
        self.dep_frec_outlbl.grid(row=1, column=1)

        avawhc_frame = tk.Frame(mid_frame)
        avawhc_frame.grid(row=1, column=0, padx=5, pady=2)
        avawhc_lbl = tk.Label(avawhc_frame,
                              text="Available water holding capacity",
                              font=NORM_FONT)
        avawhc_lbl.grid(row=0, columnspan=2, sticky='w')
        avawhc_lbl = tk.Label(avawhc_frame, text="(mm/m)", font=NORM_FONT)
        avawhc_lbl.grid(row=1, column=0)
        self.avawhc_outlbl = tk.Entry(avawhc_frame, bg="grey")
        self.avawhc_outlbl.config(state="readonly")
        self.avawhc_outlbl.grid(row=1, column=1)

        totav_frame = tk.Frame(mid_frame)
        totav_frame.grid(row=1, column=1, padx=5, pady=2)
        totav_lbl = tk.Label(totav_frame, text="Total available water",
                             font=NORM_FONT)
        totav_lbl.grid(row=0, columnspan=2, sticky='w')
        totav_lbl = tk.Label(totav_frame, text="(mm)", font=NORM_FONT)
        totav_lbl.grid(row=1, column=0)
        self.totav_outlbl = tk.Entry(totav_frame, bg="grey")
        self.totav_outlbl.config(state="readonly")
        self.totav_outlbl.grid(row=1, column=1)

        readav_frame = tk.Frame(mid_frame)
        readav_frame.grid(row=1, column=2, padx=5, pady=2)
        readav_lbl = tk.Label(readav_frame, text="Readily available water",
                              font=NORM_FONT)
        readav_lbl.grid(row=0, columnspan=2, sticky='w')
        readav_lbl = tk.Label(readav_frame, text="(mm)", font=NORM_FONT)
        readav_lbl.grid(row=1, column=0)
        self.readav_outlbl = tk.Entry(readav_frame, bg="grey")
        self.readav_outlbl.config(state="readonly")
        self.readav_outlbl.grid(row=1, column=1)

        temp_frame = tk.Frame(main_frame, width=200, height=20,
                              relief="groove", bd=0)
        temp_frame.pack(padx=5, pady=5)

        lower_frame = tk.Frame(main_frame, width=550, height=100,
                               relief="groove", bd=1)
        lower_frame.pack(padx=5, pady=5)
        lower_frame.grid_propagate(False)
        lower_frame.pack_propagate(False)

        isys_frame = tk.Frame(lower_frame)
        isys_frame.grid(row=0, column=0, padx=3, pady=2)
        isys_lbl = tk.Label(isys_frame, text="Irrigation system",
                            font=NORM_FONT)
        isys_lbl.grid(row=0, columnspan=2, sticky='w')
        self.isys_v = tk.StringVar()
        self.isys_options = ["Surface Irrigation", "Drip Irrigation",
                             "Sprinkler Irrigation"]
        self.isys_v.set(self.isys_options[0])
        self.isys_menu = ttk.OptionMenu(isys_frame, self.isys_v,
                                        *self.isys_options)
        self.isys_menu.grid(row=1, column=1, sticky='e')
        self.isys_menu.config(width=20)

        iint_frame = tk.Frame(lower_frame)
        iint_frame.grid(row=0, column=1, padx=3, pady=2)
        iint_lbl = tk.Label(iint_frame, text="Irrigation intervales",
                            font=NORM_FONT)
        iint_lbl.grid(row=0, columnspan=2, sticky='w')
        self.iint_v = tk.StringVar()
        self.iint_options = ["Irrigation at critical depletion", "15 days",
                             "10 days", "3 days", "1 day"]
        self.iint_v.set(self.iint_options[0])
        self.iint_menu = ttk.OptionMenu(iint_frame, self.iint_v,
                                        *self.iint_options)
        self.iint_menu.grid(row=1, column=1, sticky='e')
        self.iint_menu.config(width=20)

        iapp_frame = tk.Frame(lower_frame)
        iapp_frame.grid(row=0, column=2, padx=5, pady=2)
        iapp_lbl = tk.Label(iapp_frame, text="Irrigation Application (mm)",
                            font=NORM_FONT)
        iapp_lbl.grid(row=0, columnspan=2, sticky='w')
        self.iapp_v = tk.StringVar()
        self.iapp_options = ["Refill soil to Field capacity",
                             "Adjusted by user"]
        self.iapp_v.set(self.iapp_options[0])
        self.iapp_menu = ttk.OptionMenu(iapp_frame, self.iapp_v,
                                        *self.iapp_options)
        self.iapp_menu.grid(row=1, column=1, sticky='e')
        self.iapp_menu.config(width=20)

        feff_frame = tk.Frame(lower_frame)
        feff_frame.grid(row=1, column=0, padx=5, pady=2)
        feff_lbl = tk.Label(feff_frame, text="Field efficiency (%)",
                            font=NORM_FONT)
        feff_lbl.grid(row=0, columnspan=2, sticky='w')
        self.feff_ent = tk.Entry(feff_frame)
        self.feff_ent.grid(row=1, columnspan=2, sticky='e')

        ece_frame = tk.Frame(lower_frame)
        ece_frame.grid(row=1, column=1, padx=5, pady=2)
        ece_lbl = tk.Label(ece_frame, text="ECe (ds/m)", font=NORM_FONT)
        ece_lbl.grid(row=0, columnspan=2, sticky='w')
        self.ece_ent = tk.Entry(ece_frame)
        self.ece_ent.grid(row=1, column=1)

        ecw_frame = tk.Frame(lower_frame)
        ecw_frame.grid(row=1, column=2, padx=5, pady=2)
        ecw_lbl = tk.Label(ecw_frame, text="ECw (ds/m)", font=NORM_FONT)
        ecw_lbl.grid(row=0, columnspan=2, sticky='w')
        self.ecw_ent = tk.Entry(ecw_frame)
        self.ecw_ent.grid(row=1, column=1)

        self.hidden_frame = tk.Frame(main_frame, width=550, height=75, bd=1)
        self.hidden_frame.pack(side=tk.LEFT, padx=5, pady=5)
        self.hidden_frame.grid_propagate(False)
        self.hidden_frame.pack_propagate(False)

        save_but = ttk.Button(main_frame, text="Save")
        save_but.pack(side=tk.LEFT, anchor="ne", pady=25)

    def checkState(self):
        if self.std_v.get():
            self.saint_check.config(state=tk.DISABLED)
            self.stress_check.config(state=tk.DISABLED)
        else:
            self.saint_check.config(state=tk.NORMAL)
            self.stress_check.config(state=tk.NORMAL)

        if self.saint_v.get() or self.stress_v.get():
            self.std_check.config(state=tk.DISABLED)
            self.changeState()
        else:
            self.std_check.config(state=tk.NORMAL)
            self.changeState()

    def changeState(self):
        if self.saint_v.get():
            self.hidden_frame.config(relief="groove", bd=0)

            self.ece_thresh_frame = tk.Frame(self.hidden_frame)
            self.ece_thresh_frame.grid(row=0, column=0, padx=5, pady=2)
            ece_thresh_lbl = tk.Label(self.ece_thresh_frame,
                                      text="ECe threshold", font=NORM_FONT)
            ece_thresh_lbl.grid(row=0, columnspan=2, sticky='w')
            ece_thresh_lbl = tk.Label(self.ece_thresh_frame, text="(ds/m)")
            ece_thresh_lbl.grid(row=1, column=0)
            self.ece_thresh_outlbl = tk.Entry(self.ece_thresh_frame, bg="grey")
            self.ece_thresh_outlbl.config(state="readonly")
            self.ece_thresh_outlbl.grid(row=1, column=1)

            self.b_frame = tk.Frame(self.hidden_frame)
            self.b_frame.grid(row=0, column=1, padx=5, pady=2)
            b_lbl = tk.Label(self.b_frame, text="b")
            b_lbl.grid(row=0, columnspan=2, sticky='w')
            b_lbl = tk.Label(self.b_frame, text="(ds/m)")
            b_lbl.grid(row=1, column=0)
            self.b_outlbl = tk.Entry(self.b_frame, bg="grey")
            self.b_outlbl.config(state="readonly")
            self.b_outlbl.grid(row=1, column=1)

            self.yrfact_frame = tk.Frame(self.hidden_frame)
            self.yrfact_frame.grid(row=0, column=2, padx=5, pady=2)
            yrfact_lbl = tk.Label(self.yrfact_frame, text="Yield response")
            yrfact_lbl.grid(row=0, columnspan=2, sticky='w')
            yrfact_lbl = tk.Label(self.yrfact_frame, text="factor")
            yrfact_lbl.grid(row=1, column=0)
            self.yrfact_outlbl = tk.Entry(self.yrfact_frame, bg="grey")
            self.yrfact_outlbl.config(state="readonly")
            self.yrfact_outlbl.grid(row=1, column=1)
        else:
            self.hidden_frame.config(bd=0)
            try:
                self.ece_thresh_frame.destroy()
                self.b_frame.destroy()
                self.yrfact_frame.destroy()
            except AttributeError:
                pass

    def saveFile(self):
        path = os.getcwd()
        savebox = filedialog.asksaveasfile(mode='w', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")
        if savebox:
            df.to_csv(savebox, index=False)
            savebox.close()


class tabFive(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        main_frame = tk.Frame(self, height=500, width=600)
        main_frame.pack()

        temp_frame = tk.Frame(main_frame, width=200, height=25,
                              relief="groove", bd=0)
        temp_frame.pack(padx=5, pady=5)

        table_frame = tk.Frame(main_frame, height=300, width=600, bg="grey",
                               bd=3)
        table_frame.pack(side=tk.TOP, expand=True, fill="both")
        scrl_table_frame = ScrollableFrame(table_frame, height=300, width=500,
                                           borderwidth=3, add_x=True)
        scrl_table_frame.pack(fill='both', expand=True)
        scrl_table_frame.grid_propagate(False)
        scrl_table_frame.pack_propagate(False)
        start_date = "20/02"
        end_date = "15/03"
        days_list = calculateDays(start_date, end_date)
        headers, df = self.format_table(days_list)
        header_units = ["", 'mm/day', 'mm', "mm/day", "", "mm/day", "mm",
                        "mm/day", "mm/day"]
        self.table_obj = tableWidget(scrl_table_frame.scrollable_frame, df=df,
                                     headers=headers,
                                     header_units=header_units,
                                     rows=len(days_list)+1,
                                     columns=len(headers),
                                     font=NORM_FONT)
        self.table_obj.pack(fill='both', expand=True)

        lower_frame = tk.Frame(main_frame, bd=3, relief="groove")
        lower_frame.pack(anchor="c", pady=10, padx=5, side=tk.LEFT)

        totgrir_frame = tk.Frame(lower_frame)
        totgrir_frame.grid(row=0, column=0, padx=5, pady=2)
        totgrir_lbl = tk.Label(totgrir_frame, text="Total Gross Irr.",
                               font=NORM_FONT)
        totgrir_lbl.grid(row=0, columnspan=2, sticky='w')
        totgrir_lbl = tk.Label(totgrir_frame, text="(mm)", font=NORM_FONT)
        totgrir_lbl.grid(row=1, column=0)
        self.totgrir_outlbl = tk.Entry(totgrir_frame, bg="grey")
        self.totgrir_outlbl.config(state="readonly")
        self.totgrir_outlbl.grid(row=1, column=1)

        get_frame = tk.Frame(lower_frame)
        get_frame.grid(row=0, column=1, padx=5, pady=2)
        get_lbl = tk.Label(get_frame, text="Green ET", font=NORM_FONT)
        get_lbl.grid(row=0, columnspan=2, sticky='w')
        get_lbl = tk.Label(get_frame, text="(mm)", font=NORM_FONT)
        get_lbl.grid(row=1, column=0)
        self.get_outlbl = tk.Entry(get_frame, bg="grey")
        self.get_outlbl.config(state="readonly")
        self.get_outlbl.grid(row=1, column=1)

        bet_frame = tk.Frame(lower_frame)
        bet_frame.grid(row=0, column=2, padx=5, pady=2)
        bet_lbl = tk.Label(bet_frame, text="Blue ET", font=NORM_FONT)
        bet_lbl.grid(row=0, columnspan=2, sticky='w')
        bet_lbl = tk.Label(bet_frame, text="(mm)", font=NORM_FONT)
        bet_lbl.grid(row=1, column=0)
        self.bet_outlbl = tk.Entry(bet_frame, bg="grey")
        self.bet_outlbl.config(state="readonly")
        self.bet_outlbl.grid(row=1, column=1)

        but_frame = tk.Frame(main_frame)
        but_frame.pack(side=tk.LEFT)
        save_but = ttk.Button(but_frame, text="Save", command=self.saveFile)
        save_but.pack(anchor='s')
        next_but = ttk.Button(but_frame, text="Next", command=self.nextPage)
        next_but.pack(anchor='s')

    def nextPage(self):

        self.controller.show_frame(water_analysis.waterAnalysis)

    def saveFile(self):
        path = os.getcwd()
        savebox = filedialog.asksaveasfile(mode='w', initialdir=path,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("all files", "*.*")),
                                           defaultextension=".csv")
        if savebox:
            df.to_csv(savebox, index=False)
            savebox.close()

    def format_table(self, days_list):
        headers = ["Day", "ETc", "Pe", "Dr", "Ks", "ETc\n(adj)", "Net\nIrr",
                   "LR", "Gross\nIrr"]
        df = pd.DataFrame({"Day": days_list, "ETc": ['0']*len(days_list),
                           "Pe": ['0']*len(days_list),
                           "Dr": ['0']*len(days_list),
                           "Ks": ['0']*len(days_list),
                           'ETc\n(adj)': ['0']*len(days_list),
                           "Net\nIrr": [""]*len(days_list),
                           "LR": ['0']*len(days_list),
                           "Gross\nIrr": ['0']*len(days_list)},
                          columns=headers)
        return headers, df


class ScrollableFrame(tk.Frame):
    def __init__(self, container, add_x=False, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=canvas.yview)
        scrollbar2 = ttk.Scrollbar(self, orient="horizontal",
                                   command=canvas.xview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="left", fill="y")
        if add_x:
            scrollbar2.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)


class tableWidget(tk.Frame):
    def __init__(self, parent, headers, header_units, df, columns, font,
                 rows=2):
        # use black background so it "peeks through" to
        # form grid lines
        super().__init__(parent, background="gray")
        self._widgets = []

        header_row = []
        for column in range(columns):
            label = ttk.Label(self, text="%s" % (headers[column]),
                              borderwidth=0, width=10)
            if font:
                label.config(font=font)
            label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            header_row.append(label)
        self._widgets.append(header_row)

        for column in range(columns):
            label = ttk.Label(self, text="%s" % (header_units[column]),
                              borderwidth=0, width=10)
            if font:
                label.config(font=font)
            label.grid(row=1, column=column, sticky="nsew", padx=1, pady=1)
            header_row.append(label)
        self._widgets.append(header_row)

        for row in range(rows-2):
            current_row = []
            for column in range(columns):
                if not df.iloc[row, column]:
                    label = ttk.Entry(self, width=10)
                    label.grid(row=row+2, column=column, sticky="nsew", padx=1,
                               pady=1)
                    current_row.append(label)
                else:
                    label = ttk.Label(self,
                                      text="%s" % str(df.iloc[row, column]),
                                      borderwidth=0, width=10)
                    if font:
                        label.config(font=font)
                    label.grid(row=row+2, column=column, sticky="nsew", padx=1,
                               pady=1)
                    current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def insert_text(self, row, column, value):
        widget = self._widgets[row][column]
        widget.delete("0", 'end')
        widget.insert('0', value)