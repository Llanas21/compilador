from lexicon import Lexicon, InvalidIdentifierError
from semantics import (
    Semantics,
    DuplicatedSymbolError,
    TypeMismatchError,
    UndeclaredSymbolError,
)
from intermediate_code import IntermediateCode
from execution import Execution
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
        menu_file.add_command(
            label="Abrir", command=self.open_file, accelerator="Ctrl+O"
        )
        menu_file.add_command(
            label="Guardar", command=self.save_file, accelerator="Ctrl+S"
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Salir", command=self.master.quit, accelerator="Ctrl+Q"
        )

        menu_run = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ejecutar", menu=menu_run)
        menu_run.add_command(
            label="Ejecutar léxico", command=self.run_lexicon, accelerator="Ctrl+F1"
        )
        menu_run.add_command(
            label="Ejecutar semántica",
            command=self.run_semantics,
            accelerator="Ctrl+F2",
        )
        menu_run.add_command(
            label="Ejecutar código intermedio",
            command=self.run_intermediate_code,
            accelerator="Ctrl+F3",
        )
        menu_run.add_command(
            label="Ejecutar programa",
            command=self.run_execution,
            accelerator="Ctrl+F5",
        )

        self.master.bind_all("<Control-o>", lambda event: self.open_file())
        self.master.bind_all("<Control-s>", lambda event: self.save_file())
        self.master.bind_all("<Control-q>", lambda event: self.master.quit())
        self.master.bind_all("<Control-O>", lambda event: self.open_file())
        self.master.bind_all("<Control-S>", lambda event: self.save_file())
        self.master.bind_all("<Control-F1>", lambda event: self.run_lexicon())
        self.master.bind_all("<Control-F2>", lambda event: self.run_semantics())
        self.master.bind_all("<Control-F3>", lambda event: self.run_intermediate_code())
        self.master.bind_all("<Control-F5>", lambda event: self.run_execution())
        self.master.bind_all("<Control-Q>", lambda event: self.master.quit())

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

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                content = self.text_box.get(1.0, END)
                f.write(content)
            self.run_lexicon()
        else:
            messagebox.showwarning("Guardar", "No hay un archivo abierto para guardar.")

    def run_lexicon(self):
        try:
            if self.current_file:
                lexicon = Lexicon(file_path=self.current_file)
                lexicon.generateTokensTable(
                    r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\tokens_table.txt"
                )
            messagebox.showinfo("Éxito", "Análisis léxico completado sin errores")
        except InvalidIdentifierError as e:
            messagebox.showerror("Error Sintáctico", str(e))

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
        except UndeclaredSymbolError as e:
            messagebox.showerror("Error Semántico", str(e))

    def run_intermediate_code(self):
        intermediate_code = IntermediateCode(
            file_path=r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\tokens_table.txt"
        )
        intermediate_code.generate_vci()
        messagebox.showinfo("Éxito", "Código intermedio completado sin errores.")

    def run_execution(self):
        execution = Execution(
            file_path=r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\vci.txt"
        )
        execution.execute()
        messagebox.showinfo("Éxito", "Ejecución completada sin errores.")
