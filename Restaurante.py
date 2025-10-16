from ElementoMenu import CrearMenu
import customtkinter as ctk
from tkinter import ttk, Toplevel, Label, messagebox
from Ingrediente import Ingrediente
from Stock import Stock
import re
from PIL import Image
from CTkMessagebox import CTkMessagebox
from Pedido import Pedido
from BoletaFacade import BoletaFacade
import pandas as pd
from tkinter import filedialog
from Menu_catalog import get_default_menus
from menu_pdf import create_menu_pdf
from ctk_pdf_viewer import CTkPDFViewer
import os
from tkinter.font import nametofont

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestión de ingredientes y pedidos")
        self.geometry("870x700")
        nametofont("TkHeadingFont").configure(size=14)
        nametofont("TkDefaultFont").configure(size=11)

        self.stock = Stock()
        self.menus_creados = set()
        self.pedido = Pedido()
        self.menus = get_default_menus()  

        self.tabview = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.crear_pestanas()

    def on_tab_change(self):
        selected_tab = self.tabview.get()
        if selected_tab == "Stock":
            self.actualizar_treeview()
        elif selected_tab == "Pedido":
            self.actualizar_treeview_pedido()
        elif selected_tab == "Carta restorante":
            self.actualizar_treeview()

    def crear_pestanas(self):
        self.tab3 = self.tabview.add("carga de ingredientes")  
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restorante")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_ver_boleta()

    # ===================== PESTAÑA 3 - CARGA CSV ===================== #
    def configurar_pestana3(self):
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV")
        label.pack(pady=20)
        boton_cargar_csv = ctk.CTkButton(self.tab3, text="Cargar CSV", fg_color="#1976D2", text_color="white", command=self.cargar_csv)
        boton_cargar_csv.pack(pady=10)

        self.frame_tabla_csv = ctk.CTkFrame(self.tab3)
        self.frame_tabla_csv.pack(fill="both", expand=True, padx=10, pady=10)
        self.df_csv = None   
        self.tabla_csv = None

        self.boton_agregar_stock = ctk.CTkButton(self.frame_tabla_csv, text="Agregar al Stock")
        self.boton_agregar_stock.pack(side="bottom", pady=10)

    # NO SE TOCA el sistema de carga de CSV (queda igual)
    def agregar_csv_al_stock(self):
        if self.df_csv is None:
            CTkMessagebox(title="Error", message="Primero debes cargar un archivo CSV.", icon="warning")
            return

        if 'nombre' not in self.df_csv.columns or 'cantidad' not in self.df_csv.columns:
            CTkMessagebox(title="Error", message="El CSV debe tener columnas 'nombre' y 'cantidad'.", icon="warning")
            return
        for _, row in self.df_csv.iterrows():
            nombre = str(row['nombre'])
            cantidad = str(row['cantidad'])
            unidad = str(row['unidad'])
            ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=cantidad)
            self.stock.agregar_ingrediente(ingrediente)
        CTkMessagebox(title="Stock Actualizado", message="Ingredientes agregados al stock correctamente.", icon="info")
        self.actualizar_treeview()   

    def cargar_csv(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona el CSV con los ingredientes",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return
        try:
            self.df_csv = pd.read_csv(file_path)
            self.mostrar_dataframe_en_tabla(self.df_csv)
            self.boton_agregar_stock.configure(command=self.agregar_csv_al_stock)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo cargar el archivo CSV.\n{e}", icon="warning")
        
    def mostrar_dataframe_en_tabla(self, df):
        if self.tabla_csv:
            self.tabla_csv.destroy()

        self.tabla_csv = ttk.Treeview(self.frame_tabla_csv, columns=list(df.columns), show="headings")
        for col in df.columns:
            self.tabla_csv.heading(col, text=col)
            self.tabla_csv.column(col, width=100, anchor="center")

        for _, row in df.iterrows():
            self.tabla_csv.insert("", "end", values=list(row))

        self.tabla_csv.pack(expand=True, fill="both", padx=10, pady=10)

    # ===================== STOCK ===================== #
    def configurar_pestana1(self):
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_unidad = ctk.CTkLabel(frame_formulario, text="Unidad:")
        label_unidad.pack(pady=5)
        self.combo_unidad = ctk.CTkComboBox(frame_formulario, values=["kg", "unid"])
        self.combo_unidad.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente", command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        self.tree = ttk.Treeview(self.tab1, columns=("Nombre", "Unidad", "Cantidad"), show="headings", height=25)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        self.boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", command=self.generar_menus)
        self.boton_generar_menu.pack(pady=10)

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get().strip()
        unidad = self.combo_unidad.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return

        ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=int(cantidad))

        try:
            estado = self.stock.agregar_ingrediente(ingrediente)
            self.actualizar_treeview()
            if estado == "nuevo":
                CTkMessagebox(title="Nuevo ingrediente", message=f"Se agregó '{nombre}' al stock.", icon="info")
            else:
                CTkMessagebox(title="Stock actualizado", message=f"Se ajustó la cantidad de '{nombre}'.", icon="info")
        except ValueError as e:
            CTkMessagebox(title="Unidad incompatible", message=str(e), icon="warning")

        self.entry_nombre.delete(0, "end")
        self.entry_cantidad.delete(0, "end")


    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Atención", message="Selecciona un ingrediente para eliminar.", icon="warning")
            return

        for item in seleccion:
            nombre = self.tree.item(item, "values")[0]
            self.stock.eliminar_ingrediente(nombre)

        self.actualizar_treeview()
        CTkMessagebox(title="Eliminado", message="Ingrediente eliminado correctamente.", icon="info")

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for ingrediente in self.stock.lista_ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.unidad, ingrediente.cantidad))

    # ===================== PEDIDO ===================== #
    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_intermedio = ctk.CTkFrame(self.tab2)
        frame_intermedio.pack(side="top", fill="x", padx=10, pady=5)

        global tarjetas_frame
        tarjetas_frame = ctk.CTkScrollableFrame(frame_superior)
        tarjetas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(frame_intermedio, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(side="right", padx=10)

        self.label_total = ctk.CTkLabel(frame_intermedio, text="Total: $0.00", anchor="e", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio Unitario"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_boleta = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=self.generar_boleta)
        self.boton_generar_boleta.pack(side="bottom", pady=10)

    def generar_menus(self):
        for widget in tarjetas_frame.winfo_children():
            widget.destroy()

        for menu in self.menus:
            frame_menu = ctk.CTkFrame(tarjetas_frame)
            frame_menu.pack(padx=10, pady=5, fill="x")

            if menu.icono_path and os.path.exists(menu.icono_path):
                img = ctk.CTkImage(Image.open(menu.icono_path), size=(64, 64))
                label_img = ctk.CTkLabel(frame_menu, image=img, text="")
                label_img.image = img
                label_img.pack(side="left", padx=10)

            info = ctk.CTkLabel(frame_menu, text=f"{menu.nombre}\n${menu.precio:,.0f}".replace(",", "."))
            info.pack(side="left", padx=10)

            boton_agregar = ctk.CTkButton(frame_menu, text="Agregar", command=lambda m=menu: self.agregar_a_pedido(m))
            boton_agregar.pack(side="right", padx=10)

    def agregar_a_pedido(self, menu):
        self.pedido.agregar_menu(menu)
        self.actualizar_treeview_pedido()
    
    def actualizar_treeview_pedido(self):
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)
        for item in self.pedido.mostrar_pedido():
            self.treeview_menu.insert("", "end", values=(item["nombre"], item["cantidad"], f"${item['precio_unitario']:,.0f}".replace(",", ".")))
        self.label_total.configure(text=f"Total: ${self.pedido.calcular_total():,.0f}".replace(",", "."))

    def eliminar_menu(self):
        seleccion = self.treeview_menu.selection()
        if not seleccion:
            CTkMessagebox(title="Atención", message="Selecciona un menú para eliminar.", icon="warning")
            return
        for item in seleccion:
            nombre = self.treeview_menu.item(item, "values")[0]
            self.pedido.menus = [m for m in self.pedido.menus if m.nombre != nombre]
        self.actualizar_treeview_pedido()
        CTkMessagebox(title="Menú eliminado", message="El menú fue eliminado del pedido.", icon="info")

    def actualizar_treeview_pedido(self):
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)
        for menu in self.pedido.menus:
            self.treeview_menu.insert("", "end", values=(menu.nombre, menu.cantidad, f"${menu.precio:.2f}"))

    def generar_boleta(self):
        if not self.pedido.menus:
            CTkMessagebox(title="Error", message="No hay menús en el pedido.", icon="warning")
            return
        boleta = BoletaFacade(self.pedido)
        ruta = boleta.generar_boleta()
        CTkMessagebox(title="Boleta generada", message=ruta, icon="info")

    # ===================== CARTA Y BOLETA PDF ===================== #
    def _configurar_pestana_crear_menu(self):
        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        boton_menu = ctk.CTkButton(contenedor, text="Generar Carta (PDF)", command=self.generar_y_mostrar_carta_pdf)
        boton_menu.pack(pady=10)

        self.pdf_frame_carta = ctk.CTkFrame(contenedor)
        self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_carta = None

    def generar_y_mostrar_carta_pdf(self):
        try:
            pdf_path = "carta.pdf"
            create_menu_pdf(self.menus, pdf_path, titulo_negocio="Restaurante", subtitulo="Carta Primavera 2025", moneda="$")
            if self.pdf_viewer_carta is not None:
                self.pdf_viewer_carta.pack_forget()
                self.pdf_viewer_carta.destroy()
            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_carta = CTkPDFViewer(self.pdf_frame_carta, file=abs_pdf)
            self.pdf_viewer_carta.pack(expand=True, fill="both")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar/mostrar la carta.\n{e}", icon="warning")

    def _configurar_pestana_ver_boleta(self):
        contenedor = ctk.CTkFrame(self.tab5)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)
    
        boton_boleta = ctk.CTkButton(contenedor, text="Mostrar Boleta (PDF)", command=self.mostrar_boleta)
        boton_boleta.pack(pady=10)
    
        self.pdf_frame_boleta = ctk.CTkFrame(contenedor)
        self.pdf_frame_boleta.pack(expand=True, fill="both", padx=10, pady=10)
    
        self.pdf_viewer_boleta = None

    def mostrar_boleta(self):
        pdf_path = "boleta.pdf"
        if not os.path.exists(pdf_path):
            CTkMessagebox(title="Error", message="Primero genera una boleta antes de mostrarla.", icon="warning")
            return
        if self.pdf_viewer_boleta is not None:
            self.pdf_viewer_boleta.pack_forget()
            self.pdf_viewer_boleta.destroy()
        abs_pdf = os.path.abspath(pdf_path)
        self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
        self.pdf_viewer_boleta.pack(expand=True, fill="both")

    # ===================== VALIDACIONES ===================== #
    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad):
        try:
            valor = int(cantidad)
            return True
        except ValueError:
            CTkMessagebox(
                title="Error de Validación",
                message="La cantidad debe ser un número entero (positivo o negativo).",
                icon="warning"
            )
            return False



if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  
    ctk.set_default_color_theme("blue") 
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = AplicacionConPestanas()

    try:
        style = ttk.Style(app)   
        style.theme_use("clam")
    except Exception:
        pass

    app.mainloop()