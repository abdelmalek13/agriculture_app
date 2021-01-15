import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
# root = tk.Tk()
# root.geometry("300x200")
# s = ttk.Style()
#
# tab_parent = ttk.Notebook(root)
# tab1 = ttk.Frame(tab_parent)
# tab_parent.add(tab1, text="All Records")
# tab_parent.pack(expand=True, fill='both')
# # navbar = Frame(root, width=100)
# # navbar.pack(anchor=W, fill=Y, expand=False, side=LEFT)  # <----
# # s.configure("Forbid.TButton", foreground="#FB0C04", background='#FB0C04')
# # but = ttk.Button(navbar,style="Forbid.TButton")
# # but.pack()
#
# # s.map('Forbid.TButton', background=[('active', '#000000')])
#
# # # tkvar = tk.StringVar(navbar)
# # content_frame = Frame(root, bg="orange")
# # content_frame.pack(anchor=N, fill=BOTH, expand=True, side=LEFT )
# root.mainloop()

#
# class ExampleApp(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         t = SimpleTable(self, 10,8)
#         t.pack(side="top", fill="x")
#         # t.set(0,0,"Hello, world")
#
# class SimpleTable(tk.Frame):
#     def __init__(self, parent, rows=10, columns=8):
#         # use black background so it "peeks through" to
#         # form grid lines
#         tk.Frame.__init__(self, parent, background="black")
#         self._widgets = []
#
#         header_col = []
#         headers=['Index', "Day", "Min\nTemp", "Max\nTemp", "Humidity", "Wind",
#                  'Sun\nhours', "Eto"]
#         for column in range(columns):
#             label = ttk.Label(self, text="%s" % (headers[column]),
#                              borderwidth=0, width=10)
#             label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
#             header_col.append(label)
#         self._widgets.append(header_col)
#
#         for row in range(rows-1):
#             current_row = []
#             for column in range(columns):
#                 label = ttk.Label(self, text="%s/%s" % (row, column),
#                                  borderwidth=0, width=10)
#                 label.grid(row=row+1, column=column, sticky="nsew", padx=1, pady=1)
#                 current_row.append(label)
#             self._widgets.append(current_row)
#         print(self._widgets)
#         for column in range(columns):
#             self.grid_columnconfigure(column, weight=1)
#
#
#     def set(self, row, column, value):
#         widget = self._widgets[row][column]
#         widget.configure(text=value)
#
# if __name__ == "__main__":
#     app = ExampleApp()
#     app.mainloop()


#
# class ExampleApp(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         t = SimpleTable(self, 10,7)
#         t.pack(side="top", fill="x")
#         # t.set(0,0,"Hello, world")
#
# class SimpleTable(tk.Frame):
#     def __init__(self, parent, rows=10, columns=7):
#         # use black background so it "peeks through" to
#         # form grid lines
#         tk.Frame.__init__(self, parent, background="gray")
#         self._widgets = []
#
#         header_col = []
#         headers=[ "Day", "Min\nTemp", "Max\nTemp", "Humidity", "Wind",
#                  'Sun\nhours', "Eto"]
#         ds = list(range(1,10))
#         df = pd.DataFrame({"Day":pd.Series(ds),"Min\nTemp":['']*len(ds),
#                            "Max\nTemp":['']*len(ds), "Humidity":['']*len(ds),
#                            "Wind":['']*len(ds),'Sun\nhours':['']*len(ds),
#                            "Eto":["0"]*len(ds)}, columns=headers)
#         # print(df.head())
#         header_col = []
#         for column in range(columns):
#             label = ttk.Label(self, text="%s" % (headers[column]),
#                              borderwidth=0, width=10)
#             label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
#             header_col.append(label)
#         self._widgets.append(header_col)
#
#         for row in range(rows-1):
#             current_row = []
#             for column in range(columns):
#                 # print(row,column)
#                 if not df.iloc[row, column]:
#                     # print(row, column)
#                     label = ttk.Entry(self,width=10)
#                     label.grid(row=row+1, column=column, sticky="nsew", padx=1, pady=1)
#                     current_row.append(label)
#                 else:
#                     label = ttk.Label(self, text="%s" % str(df.iloc[row, column]),
#                                      borderwidth=0, width=10)
#                     label.grid(row=row+1, column=column, sticky="nsew", padx=1, pady=1)
#                     current_row.append(label)
#             self._widgets.append(current_row)
#
#         for column in range(columns):
#             self.grid_columnconfigure(column, weight=1)
#
#         # for i in range(10):
#         #     for j in range(7):
#         #         print(i,j,self._widgets[i][j].__class__,self._widgets[i][j].cget("text"))
#                 # print(i,j,col.__class__,col.cget("text"))
#
#
#     def set(self, row, column, value):
#         widget = self._widgets[row][column]
#         widget.configure(text=value)
#
#     def insert_text(self, row, column, value):
#         widget = self._widgets[row][column]
#         widget.insert('0',value)
#
# if __name__ == "__main__":
#     app = ExampleApp()
#     app.mainloop()

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

root = tk.Tk()

frame = ScrollableFrame(root)

for i in range(50):
    ttk.Label(frame.scrollable_frame, text="Sample scrolling label").pack()

frame.pack()
root.mainloop()
