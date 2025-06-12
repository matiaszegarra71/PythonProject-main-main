#!/usr/bin/env python3
"""
🐛 Ejemplos de Debugging en Python para TennisManager
Equivalente a byebug en Ruby on Rails
"""

# Importaciones para debugging
import pdb      # Python Debugger nativo
import ipdb     # IPython Debugger (mejorado)
import sys

def ejemplo_pdb():
    """Ejemplo usando pdb (Python Debugger nativo)"""
    print("🔍 Ejemplo con pdb")
    variable = "Hola desde pdb"

    # Equivalente a byebug en Ruby
    pdb.set_trace()  # ⬅️ BREAKPOINT AQUÍ

    print(f"Variable: {variable}")
    return variable

def ejemplo_ipdb():
    """Ejemplo usando ipdb (IPython Debugger - RECOMENDADO)"""
    print("🔍 Ejemplo con ipdb (mejor interfaz)")
    datos = {
        'usuario': 'eidan',
        'rol': 'admin',
        'notas': ['nota1', 'nota2']
    }

    # Mejor que pdb, con colores y autocompletado
    ipdb.set_trace()  # ⬅️ BREAKPOINT AQUÍ

    print(f"Datos: {datos}")
    return datos

def ejemplo_breakpoint():
    """Ejemplo usando breakpoint() - Python 3.7+ (MODERNO)"""
    print("🔍 Ejemplo con breakpoint() - Python 3.7+")
    lista_usuarios = ['admin', 'manager1', 'eidan']

    # Forma moderna y oficial (Python 3.7+)
    breakpoint()  # ⬅️ BREAKPOINT AQUÍ

    for usuario in lista_usuarios:
        print(f"Procesando usuario: {usuario}")

    return lista_usuarios

def ejemplo_condicional():
    """Ejemplo de debugging condicional"""
    print("🔍 Ejemplo de debugging condicional")

    for i in range(10):
        # Solo debuggear cuando i == 5
        if i == 5:
            ipdb.set_trace()  # ⬅️ BREAKPOINT CONDICIONAL

        print(f"Iteración: {i}")

def ejemplo_en_excepcion():
    """Ejemplo de debugging en excepciones"""
    print("🔍 Ejemplo de debugging en excepciones")

    try:
        resultado = 10 / 0  # Esto causará una excepción
    except ZeroDivisionError as e:
        print(f"Error capturado: {e}")
        # Debuggear cuando hay una excepción
        ipdb.set_trace()  # ⬅️ BREAKPOINT EN EXCEPCIÓN
        print("Continuando después del error...")

# Función para debugging post-mortem
def ejemplo_post_mortem():
    """Ejemplo de debugging post-mortem"""
    print("🔍 Ejemplo de debugging post-mortem")

    try:
        # Código que puede fallar
        datos = {'usuario': 'test'}
        print(datos['clave_inexistente'])  # KeyError
    except Exception:
        # Debugging post-mortem (después del error)
        import traceback
        traceback.print_exc()
        ipdb.post_mortem()  # ⬅️ DEBUGGING POST-MORTEM

if __name__ == "__main__":
    print("🎾 TennisManager - Ejemplos de Debugging")
    print("=" * 50)

    # Descomenta la función que quieras probar:

    # ejemplo_pdb()
    # ejemplo_ipdb()
    # ejemplo_breakpoint()
    # ejemplo_condicional()
    # ejemplo_en_excepcion()
    # ejemplo_post_mortem()

    print("\n💡 Para usar debugging:")
    print("1. Descomenta una función arriba")
    print("2. Ejecuta: python debug_example.py")
    print("3. O desde Docker: docker-compose exec web python debug_example.py")
