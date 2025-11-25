#!/usr/bin/env python3
# texor.py - recreación del boceto como editor simple con Tkinter

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def new_file():
    text_area.delete("1.0", tk.END)
    status.config(text="texor — archivo sin nombre")

def open_file():
    path = filedialog.askopenfilename(filetypes=[("All files","*.*")])
    if path:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", f.read())
            status.config(text=f"texor — {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def save_file():
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("Python","*.py"),("All files","*.*")])
    if path:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
            status.config(text=f"texor — {path}")
            messagebox.showinfo("texor", "Archivo guardado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("texor")
root.geometry("900x600")
root.minsize(700, 450)

# Top toolbar
top_frame = ttk.Frame(root, height=50)
top_frame.pack(side="top", fill="x")

btn_new = ttk.Button(top_frame, text="📄", width=3, command=new_file)
btn_open = ttk.Button(top_frame, text="📁", width=3, command=open_file)
btn_save = ttk.Button(top_frame, text="💾", width=3, command=save_file)
btn_cut = ttk.Button(top_frame, text="✂️", width=3, command=lambda: root.focus_get().event_generate("<<Cut>>"))
btn_copy = ttk.Button(top_frame, text="📋", width=3, command=lambda: root.focus_get().event_generate("<<Copy>>"))
btn_paste = ttk.Button(top_frame, text="📥", width=3, command=lambda: root.focus_get().event_generate("<<Paste>>"))

for w in (btn_new, btn_open, btn_save, btn_cut, btn_copy, btn_paste):
    w.pack(side="left", padx=3, pady=6)

# Main layout
main_frame = ttk.Frame(root)
main_frame.pack(side="top", fill="both", expand=True)

left_frame = ttk.Frame(main_frame, width=140)
left_frame.pack(side="left", fill="y", padx=(8,4), pady=8)
left_frame.pack_propagate(False)

center_frame = ttk.Frame(main_frame)
center_frame.pack(side="left", fill="both", expand=True, padx=4, pady=8)

right_frame = ttk.Frame(main_frame, width=80)
right_frame.pack(side="right", fill="y", padx=(4,8), pady=8)
right_frame.pack_propagate(False)

# Left: mock explorer
lbl_explorer = ttk.Label(left_frame, text="Explorador", anchor="w", font=("Segoe UI", 9, "bold"))
lbl_explorer.pack(fill="x", padx=4, pady=(4,2))

file_list = tk.Listbox(left_frame, height=20)
file_list.pack(fill="both", expand=True, padx=4, pady=2)
for it in ["main.py", "utils.py", "notes.txt", "readme.md"]:
    file_list.insert("end", it)

# Center: canvas con texto encima (para dibujar líneas verticales como en el boceto)
canvas = tk.Canvas(center_frame, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)
inner = ttk.Frame(canvas)
text_window = canvas.create_window((0,0), window=inner, anchor="nw")

text_area = tk.Text(inner, wrap="none", font=("Consolas", 12), undo=True, padx=6, pady=6)
text_area.pack(fill="both", expand=True)
text_area.insert("1.0", "texto de ejemplo\n\nAquí va el contenido del editor 'texor'.\nPuedes abrir/guardar archivos con la barra superior.\n")

def draw_grid(event=None):
    canvas.delete("gridline")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    canvas.create_rectangle(2,2,w-2,h-2, outline="#444", tags="gridline")
    x = 2 + 60
    while x < w-6:
        canvas.create_line(x, 6, x, h-6, dash=(3,5), tags="gridline")
        x += 60

canvas.bind("<Configure>", draw_grid)

# Scrollbars (as en editor)
v_scroll = ttk.Scrollbar(inner, orient="vertical", command=text_area.yview)
h_scroll = ttk.Scrollbar(inner, orient="horizontal", command=text_area.xview)
text_area.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
v_scroll.pack(side="right", fill="y")
h_scroll.pack(side="bottom", fill="x")

# Right vertical toolbar
right_top = ttk.Frame(right_frame)
right_top.pack(side="top", fill="x", pady=(4,8))
btn_py = ttk.Button(right_top, text=".py", width=6, command=lambda: text_area.insert("1.0", "# Archivo Python\n"))
btn_js = ttk.Button(right_top, text=".js", width=6, command=lambda: text_area.insert("1.0", "// Archivo JS\n"))
btn_py.pack(padx=8, pady=2)
btn_js.pack(padx=8, pady=2)

x_frame = ttk.Frame(right_frame)
x_frame.pack(side="top", fill="y", expand=True, pady=6)
for i in range(6):
    b = ttk.Button(x_frame, text="X", width=6, command=lambda i=i: messagebox.showinfo("texor", f"Botón X {i+1}"))
    b.pack(padx=8, pady=4)

# Shortcuts
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-n>", lambda e: new_file())

# Status bar
status = ttk.Label(root, text="texor — archivo sin nombre", anchor="w")
status.pack(side="bottom", fill="x")

root.mainloop()
