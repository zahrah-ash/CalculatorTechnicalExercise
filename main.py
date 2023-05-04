import tkinter as tk
import numpy as np

# Create the Calculator class that inherits from tk.Tk
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("300x500")

        # Create the menu, display, and buttons
        self.create_menu()
        self.create_display()
        self.create_buttons()

    # Create the menu bar
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create a drop-down menu with different categories
        categories = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=categories)
        categories.add_command(label="Matrix Operations", command=self.matrix_operations)
        categories.add_command(label="Unit Conversions", command=self.unit_conversions)
        categories.add_command(label="Programmatic Conversions", command=self.programmatic_conversions)

    # Create the display for the calculator
    def create_display(self):
        self.result_var = tk.StringVar()

        # Create an entry widget for displaying the result
        result_display = tk.Entry(self, textvariable=self.result_var, font=("Arial", 20), justify='right', bd=15)
        result_display.pack(fill=tk.X, padx=5, pady=5)

        # Create a history listbox to store calculation history
        self.history = []
        self.history_listbox = tk.Listbox(self, font=("Arial", 12), height=5)
        self.history_listbox.pack(fill=tk.X, padx=5, pady=5)

        # Recall and delete buttons for the history
        history_button_frame = tk.Frame(self)
        history_button_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(history_button_frame, text="Recall", font=("Arial", 14), command=self.recall_history).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(history_button_frame, text="Delete", font=("Arial", 14), command=self.delete_history).pack(side=tk.LEFT, padx=5, pady=5)


    # Create the calculator buttons
    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Define the buttons in a list of tuples
        buttons = [

            ('(',')', 'AC', 'ANS'),
            ('7','8','9','/'),
            ('4','5', '6', '*'),
            ('1','2','3','-'),
            ('0','.', '=','+')

        ]

        # AC and ANS buttons
        tk.Button(button_frame, text='AC', font=("Arial", 18), command=self.clear_entry).grid(row=0, column=2, sticky='news', padx=5, pady=5)
        tk.Button(button_frame, text='ANS', font=("Arial", 18), command=self.insert_last_result).grid(row=0, column=3, sticky='news', padx=5, pady=5)

        

