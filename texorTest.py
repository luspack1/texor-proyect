import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ------------------------------
# Funciones principales del editor
# ------------------------------
def new_file():
    text_area.delete("1.0", tk.END)
    status.config(text="Nuevo archivo")


def open_file():
    path = filedialog.askopenfilename(
        filetypes=[
            ("Archivos de texto", "*.txt *.py *.md *.json *.js"),
            ("Todos los archivos", "*.*")
        ]
    )
    if path:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", f.read())
            status.config(text=f"Abierto: {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def open_from_explorer(event):
    """Abrir archivo desde el panel izquierdo (explorador)"""
    try:
        selection = file_list.get(file_list.curselection())
        with open(selection, "r", encoding="utf-8", errors="ignore") as f:
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", f.read())
        status.config(text=f"Abierto: {selection}")
    except:
        pass


def save_file():
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Texto", "*.txt"), ("Python", "*.py"), ("Todos", "*.*")]
    )
    if path:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
            status.config(text=f"Guardado: {path}")
            messagebox.showinfo("texor", "Archivo guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ------------------------------
# UI principal
# ------------------------------
root = tk.Tk()
root.title("texor")
root.geometry("900x600")

# Barra de herramientas
toolbar = ttk.Frame(root)
toolbar.pack(side="top", fill="x")

ttk.Button(toolbar, text="Nuevo", width=10, command=new_file).pack(side="left", padx=3, pady=3)
ttk.Button(toolbar, text="Abrir", width=10, command=open_file).pack(side="left", padx=3, pady=3)
ttk.Button(toolbar, text="Guardar", width=10, command=save_file).pack(side="left", padx=3, pady=3)

# Marco principal
main = ttk.Frame(root)
main.pack(fill="both", expand=True)

# Explorador de archivos (izquierda)
explorer = ttk.Frame(main, width=150)
explorer.pack(side="left", fill="y")
explorer.pack_propagate(False)

ttk.Label(explorer, text="Explorador").pack(pady=5)

file_list = tk.Listbox(explorer)
file_list.pack(fill="both", expand=True, padx=5)
file_list.insert("end", "main.py")
file_list.insert("end", "config.py")
file_list.insert("end", "notes.txt")

file_list.bind("<Double-Button-1>", open_from_explorer)

# Área de texto (centro)
center = ttk.Frame(main)
center.pack(side="left", fill="both", expand=True)

text_area = tk.Text(center, wrap="none", font=("Consolas", 12))
text_area.pack(fill="both", expand=True)

text_area.insert("1.0", "texto de ejemplo\n\nBienvenido a TEXOR.")

# Barra de estado
status = ttk.Label(root, text="Listo", anchor="w")
status.pack(fill="x")


root.mainloop()
