# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

Icono_Papas = "IMG/icono_papas_fritas_64x64.png"

def get_default_menus() -> List[IMenu]:
    return [
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
        CrearMenu(
            "Cangriburger Simple",
            [
                Ingrediente("Carne de hamburguesa", "unid", 1),
                Ingrediente("Pan de hamburguesa", "unid", 1),
                Ingrediente("lechuga", "unidad", 0.5),
                Ingrediente("Tomate", "unidad", 0.5),
                Ingrediente("Lamina de queso", "unid", 1),
            ],
            precio=2500,
            icono_path="IMG/icono_hamburguesa_simple_64x64.png",
        ),

        CrearMenu(
            "Cangriburger Doble",
            [
                Ingrediente("Carne de hamburguesa", "unid", 2),
                Ingrediente("Pan de hamburguesa", "unid", 1),
                Ingrediente("lechuga", "unidad", 1),
                Ingrediente("Tomate", "unidad", 1),
                Ingrediente("Lamina de queso", "unid", 2),
            ],
            precio=3500,
            icono_path="IMG/icono_hamburguesa_doble_64x64.png",        
        ),

        CrearMenu(
            "Papas fritas (chicas)",
            [
                Ingrediente("Papa", "unid", 2),

            ],
            precio=1000,
            icono_path= Icono_Papas,        
        ),

        CrearMenu(
            "Papas fritas (medianas)",
            [
                Ingrediente("Papa", "unid", 4),

            ],
            precio=2000,
            icono_path=Icono_Papas,        
        ),

        CrearMenu(
            "Papas fritas (grandes)",
            [
                Ingrediente("Papa", "unid", 6),

            ],
            precio=3000,
            icono_path=Icono_Papas,        
        ),
    ]