# Create the buttons and assign their commands
        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                if button == '=':
                    tk.Button(button_frame, text=button, font=("Arial", 18), command=self.calculate).grid(row=i, column=j, sticky='news', padx=5, pady=5)
                elif button == 'AC':
                    tk.Button(button_frame, text=button, font=("Arial", 18), command=self.clear_entry).grid(row=i, column=j, sticky='news', padx=5, pady=5)
                elif button == 'ANS':
                    tk.Button(button_frame, text=button, font=("Arial", 18), command=self.insert_last_result).grid(row=i, column=j, sticky='news', padx=5, pady=5)
                else:
                    tk.Button(button_frame, text=button, font=("Arial", 18), command=lambda button=button: self.append_char(button)).grid(row=i, column=j, sticky='news', padx=5, pady=5)

        # Configure the row and column weights of the button frame
        button_frame.rowconfigure((0, 1, 2, 3), weight=1)
        button_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    def clear_entry(self):
        self.result_var.set("")

    def insert_last_result(self):
        current_text = self.result_var.get()
        self.result_var.set(current_text + 'ANS')

    # Append a character to the current result
    def append_char(self, char):
        current_text = self.result_var.get()
        self.result_var.set(current_text + char)

    # Calculate the result of the current expression
    def calculate(self):
        expression = self.result_var.get()

        if self.history and 'ANS' in expression:
            last_result = self.history[-1].split(" = ")[-1]
            expression = expression.replace('ANS', last_result)

        self.history.append(expression)

        try:
            result = eval(expression)
            self.result_var.set(result)
            self.history_listbox.insert(tk.END, f"{expression} = {result}")
        except Exception as e:
            self.result_var.set("Error")

    # Matrix operations functionality
    def matrix_operations(self):
        # Functions for adding, subtracting, and multiplying matrices
        def add_matrices():
            try:
                matrix1 = np.array(eval(matrix1_entry.get()))
                matrix2 = np.array(eval(matrix2_entry.get()))
                result = np.add(matrix1, matrix2)
                result_label.config(text=str(result))
            except Exception as e:
                result_label.config(text="Error")

        def subtract_matrices():
            try:
                matrix1 = np.array(eval(matrix1_entry.get()))
                matrix2 = np.array(eval(matrix2_entry.get()))
                result = np.subtract(matrix1, matrix2)
                result_label.config(text=str(result))
            except Exception as e:
                result_label.config(text="Error")

        def multiply_matrices():
            try:
                matrix1 = np.array(eval(matrix1_entry.get()))
                matrix2 = np.array(eval(matrix2_entry.get()))
                result = np.matmul(matrix1, matrix2)
                result_label.config(text=str(result))
            except Exception as e:
                result_label.config(text="Error")

        # Create a window for matrix operations
        matrix_window = tk.Toplevel(self)
        matrix_window.title("Matrix Operations")

        # Create entry widgets for matrix inputs
        matrix1_entry = tk.Entry(matrix_window, width=40, font=("Arial", 14))
        matrix1_entry.grid(row=0, column=0, columnspan=3)

        matrix2_entry = tk.Entry(matrix_window, width=40, font=("Arial", 14))
        matrix2_entry.grid(row=1, column=0, columnspan=3)

        # Create buttons for matrix operations
        tk.Button(matrix_window, text="Add", font=("Arial", 14), command=add_matrices).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(matrix_window, text="Subtract", font=("Arial", 14), command=subtract_matrices).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(matrix_window, text="Multiply", font=("Arial", 14), command=multiply_matrices).grid(row=2, column=2, padx=5, pady=5)

        # Create a label to display the result of matrix operations
        result_label = tk.Label(matrix_window, text="", font=("Arial", 14))
        result_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    # Recall button
    def recall_history(self):
        try:
            selected_index = self.history_listbox.curselection()[0]
            selected_calculation = self.history_listbox.get(selected_index)
            expression = selected_calculation.split(" = ")[0]
            self.result_var.set(expression)
        except IndexError:
            pass # Ignore if nothing is selected

    # Delete history button
    def delete_history(self):
        try:
            selected_index = self.history_listbox.curselection()[0]
            self.history_listbox.delete(selected_index)
            del self.history[selected_index]
        except IndexError:
            pass # Ignore if nothing is selected
    # Unit conversion functionality
    def unit_conversions(self):
        conversion_window = tk.Toplevel(self)
        conversion_window.title("Unit Conversions")

        # Define the conversion factors
        conversions = [
            ('Kilos', 'Stone', 0.157473),
            ('Gigabytes', 'Bytes', 1e9),
            ('Inches', 'Centimeters', 2.54),
            ('Days', 'Seconds', 86400)
        ]

        # Create the conversion widgets
        for i, (unit1, unit2, factor) in enumerate(conversions):
            tk.Label(conversion_window, text=f"{unit1} =", font=("Arial", 14)).grid(row=i, column=0)
            tk.Label(conversion_window, text=f"{unit2} =", font=("Arial", 14)).grid(row=i, column=2)

            entry1 = tk.Entry(conversion_window, width=10, font=("Arial", 14))
            entry1.grid(row=i, column=1)
            entry2 = tk.Entry(conversion_window, width=10, font=("Arial", 14))
            entry2.grid(row=i, column=3)

            entry1.bind("<FocusOut>", lambda event, entry1=entry1, entry2=entry2, factor=factor: self.convert_unit(event, entry1, entry2, factor))
            entry2.bind("<FocusOut>", lambda event, entry1=entry1, entry2=entry2, factor=factor: self.convert_unit(event, entry2, entry1, 1/factor))

           

    # Function to convert units
    def convert_unit(self, event, entry_from, entry_to, conversion_factor):
        try:
            value_from = float(entry_from.get())
            value_to = value_from * conversion_factor
            entry_to.delete(0, tk.END)
            entry_to.insert(0, str(value_to))
        except ValueError:
            pass  # Ignore invalid input

    # Programmatic conversion functionality
    def programmatic_conversions(self):
        def convert_programmatic():
            try:
                input_value = input_entry.get()
                input_base = int(input_base_var.get())
                output_base = int(output_base_var.get())

                # Convert input to decimal (base 10) first
                decimal_value = int(input_value, input_base)

                # Convert decimal to the desired output base
                if output_base == 2:
                    output_value = bin(decimal_value)[2:]
                elif output_base == 8:
                    output_value = oct(decimal_value)[2:]
                elif output_base == 10:
                    output_value = str(decimal_value)
                elif output_base == 16:
                    output_value = hex(decimal_value)[2:].upper()
                else:
                    raise ValueError("Invalid base")

                output_entry.delete(0, tk.END)
                output_entry.insert(0, output_value)
            except ValueError:
                output_entry.delete(0, tk.END)
                output_entry.insert(0, "Error")

        # Create a window for programmatic conversions
        conversion_window = tk.Toplevel(self)
        conversion_window.title("Programmatic Conversions")

        # Create input widgets
        tk.Label(conversion_window, text="Input:", font=("Arial", 14)).grid(row=0, column=0)
        input_entry = tk.Entry(conversion_window, width=10, font=("Arial", 14))
        input_entry.grid(row=0, column=1)

        input_base_var = tk.StringVar(conversion_window)
        input_base_var.set("10")
        input_base_options = {"Decimal": "10", "Binary": "2", "Octal": "8", "Hexadecimal": "16"}
        input_base_menu = tk.OptionMenu(conversion_window, input_base_var, *input_base_options.values())
        input_base_menu.config(font=("Arial", 14))
        input_base_menu.grid(row=0, column=2)

        # Create output widgets
        tk.Label(conversion_window, text="Output:", font=("Arial", 14)).grid(row=1, column=0)
        output_entry = tk.Entry(conversion_window, width=10, font=("Arial", 14))
        output_entry.grid(row=1, column=1)

        output_base_var = tk.StringVar(conversion_window)
        output_base_var.set("2")
        output_base_options = {"Binary": "2", "Octal": "8", "Decimal": "10", "Hexadecimal": "16"}
        output_base_menu = tk.OptionMenu(conversion_window, output_base_var, *output_base_options.values())
        output_base_menu.config(font=("Arial", 14))
        output_base_menu.grid(row=1, column=2)

        # Create convert button
        tk.Button(conversion_window, text="Convert", font=("Arial", 14), command=convert_programmatic).grid(row=2, column=1, pady=10)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

