from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

# Ruta base de íconos (usa tu carpeta original IMG)
ICONO_PAPAS = "IMG/icono_papas_fritas_64x64.png"

def get_default_menus() -> List[IMenu]:
    return [

        # 🥩 Sandwich de Potito
        CrearMenu(
            "Sandwich de potito (Especialidad de la casa)",
            [
                Ingrediente("Intestino de vacuno", "unid", 0.5),
                Ingrediente("Pan de hamburguesa", "unid", 1),
                Ingrediente("Longaniza", "unid", 0.5),
                Ingrediente("Cebolla", "unid", 0.5),
            ],
            precio=2400,
            icono_path="IMG/icono_hamburguesa_simple_64x64.png",
        ),

        # 🌭 Completo
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa", "unid", 1),
                Ingrediente("Pan de completo", "unid", 1),
                Ingrediente("Palta", "unid", 1),
                Ingrediente("Tomate", "unid", 1),
            ],
            precio=1800,
            icono_path="IMG/icono_hotdog_sin_texto_64x64.png",
        ),

        # 🍔 Cangriburger Simple
        CrearMenu(
            "Cangriburger Simple",
            [
                Ingrediente("Carne de hamburguesa", "unid", 1),
                Ingrediente("Pan de hamburguesa", "unid", 1),
                Ingrediente("Lechuga", "unid", 1),
                Ingrediente("Tomate", "unid", 1),
                Ingrediente("Lamina de cheddar", "unid", 1),
            ],
            precio=2500,
            icono_path="IMG/icono_hamburguesa_simple_64x64.png",
        ),

        # 🍔 Cangriburger Doble
        CrearMenu(
            "Cangriburger Doble",
            [
                Ingrediente("Carne de hamburguesa", "unid", 2),
                Ingrediente("Pan de hamburguesa", "unid", 1),
                Ingrediente("Lechuga", "unid", 1),
                Ingrediente("Tomate", "unid", 1),
                Ingrediente("Lamina de cheddar", "unid", 2),
            ],
            precio=3500,
            icono_path="IMG/icono_hamburguesa_doble_64x64.png",        
        ),

        # 🍟 Papas fritas
        CrearMenu(
            "Papas fritas (chicas)",
            [
                Ingrediente("Papas", "unid", 2),
            ],
            precio=1000,
            icono_path=ICONO_PAPAS,        
        ),
        CrearMenu(
            "Papas fritas (medianas)",
            [
                Ingrediente("Papas", "unid", 4),
            ],
            precio=2000,
            icono_path=ICONO_PAPAS,        
        ),
        CrearMenu(
            "Papas fritas (grandes)",
            [
                Ingrediente("Papas", "unid", 6),
            ],
            precio=3000,
            icono_path=ICONO_PAPAS,        
        ),

        # 🍳 Chorrillanas
        CrearMenu(
            "Chorrillana simple",
            [
                Ingrediente("Carne de vacuno", "unid", 1),
                Ingrediente("Papas", "unid", 3),
                Ingrediente("Cebolla", "unid", 1),
                Ingrediente("Huevos", "unid", 2),
            ],
            precio=5000,
            icono_path="IMG/icono_chorrillana_64x64.png",
        ),
        CrearMenu(
            "Chorrillana XL",
            [
                Ingrediente("Carne de vacuno", "unid", 2),
                Ingrediente("Papas", "unid", 4),
                Ingrediente("Cebolla", "unid", 2),
                Ingrediente("Huevos", "unid", 2),
                Ingrediente("Chorizo", "unid", 1),
                Ingrediente("Vienesa", "unid", 1),
            ],
            precio=8000,
            icono_path="IMG/icono_chorrillana_64x64.png",
        ),

        # 🥗 Ensalada
        CrearMenu(
            "Ensalada mixta",
            [
                Ingrediente("Tomate", "unid", 1),
                Ingrediente("Lechuga", "unid", 1),
                Ingrediente("Cebolla", "unid", 0.5),
                Ingrediente("Huevos", "unid", 1),
            ],
            precio=1800,
            icono_path="IMG/icono_ensalada_64x64.png",
        ),

        # 🥟 Empanadas
        CrearMenu(
            "Empanada frita",
            [
                Ingrediente("Masa de empanada", "unid", 1),
                Ingrediente("Carne de vacuno", "unid", 0.5),
                Ingrediente("Cebolla", "unid", 0.5),
                Ingrediente("Huevos", "unid", 0.25),
            ],
            precio=1200,
            icono_path="IMG/icono_empanada_queso_64x64.png",
        ),
        CrearMenu(
            "Empanada de queso",
            [
                Ingrediente("Masa de empanada", "unid", 1),
                Ingrediente("Queso", "unid", 0.5),
            ],
            precio=1000,
            icono_path="IMG/icono_empanada_queso_64x64.png",
        ),

        # 🥤 Bebidas
        CrearMenu(
            "Coca-Cola",
            [
                Ingrediente("Coca cola","unid",1),
            ],
            precio=1100,
            icono_path="IMG/icono_cola_lata_64x64.png",
        ),
        CrearMenu(
            "Pepsi",
            [
                Ingrediente("Pepsi","unid",1),
            ],
            precio=1100,
            icono_path="IMG/icono_cola_64x64.png",
        ),
    ]
