import datetime

def check_date(ent, format, msg, status_var=None, status_bar=None):
    try:
        datetime.datetime.strptime(ent.get(), format)
        return True
    except ValueError:
        status_var.set(msg)
        status_bar.config(fg="red")
        return False

def check_field_type(val, data_type, msg, status_var=None,
                     status_bar=None):
    try:
        data_type(val)
        return True
    except ValueError:
        status_var.set(msg)
        status_bar.config(fg="red")
        return False

def check_field_nonempty(ent, msg, status_var=None, status_bar=None):
    if ent.get():
        return True
    else:
        status_var.set(msg)
        status_bar.config(fg="red")
        return False

def compare_dates(date1, date2, msg, status_var=None, status_bar=None):
    d1, m1, y1 = date1.split('/')
    d2, m2, y2 = date2.split('/')
    date1 = datetime.datetime(int(y1), int(m1), int(d1))
    date2 = datetime.datetime(int(y2), int(m2), int(d2))
    if date1 - date2 >= datetime.timedelta(60):
        return True
    else:
        status_var.set(msg)
        status_bar.config(fg="red")
        return False

def compare_values(val1, val2, msg, status_var=None, status_bar=None):
    if val1 >= val2:
        return True
    else:
        status_var.set(msg)
        status_bar.config(fg="red")
        return False
