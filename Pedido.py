# Pedido.py
from ElementoMenu import CrearMenu

class Pedido:
    def __init__(self):
        self.menus = []

    def agregar_menu(self, menu: CrearMenu):
        """
        Si el menú ya existe en el pedido, aumenta su cantidad.
        Si no existe, lo agrega como nuevo.
        """
        for item in self.menus:
            if item.nombre == menu.nombre:
                item.cantidad += 1
                return
        nuevo = CrearMenu(
            nombre=menu.nombre,
            ingredientes=menu.ingredientes,
            precio=menu.precio,
            icono_path=menu.icono_path,
            cantidad=1
        )
        self.menus.append(nuevo)

    def eliminar_menu(self, nombre_menu: str):
        """
        Elimina un menú por nombre. Si su cantidad > 1, solo resta 1.
        """
        for item in self.menus:
            if item.nombre == nombre_menu:
                if item.cantidad > 1:
                    item.cantidad -= 1
                else:
                    self.menus.remove(item)
                return

    def mostrar_pedido(self):
        """
        Devuelve una lista de menús (nombre, cantidad, precio, subtotal).
        """
        detalle = []
        for item in self.menus:
            subtotal = item.precio * item.cantidad
            detalle.append({
                "nombre": item.nombre,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio,
                "subtotal": subtotal
            })
        return detalle

    def calcular_total(self) -> float:
        """
        Calcula el total del pedido (sin IVA).
        """
        return sum(item.precio * item.cantidad for item in self.menus)

