import sqlite3 as sq
from datetime import datetime
def start_sql():
    with sq.connect('new.db') as db:
        cursor=db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS 
                    client_(ident TEXT, dates TEXT, times TEXT)''')


def search_bd_id(callback):
    with sq.connect('new.db') as db:
        cursor = db.cursor()
        id = cursor.execute('''SELECT ident FROM client_ 
                            WHERE ident = ?''', (callback,)).fetchall()
    return id

def search_bd_date_time(date_time, time):
    with sq.connect('new.db') as db:
        cursor = db.cursor()
        date = cursor.execute('''SELECT dates FROM client_ 
                               WHERE dates = ?''', (date_time,)).fetchall()
        time = cursor.execute('''SELECT times FROM client_ 
                                       WHERE times = ?''', (time,)).fetchall()
        try:
            if date[0] and time[0]:
                return True
        except IndexError:
            return False
        print(date)
        print(time)

search_bd_date_time('15.02.2024', '14:00')

def add_users(callback, date, time):
    with sq.connect('new.db') as db:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO client_ VALUES(?, ?, ?) ",
                       (callback, date, time))


def delete_users(callback):
    with sq.connect('new.db') as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM client_ WHERE ident = ?', (callback,))


def shedul(date_time):
    with sq.connect('new.db') as db:
        cursor = db.cursor()
        date = cursor.execute('''SELECT dates FROM client_ 
                               WHERE dates = ?''', (date_time,)).fetchall()
    if datetime.now().strftime("%d.%m.%Y")==date[0]:
        return True

print(datetime.now().strftime("%d.%m.%Y"))
# def delete_time_user():
#     with sq.connect('new.db') as db:
#         cursor = db.cursor()
#         cursor.execute("DELETE FROM client_ WHERE dates=? <datetime('now')")