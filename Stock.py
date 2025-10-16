from Ingrediente import Ingrediente

class Stock:
    """Clase que gestiona el inventario de ingredientes del restaurante."""

    def __init__(self):
        self.lista_ingredientes: list[Ingrediente] = []

    def agregar_ingrediente(self, ingrediente: Ingrediente) -> str:
        nombre_nuevo = ingrediente.nombre.strip().lower()
        for ing in self.lista_ingredientes:
            if ing.nombre.strip().lower() == nombre_nuevo:
                if ing.unidad != ingrediente.unidad:
                    # nombre igual pero unidad distinta -> no lo permitimos
                    raise ValueError(f"Ya existe '{ing.nombre}' con unidad '{ing.unidad}'.")
                # misma unidad -> sumar (acepta enteros negativos)
                ing.cantidad = int(ing.cantidad) + int(ingrediente.cantidad)
                return "actualizado"
        # no existía -> agregar
        self.lista_ingredientes.append(ingrediente)
        return "nuevo"


    def eliminar_ingrediente(self, nombre_ingrediente: str) -> None:
        """Elimina un ingrediente del stock por nombre."""
        self.lista_ingredientes = [
            ing for ing in self.lista_ingredientes if ing.nombre != nombre_ingrediente
        ]

    def verificar_stock(self) -> list[str]:
        """Devuelve una lista legible de los ingredientes disponibles."""
        return [str(ing) for ing in self.lista_ingredientes]

    def actualizar_stock(self, nombre_ingrediente: str, nueva_cantidad: float) -> bool:
        """Actualiza la cantidad de un ingrediente existente."""
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre_ingrediente:
                ing.cantidad = float(nueva_cantidad)
                return True
        return False

    def obtener_elementos_menu(self) -> list[str]:
        """Devuelve los nombres de los ingredientes actuales."""
        return [ing.nombre for ing in self.lista_ingredientes]

    # --- Métodos adicionales (para integrarse con Pedido y CrearMenu) --- #
    def disponible(self, nombre: str, cantidad: float) -> bool:
        """Verifica si hay suficiente cantidad de un ingrediente."""
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre and float(ing.cantidad) >= float(cantidad):
                return True
        return False

    def usar_ingredientes(self, usos: dict[str, float]) -> None:
        """
        Descuenta del stock los ingredientes usados en un pedido.
        Ejemplo: usos = {"Tomate": 0.2, "Pan": 1}
        """
        for nombre, cantidad in usos.items():
            for ing in self.lista_ingredientes:
                if ing.nombre == nombre:
                    ing.cantidad = max(0, float(ing.cantidad) - float(cantidad))
                    break