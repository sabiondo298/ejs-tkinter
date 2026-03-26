import tkinter as tk
import math
from tkinter import ttk

root = tk.Tk()
root.title("Calculadora")
root.geometry("500x700")

pantalla = tk.StringVar()
entry = ttk.Entry(root, textvariable=pantalla, font=("Arial", 20))
entry.pack(fill="x", padx=10, pady=10)

def presionar(valor):
    pantalla.set(pantalla.get() + valor)

def limpiar():
    pantalla.set("")

def calcular():
    try:
        resultado = eval(pantalla.get())
        pantalla.set(resultado)
    except ZeroDivisionError:
        pantalla.set("Error: división por 0")
    except:
        pantalla.set("Error")

def raiz():
    try:
        valor = float(pantalla.get())
        resultado = math.sqrt(valor)
        pantalla.set(resultado)
    except:
        pantalla.set("Error")

frame = ttk.Frame(root)
frame.pack()

ttk.Button(frame, text="7", command=lambda: presionar("7")).grid(row=0, column=0)
ttk.Button(frame, text="8", command=lambda: presionar("8")).grid(row=0, column=1)
ttk.Button(frame, text="9", command=lambda: presionar("9")).grid(row=0, column=2)
ttk.Button(frame, text="/", command=lambda: presionar("/")).grid(row=0, column=3)

botones = [
    ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
    ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
    ("0", 3, 0), ("C", 3, 1), ("=", 3, 2), ("+", 3, 3),
]

for (texto, fila, col) in botones:
    if texto == "C":
        accion = limpiar
    elif texto == "=":
        accion = calcular
    else:
        accion = lambda t=texto: presionar(t)

    ttk.Button(frame, text=texto, command=accion)\
        .grid(row=fila, column=col, padx=5, pady=5)
    
ttk.Button(frame, text="^", command=lambda: presionar("**")).grid(row=4, column=0)
ttk.Button(frame, text="√", command=raiz).grid(row=4, column=1)
command=lambda: presionar("7")
root.mainloop()

