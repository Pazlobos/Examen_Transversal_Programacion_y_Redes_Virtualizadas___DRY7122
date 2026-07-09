from ncclient import manager
import sys

# 1. DATOS DE CONEXIÓN AL ROUTER CSR1000v
ROUTER_IP = "192.168.56.101"  
ROUTER_PORT = 830             
USER = "developer"            
PASS = "C1sco12345"           

print("==========================================================")
print("  PASO 1: CONECTANDO AL ROUTER CSR1000v VÍA NETCONF...   ")
print("==========================================================")

# Estructura XML para cambiar el nombre del equipo
apellidos_grupo = "Lobos_Sandretti_Coye" 
xml_cambiar_nombre = f"""
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{apellidos_grupo}</hostname>
    </native>
</config>
"""

# Estructura XML para crear la interfaz Loopback 11
xml_crear_loopback = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>11</name>
                <ip>
                    <address>
                        <primary>
                            <address>11.11.11.11</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

try:
    # Conectarse al router--librería ncclient
    with manager.connect(
        host=ROUTER_IP,
        port=ROUTER_PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False
    ) as m:
        
        print("Conexion SSH NETCONF establecida con exito!")
        print("-" * 50)
        
        # Cambiar el nombre del router
        print(f"Enviando configuracion: Cambiando nombre del router a '{apellidos_grupo}'...")
        respuesta_nombre = m.edit_config(target='running', config=xml_cambiar_nombre)
        if "<ok/>" in str(respuesta_nombre):
            print("   ↳ Nombre modificado correctamente en el router!")
        
        print("-" * 50)
        
        # Crear Loopback 11
        print("Enviando configuracion: Creando interfaz Loopback 11 (IP 11.11.11.11)...")
        respuesta_loopback = m.edit_config(target='running', config=xml_crear_loopback)
        if "<ok/>" in str(respuesta_loopback):
            print("   ↳ Interfaz Loopback 11 configurada y encendida!")
            
        print("=" * 50)
        print("ITEM 4 COMPLETADO CON EXITO PARA LA REVISION!")
        print("==================================================")

except Exception as e:
    print(f"\nERROR DE CONEXION: No se pudo conectar al router en la IP {ROUTER_IP}.")
    print("Por favor, asegurate de que el router CSR1000v este encendido en VirtualBox.")
    print(f"Detalle tecnico del error: {e}")