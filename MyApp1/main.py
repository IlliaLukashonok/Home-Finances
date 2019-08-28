import tkinter as tk
from tkinter import ttk
import sqlite3 as sql

VERSION = '2.1.0'

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
        self.update_current()


    def init_main(self):
        toolbar = tk.Frame(bg='#D7D8E0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="data\\add.png")
        btn_open_dialog = tk.Button(
                            toolbar,
                            text='Add position',
                            command=self.open_dialog,
                            bg='#D7D8E0',
                            bd=0,
                            compound=tk.TOP,
                            image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='data\\update.png')

        btn_edit_dialog = tk.Button(
            toolbar,
            text='Edit',
            bg='#D7D8E0',
            bd=0,
            image=self.update_img,
            compound=tk.TOP,
            command=self.open_update_dialog)

        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='data\\delete.png')
        btn_delete = tk.Button(
            toolbar,
            text='Delete',
            bg='#D7D8E0',
            bd=0,
            image=self.delete_img,
            compound=tk.TOP,
            command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        
        self.update_curr_img = tk.PhotoImage(file='data\\upd.png')
        btn_update = tk.Button(
            toolbar,
            bg='#D7D8E0',
            bd=0,
            image=self.update_curr_img,
            command=self.update_current)
        btn_update.pack(anchor=tk.SE)


        current_num = tk.LabelFrame(
            toolbar,
            bg='#D7D8E0',
            bd=0,
            text='Current')
        current_num.pack(side=tk.RIGHT)
        
        self.current_n = tk.Label(current_num, width=10)
        self.current_n.pack()

        self.tree = ttk.Treeview(
            self,
            columns=('ID', 'description', 'costs', 'total'),
            height=17,
            show='headings')
        self.tree.column(
            'ID',
            width=30,
            anchor=tk.CENTER)
        self.tree.column(
            'description',
            width=419,
            anchor=tk.CENTER)
        self.tree.column(
            'costs',
            width=111,
            anchor=tk.CENTER)
        self.tree.column(
            'total',
            width=70,
            anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Name')
        self.tree.heading('costs', text='Incomes\\expenses')
        self.tree.heading('total', text='Total')

        self.tree.pack()


    def records(self, description, costs, total):
        self.db.incert_data(description, costs, total)
        self.view_records()

    def update_records(self, description, costs, total):
        self.db.c.execute(
            '''UPDATE finance SET 
            description=?,
            costs=?,
            total=? 
            WHERE ID=?''',
            (description, costs, total, self.tree.set(
                self.tree.selection()[0],
                '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute(
                '''DELETE FROM finance WHERE ID=?''',
                (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()

    def update_current(self):
        self.db.c.execute('''SELECT * FROM finance''')
        sum_list = []
        while True:
            row = self.db.c.fetchone()
            if row == None:
                break
            i = row[3]
            sum_list.append(i)
        self.current_n.config(text=sum(sum_list))
    
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Add income and expenses')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = ttk.Label(self, text="Names")
        label_description.place(x=50, y=50)
        label_select = ttk.Label(self, text="Incomes or expenses")
        label_select.place(x=50, y=80)
        label_sum = ttk.Label(self, text="Summ:")
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Income', u'Expence'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cansel = ttk.Button(
            self,
            text='Close',
            command=self.destroy)
        btn_cansel.place(x=300, y=170)

        self.btn_ok = ttk.Button(
            self,
            text='Enter')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind(
            '<Button-1>',
            lambda event: self.view.records(
                self.entry_description.get(),
                self.combobox.get(),
                self.entry_money.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Edit pos')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            '<Button-1>',
           lambda event: self.view.update_records(
                self.entry_description.get(),
                self.combobox.get(),
                self.entry_money.get()))
        
        self.btn_ok.destroy()

class DB:
    def __init__(self):
        self.conn = sql.connect('data\\finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (
            id integer primary key,
            description text,
            costs text,
            total real)''')
        self.conn.commit()

    def incert_data(self, description, costs, total):
        self.c.execute(
            '''INSERT INTO finance(description, costs, total) VALUES (?, ?, ?)''',
            (description, costs, total))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry("640x480+200+300")
    root.resizable(False, False)

    root.mainloop()
    