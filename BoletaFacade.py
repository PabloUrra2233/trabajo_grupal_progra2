from fpdf import FPDF
from datetime import datetime
import os

class BoletaFacade:
    def __init__(self, pedido):
        self.pedido = pedido
        self.numero_boleta = None
        self.output_dir = "output/boletas"
        self.subtotal = 0
        self.iva = 0
        self.total = 0

    # --- FORMATEO CLP ---
    def _formato_clp(self, n):
        return f"${int(round(n)):,.0f}".replace(",", ".")

    # --- DETALLE DE LA BOLETA ---
    def generar_detalle_boleta(self):
        self.numero_boleta = f"BOL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.subtotal = self.pedido.calcular_total()
        self.iva = self.subtotal * 0.19
        self.total = self.subtotal + self.iva

    # --- CREACIÓN DEL PDF ---
    def crear_pdf(self):
        os.makedirs(self.output_dir, exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Boleta Restaurante", ln=True, align='L')

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, "Razón Social del Negocio", ln=True)
        pdf.cell(0, 8, "RUT: 12.345.678-9", ln=True)
        pdf.cell(0, 8, "Dirección: Calle Falsa 123", ln=True)
        pdf.cell(0, 8, f"N° Boleta: {self.numero_boleta}", ln=True)
        pdf.cell(0, 8, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='R')
        pdf.ln(4)

        # Tabla de productos
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(80, 8, "Nombre", border=1)
        pdf.cell(25, 8, "Cantidad", border=1, align='C')
        pdf.cell(40, 8, "Precio Unitario", border=1, align='R')
        pdf.cell(40, 8, "Subtotal", border=1, align='R')
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for item in self.pedido.menus:
            subtotal = item.precio * item.cantidad
            pdf.cell(80, 8, str(item.nombre), border=1)
            pdf.cell(25, 8, str(item.cantidad), border=1, align='C')
            pdf.cell(40, 8, self._formato_clp(item.precio), border=1, align='R')
            pdf.cell(40, 8, self._formato_clp(subtotal), border=1, align='R')
            pdf.ln()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(145, 8, "Subtotal:", 0, 0, 'R')
        pdf.cell(40, 8, self._formato_clp(self.subtotal), 0, 1, 'R')
        pdf.cell(145, 8, "IVA (19%):", 0, 0, 'R')
        pdf.cell(40, 8, self._formato_clp(self.iva), 0, 1, 'R')
        pdf.cell(145, 8, "Total:", 0, 0, 'R')
        pdf.cell(40, 8, self._formato_clp(self.total), 0, 1, 'R')

        pdf.ln(4)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 8, "Gracias por su compra.", 0, 1, 'C')

        pdf_filename = os.path.join(self.output_dir, f"{self.numero_boleta}.pdf")
        pdf.output(pdf_filename)
        return pdf_filename

    # --- GENERAR BOLETA COMPLETA ---
    def generar_boleta(self):
        if not hasattr(self.pedido, "menus") or not self.pedido.menus:
            raise ValueError("No hay ítems en el pedido para generar la boleta.")
        for it in self.pedido.menus:
            assert hasattr(it, "nombre") and hasattr(it, "precio") and hasattr(it, "cantidad"), \
                "Item inválido en pedido."
        self.generar_detalle_boleta()
        pdf_path = self.crear_pdf()
        return {
            "archivo": pdf_path,
            "numero": self.numero_boleta,
            "subtotal": self.subtotal,
            "iva": self.iva,
            "total": self.total
        }
