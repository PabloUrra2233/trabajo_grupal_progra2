from ElementoMenu import CrearMenu

class Pedido:
    """Representa un pedido compuesto por varios menús."""

    def __init__(self) -> None:
        """Inicializa un pedido vacío."""
        self._menus: list[CrearMenu] = []

    def agregar_menu(self, menu: CrearMenu) -> bool:
        """
        Agrega un menú al pedido si no existe previamente.
        Retorna True si se agregó correctamente, False si ya existía.
        """
        if any(m.nombre.lower() == menu.nombre.lower() for m in self._menus):
            return False
        self._menus.append(menu)
        return True

    def eliminar_menu(self, nombre_menu: str) -> bool:
        """
        Elimina un menú del pedido por nombre.
        Retorna True si se eliminó, False si no se encontró.
        """
        for m in self._menus:
            if m.nombre.lower() == nombre_menu.lower():
                self._menus.remove(m)
                return True
        return False

    def obtener_pedido(self) -> list[CrearMenu]:
        """
        Retorna una lista con todos los menús del pedido actual.
        No modifica el estado interno.
        """
        return list(self._menus)  # se devuelve una copia para evitar mutación externa

    def calcular_total(self) -> float:
        """Calcula y retorna el total del pedido."""
        return sum(menu.precio for menu in self._menus)

    def esta_vacio(self) -> bool:
        """Indica si el pedido no contiene menús."""
        return len(self._menus) == 0

    def __str__(self) -> str:
        """Devuelve una representación legible del pedido."""
        if not self._menus:
            return "El pedido está vacío."
        lineas = [f"Pedido actual ({len(self._menus)} ítems):"]
        lineas.extend(f"- {menu.nombre} (${menu.precio:.2f})" for menu in self._menus)
        lineas.append(f"Total: ${self.calcular_total():.2f}")
        return "\n".join(lineas)
