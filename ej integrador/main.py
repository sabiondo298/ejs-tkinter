import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("800x600")

        self.inventory = []
        self.data_file = "inventory.json"
        self.load_data()

        self.var_codigo = tk.StringVar()
        self.var_descripcion = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_cantidad = tk.IntVar()

        self.var_search = tk.StringVar()
        self.var_search.trace("w", self.on_search_change)

        self.create_widgets()

        self.refresh_table()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.entry_search = ttk.Entry(search_frame, textvariable=self.var_search)
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(content_frame, text="Panel de Operaciones", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Código:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_codigo = ttk.Entry(form_frame, textvariable=self.var_codigo)
        self.entry_codigo.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_descripcion = ttk.Entry(form_frame, textvariable=self.var_descripcion)
        self.entry_descripcion.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(form_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_precio = ttk.Entry(form_frame, textvariable=self.var_precio)
        self.entry_precio.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(form_frame, text="Categoría:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.entry_categoria = ttk.Entry(form_frame, textvariable=self.var_categoria)
        self.entry_categoria.grid(row=3, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(form_frame, text="Cantidad:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.spin_cantidad = ttk.Spinbox(form_frame, from_=0, to=10000, textvariable=self.var_cantidad)
        self.spin_cantidad.grid(row=4, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X)

        self.btn_guardar = ttk.Button(button_frame, text="Guardar", command=self.guardar)
        self.btn_guardar.pack(fill=tk.X, pady=2)

        self.btn_modificar = ttk.Button(button_frame, text="Modificar", command=self.modificar)
        self.btn_modificar.pack(fill=tk.X, pady=2)

        self.btn_borrar = ttk.Button(button_frame, text="Borrar", command=self.borrar)
        self.btn_borrar.pack(fill=tk.X, pady=2)

        right_frame = ttk.LabelFrame(content_frame, text="Inventario", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("codigo", "descripcion", "precio", "categoria", "cantidad")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

        self.tree.heading("codigo", text="Código", command=lambda: self.sort_by_column("codigo"))
        self.tree.heading("descripcion", text="Descripción", command=lambda: self.sort_by_column("descripcion"))
        self.tree.heading("precio", text="Precio", command=lambda: self.sort_by_column("precio"))
        self.tree.heading("categoria", text="Categoría", command=lambda: self.sort_by_column("categoria"))
        self.tree.heading("cantidad", text="Cantidad", command=lambda: self.sort_by_column("cantidad"))

        self.tree.column("codigo", width=100)
        self.tree.column("descripcion", width=200)
        self.tree.column("precio", width=80)
        self.tree.column("categoria", width=100)
        self.tree.column("cantidad", width=80)

        v_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        self.tree.tag_configure("low_stock", background="red")

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.inventory = json.load(f)
            except:
                self.inventory = []

    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.inventory, f, indent=4, ensure_ascii=False)
        except:
            messagebox.showerror("Error", "No se pudo guardar los datos")

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_data = data if data is not None else self.inventory

        for item in display_data:
            values = (item["codigo"], item["descripcion"], f"{item['precio']:.2f}", item["categoria"], item["cantidad"])
            tag = "low_stock" if item["cantidad"] < 10 else ""
            self.tree.insert("", tk.END, values=values, tags=(tag,))

    def guardar(self):
        codigo = self.var_codigo.get().strip()
        descripcion = self.var_descripcion.get().strip()
        precio_str = self.var_precio.get().strip()
        categoria = self.var_categoria.get().strip()
        cantidad = self.var_cantidad.get()

        if not all([codigo, descripcion, precio_str, categoria]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser un número")
            return

        if any(item["codigo"] == codigo for item in self.inventory):
            messagebox.showerror("Error", "El código ya existe")
            return

        new_item = {
            "codigo": codigo,
            "descripcion": descripcion,
            "precio": precio,
            "categoria": categoria,
            "cantidad": cantidad
        }
        self.inventory.append(new_item)
        self.save_data()
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Éxito", "Producto guardado")

    def modificar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Seleccione un producto o ingrese código")
            return

        for i, item in enumerate(self.inventory):
            if item["codigo"] == codigo:
                # Update
                descripcion = self.var_descripcion.get().strip()
                precio_str = self.var_precio.get().strip()
                categoria = self.var_categoria.get().strip()
                cantidad = self.var_cantidad.get()

                if not all([descripcion, precio_str, categoria]):
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return

                try:
                    precio = float(precio_str)
                except ValueError:
                    messagebox.showerror("Error", "Precio debe ser un número")
                    return

                self.inventory[i] = {
                    "codigo": codigo,
                    "descripcion": descripcion,
                    "precio": precio,
                    "categoria": categoria,
                    "cantidad": cantidad
                }
                self.save_data()
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Éxito", "Producto modificado")
                return

        messagebox.showerror("Error", "Producto no encontrado")

    def borrar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Seleccione un producto o ingrese código")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de borrar este producto?"):
            return

        for i, item in enumerate(self.inventory):
            if item["codigo"] == codigo:
                del self.inventory[i]
                self.save_data()
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Éxito", "Producto borrado")
                return

        messagebox.showerror("Error", "Producto no encontrado")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            self.var_codigo.set(values[0])
            self.var_descripcion.set(values[1])
            self.var_precio.set(values[2])
            self.var_categoria.set(values[3])
            self.var_cantidad.set(values[4])

    def clear_form(self):
        self.var_codigo.set("")
        self.var_descripcion.set("")
        self.var_precio.set("")
        self.var_categoria.set("")
        self.var_cantidad.set(0)

    def on_search_change(self, *args):
        search_term = self.var_search.get().lower()
        if search_term:
            filtered = [item for item in self.inventory if search_term in item["descripcion"].lower() or search_term in item["categoria"].lower()]
            self.refresh_table(filtered)
        else:
            self.refresh_table()

    def sort_by_column(self, col):
        if col == "codigo":
            self.inventory.sort(key=lambda x: x["codigo"])
        elif col == "descripcion":
            self.inventory.sort(key=lambda x: x["descripcion"])
        elif col == "precio":
            self.inventory.sort(key=lambda x: x["precio"])
        elif col == "categoria":
            self.inventory.sort(key=lambda x: x["categoria"])
        elif col == "cantidad":
            self.inventory.sort(key=lambda x: x["cantidad"])
        self.save_data()
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()