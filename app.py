import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re
from countries import *


class CurrencyConverter:
    """A calculator to convert currencies."""
    def __init__(self, source):
        self.data = requests.get(source).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

        # rounding the result
        amount = round(amount * self.currencies[to_currency], 2)
        return amount


class App(tk.Tk):
    """A class to run the app using Tkinter"""
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.converter = converter
        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # app dimensions
        self.geometry("400x700")

        # initializing frames to a dict
        self.frames = {}

        # moving between pages of the app using a for loop
        for page in (Convert, Graph):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Convert)    # default page

    # to show the current frame
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class Convert(tk.Frame):
    """A class for the Convert page with buttons for its functions and to go Graph page."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # creating and placing converter button
        button1 = ttk.Button(self, text="Converter")
        button1.place(x=130, y=70)

        # creating and placing graph button
        button2 = ttk.Button(self, text="Graph", command=lambda: controller.show_frame(Graph))
        button2.place(x=210, y=70)

        # to function the converter
        self.converter = converter

        # Page intro
        self.intro_box = Label(self, text=' CURRENCY CONVERTER', fg='black')
        self.intro_box.config(font=('Cambria', 25, 'bold', 'italic'))
        self.intro_box.place(relx=0.5, rely=0.05, anchor=CENTER)

        # Currency entry boxes
        valid = (self.register(self.validator), '%d', '%P')     # to validate numbers entered
        self.amount_field = Entry(self, bd=3, bg='turquoise1', relief=tk.SUNKEN, font='Cambria', justify=tk.RIGHT,
                                  width=15, validate='key', validatecommand=valid)
        self.converted_amount_field = Label(self, text='', fg='black', bg='sienna1', relief=tk.SUNKEN,
                                            font='Cambria', width=15, borderwidth=3, anchor='e')
        # from and to amount description
        self.from_amount_text = Label(self, text=' Original', fg='black')
        self.from_amount_text.config(font=('Cambria', 10, 'bold', 'italic'))
        self.from_amount_text.place(x=210, y=130)
        self.to_amount_text = Label(self, text=' Converted', fg='black')
        self.to_amount_text.config(font=('Cambria', 10, 'bold', 'italic'))
        self.to_amount_text.place(x=210, y=180)

        # dropdowns
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("CAD")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("GBP")  # default value
        font = ("Cambria", 12, "bold")
        self.option_add('*TCombobox*Listbox.background', 'aquamarine')
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.converter.currencies.keys()), font=font,
                                                   state='readonly', width=10, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.converter.currencies.keys()), font=font,
                                                 state='readonly', width=10, justify=tk.CENTER)
        # placing
        self.from_currency_dropdown.place(x=60, y=150)
        self.amount_field.place(x=210, y=150)
        self.to_currency_dropdown.place(x=60, y=200)
        self.converted_amount_field.place(x=210, y=200)

        # Convert button
        self.convert_button = Button(self, text="Convert", fg="black", command=self.execute)
        self.convert_button.config(font=('Cambria', 12, 'bold'))
        self.convert_button.place(relx=0.5, y=255, anchor=CENTER)

        # Currency lookup feature
        self.look_up = Label(self, text='Look up currency by country name', fg='black')
        self.look_up.config(font=('Cambria', 9, 'bold', 'italic'), fg='red')
        self.look_up.place(x=60, y=280)

        def update(data):
            curr_list.delete(0, END)
            for country in data:
                curr_list.insert(END, country)

        # Update entry box with listbox clicked

        def fillout(event):
            # delete what's in the search box
            search_box.delete(0, END)
            # add clicked list item to entry box
            search_box.insert(0, curr_list.get(ANCHOR))
        # function to check entry vs listbox

        def check(event):
            typed = search_box.get()
            if typed == '':
                data = countries
            else:
                data = []
                for country in countries:
                    if typed.lower() in country.lower():
                        data.append(country)
            # update listbox with selected country
            update(data)

        # Search box
        search_box = Entry(self, font=('Cambria', 12), width=33)
        search_box.place(x=60, y=300)

        # List box
        curr_list = Listbox(self, width=50)
        curr_list.place(x=60, y=330)

        update(countries)
        # create binding on listbox onclick
        curr_list.bind("<<ListboxSelect>>", fillout)
        search_box.bind("<KeyRelease>", check)

    def execute(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()
        converted_amount = round(self.converter.convert(from_curr, to_curr, amount),2)
        converted_amount = "{:,}".format(converted_amount)
        self.converted_amount_field.config(text=str(converted_amount), justify=tk.RIGHT)

    def validator(self, action, string):
        # validate that input is only numbers
        regex = re.compile(r"\d*?(\.)?\d,*$")
        result = regex.match(string)
        return string == "" or (string.count('.') <= 1 and result is not None)


class Graph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # creating and placing converter button
        button1 = ttk.Button(self, text="Converter",
                             command=lambda: controller.show_frame(Convert))
        button1.place(x=130, y=70)
        # creating and placing non-working graph button
        button2 = ttk.Button(self, text="Graph",)
        button2.place(x=210, y=70)
        # for converter to work
        self.converter = converter

        # Page intro
        self.intro_box = Label(self, text=' GRAPH GENERATOR', fg='black')
        self.intro_box.config(font=('Cambria', 25, 'bold', 'italic'))
        self.intro_box.place(relx=0.5, rely=0.05, anchor=CENTER)

        # from and to date
        self.from_date_text = Label(self, text=' From date (YYYY-MM-DD)', fg='black')
        self.from_date_text.config(font=('Cambria', 9, 'bold', 'italic'))
        self.from_date_text.place(x=210, y=130)
        self.to_date_text = Label(self, text=' To date (YYYY-MM-DD)', fg='black')
        self.to_date_text.config(font=('Cambria', 9, 'bold', 'italic'))
        self.to_date_text.place(x=210, y=180)

        # Date Entry box
        self.from_date = Entry(self, bd=3, bg='turquoise1', relief=tk.SUNKEN, font='Cambria', justify=tk.CENTER,
                               width=17, validate='key')
        self.to_date = Entry(self, bd=3, bg='sienna1', relief=tk.SUNKEN, font='Cambria', justify=tk.CENTER,
                             width=17, validate='key')

        # dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("CAD")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("GBP")  # default value

        font = ("Cambria", 12, "bold")
        self.option_add('*TCombobox*Listbox.background', 'indian red')
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.converter.currencies.keys()), font=font,
                                                   state='readonly', width=10, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.converter.currencies.keys()), font=font,
                                                 state='readonly', width=10, justify=tk.CENTER)
        # placing
        self.from_currency_dropdown.place(x=40, y=150)
        self.from_date.place(x=210, y=150)
        self.to_currency_dropdown.place(x=40, y=200)
        self.to_date.place(x=210, y=200)

        # Graph generate button
        self.generate_button = Button(self, text="Generate Graph", fg="black")
        self.generate_button.config(font=('Cambria', 12, 'bold'))
        self.generate_button.place(relx=0.5, rely=0.4, anchor=CENTER)


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)
    App()
    mainloop()

