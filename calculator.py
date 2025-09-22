#import 2 library agar program semuanya berjalan
import tkinter as tk
import math

#class utama untuk seluruh program yang akan dijalankan menggunakan tkinter dan semua tombol ada di dalam
class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multipurpose Scientific Calculator")
        self.memory = 0
        self.history = []
        self.angle_mode = "RAD"  # or "DEG"

        self.create_widgets()

    def create_widgets(self):
        # dibawah ini adalah program untuk interfcae dari tkinter
        self.entry = tk.Entry(self.root, font="Arial 20", borderwidth=5, relief=tk.RIDGE, justify="right")
        self.entry.grid(row=0, column=0, columnspan=8, padx=10, pady=10, sticky="we")

        self.history_box = tk.Listbox(self.root, height=5, width=40)
        self.history_box.grid(row=1, column=0, columnspan=8, padx=10, pady=2, sticky="we")

        #variable button berisi tombol-tombol yang akan digunakan
        buttons = [
            "7", "8", "9", "/", "sin", "cos", "tan", "log",
            "4", "5", "6", "*", "asin", "acos", "atan", "ln",
            "1", "2", "3", "-", "sqrt", "exp", "x^y", "x!",
            "0", ".", "C", "+", "(", ")", "pi", "e",
            "M+", "M-", "MR", "MC", "DEG", "RAD", "Ans", "="
        ] #tombol yang akan digunakan pada tkinter

        row, col = 2, 0
        for btn_text in buttons:
            btn = tk.Button(self.root, text=btn_text, font="Arial 14", width=5, height=2) #tombol ynag diambil dari varriabel button
            btn.grid(row=row, column=col, padx=2, pady=2) #ukuran dan posisi tombol
            btn.bind("<Button-1>", self.on_click)
            col += 1
            if col > 7:
                col = 0
                row += 1

# fungsi di bawah akan memberi fungsi pada tombol, menggunakan library math
    def on_click(self, event):
        text = event.widget.cget("text")
        if text == "=":
            self.calculate()
        elif text == "C":
            self.entry.delete(0, tk.END)
        elif text == "Ans":
            if self.history:
                self.entry.insert(tk.END, str(self.history[-1][1]))
        elif text == "pi":
            self.entry.insert(tk.END, str(math.pi))
        elif text == "e":
            self.entry.insert(tk.END, str(math.e))
        elif text == "x^y":
            self.entry.insert(tk.END, "**")
        elif text == "x!":
            self.entry.insert(tk.END, "fact(")
        elif text in ["sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "sqrt", "exp"]:
            self.entry.insert(tk.END, f"{text}(")
        elif text == "M+":
            self.memory_add()
        elif text == "M-":
            self.memory_subtract()
        elif text == "MR":
            self.entry.insert(tk.END, str(self.memory))
        elif text == "MC":
            self.memory = 0
        elif text == "DEG":
            self.angle_mode = "DEG"
        elif text == "RAD":
            self.angle_mode = "RAD"
        else:
            self.entry.insert(tk.END, text)

#fungsi dibawah akan melakukan perhitungan setelah menginput angka dan persamaan
    def calculate(self):
        expr = self.entry.get()
        expr = expr.replace('^', '**')
        expr = expr.replace('ln', 'log')
        try:
            result = str(eval(expr, {"__builtins__": None}, self.safe_dict()))
            self.history.append((expr, result))
            self.update_history()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

#fungsi dibawah akan mengamankan perhitungan agar tidak ada error
    def safe_dict(self):
        d = math.__dict__.copy()
        d.update({
            "fact": math.factorial,
            "pi": math.pi,
            "e": math.e,
            "exp": math.exp,
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,
        })
        return d
#fungsi dibawah masih sama menggunakan library math untuk fungsi trigonometri
    def sin(self, x):
        return math.sin(math.radians(x)) if self.angle_mode == "DEG" else math.sin(x)
    def cos(self, x):
        return math.cos(math.radians(x)) if self.angle_mode == "DEG" else math.cos(x)
    def tan(self, x):
        return math.tan(math.radians(x)) if self.angle_mode == "DEG" else math.tan(x)
    def asin(self, x):
        return math.degrees(math.asin(x)) if self.angle_mode == "DEG" else math.asin(x)
    def acos(self, x):
        return math.degrees(math.acos(x)) if self.angle_mode == "DEG" else math.acos(x)
    def atan(self, x):
        return math.degrees(math.atan(x)) if self.angle_mode == "DEG" else math.atan(x)

#fungsi dibawah untuk memory add dan subtract
    def memory_add(self):
        try:
            self.memory += float(self.entry.get())
        except Exception:
            pass

    def memory_subtract(self):
        try:
            self.memory -= float(self.entry.get())
        except Exception:
            pass

    def update_history(self):
        self.history_box.delete(0, tk.END)
        for expr, result in self.history[-5:]:
            self.history_box.insert(tk.END, f"{expr} = {result}")

#memulai program
if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()