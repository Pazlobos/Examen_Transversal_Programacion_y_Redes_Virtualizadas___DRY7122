# item1.py
from tabulate import tabulate

def mostrar_integrantes():
    # Modifica estos datos con los nombres reales de tu grupo
    integrantes = [
        ["Nombre", "Apellido"],
        ["Maria Paz", "Lobos"],
        ["Tomas", "Sandretti"],
        ["Joahns","Coye"]

    ]
    print("\n=== INTEGRANTES DEL GRUPO ===")
    print(tabulate(integrantes, headers="firstrow", tablefmt="grid"))

def verificar_vlan():
    print("\n--- Verificador de Rango de VLAN ---")
    try:
        vlan = int(input("Ingrese el número de VLAN a verificar: "))
        if 1 <= vlan <= 1005:
            print(f"La VLAN {vlan} corresponde al RANGO NORMAL.")
        elif 1006 <= vlan <= 4094:
            print(f"La VLAN {vlan} corresponde al RANGO EXTENDIDO.")
        else:
            print(f"El número {vlan} no es una VLAN válida (Rango permitido: 1-4094).")
    except ValueError:
        print("Error: Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    mostrar_integrantes()
    verificar_vlan()