from lexicon import Lexicon
from semantics import Semantics, DuplicatedSymbolError, TypeMismatchError
import tkinter as tk
from tkinter import filedialog, Menu, Text, Scrollbar, messagebox, END


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lenguajes & Autómatas IDE")
        self.master.geometry("854x480")

        self.current_file = ""

        self.text_box = Text(master, wrap="word", font=("Consolas", 12))
        self.text_box.pack(expand=True, fill="both")

        self.scroll_bar = Scrollbar(self.text_box)
        self.scroll_bar.pack(side="right", fill="y")
        self.text_box.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.text_box.yview)

        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=menu_file)
        menu_file.add_command(label="Abrir", command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label="Salir", command=self.master.quit)

        menu_run = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ejecutar", menu=menu_run)
        menu_run.add_command(label="Ejecutar léxico", command=self.run_lexicon)
        menu_run.add_command(label="Ejecutar semántica", command=self.run_semantics)

    def open_file(self):
        file = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if file:
            self.current_file = file
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_box.delete(1.0, END)
                self.text_box.insert(END, content)

    def run_lexicon(self):
        if self.current_file:
            lexicon = Lexicon(file_path=self.current_file)
            lexicon.generateTokensTable(
                r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\tokens_table.txt"
            )

    def run_semantics(self):
        try:
            semantics = Semantics(
                file_path=r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\tokens_table.txt"
            )
            semantics.generate_dir_sym_tables(
                r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\\"
            )
            messagebox.showinfo("Éxito", "Análisis semántico completado sin errores.")
        except DuplicatedSymbolError as e:
            messagebox.showerror("Error Semántico", str(e))
        except TypeMismatchError as e:
            messagebox.showerror("Error Semántico", str(e))
