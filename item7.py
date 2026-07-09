from netmiko import ConnectHandler

# 1. Definir los parámetros de conexión al router CSR1000v
router_csr = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',  # Cambia por la IP real de tu router
    'username': 'developer',
    'password': 'C1sco12345',
    'secret': 'C1sco12345',    # Por si acaso
}

def ejecutar_examen_item7():
    print("Connecting to CSR1000v via Netmiko...")
    try:
        # Establecer la conexión SSH
        net_connect = netkey = ConnectHandler(**router_csr)
        net_connect.enable()
        
        # ---------------------------------------------------------
        # ▪ REQUISITO 1: Configurar EIGRP Nombrado (IPv4 e IPv6)
        # ---------------------------------------------------------
        print("\nConfiguring Named EIGRP (IPv4/IPv6)...")
        # Definimos los comandos de configuración global, familias de direcciones e interfaces pasivas
        config_commands = [
            'router eigrp EXAMEN_DUOC',
            ' address-family ipv4 autonomous-system 100',
            '  af-interface default',
            '   passive-interface',
            '  exit-address-family',
            ' address-family ipv6 autonomous-system 200',
            '  af-interface default',
            '   passive-interface',
            '  exit-address-family'
        ]
        
        # Enviamos el bloque de configuración
        net_connect.send_config_set(config_commands)
        
        # Validamos de inmediato mostrando la sección de EIGRP con show running-config
        print("\n=== VERIFICACION EIGRP NOMBRADO (show running-config | section eigrp) ===")
        check_eigrp = net_connect.send_command('show running-config | section eigrp')
        print(check_eigrp)
        
        # ---------------------------------------------------------
        # ▪ Obtener IP y estado de las interfaces
        # ---------------------------------------------------------
        print("\n=== REQUISITO 2: ESTADO E IP DE INTERFACES (show ip interface brief) ===")
        check_interfaces = net_connect.send_command('show ip interface brief')
        print(check_interfaces)
        
        # ---------------------------------------------------------
        # ▪ Obtener el running-config completo
        # ---------------------------------------------------------
        print("\n=== REQUISITO 3: RUNNING-CONFIG ===")
        running_config = net_connect.send_command('show running-config')
        # Imprimimos solo las primeras 30 líneas en consola para no saturar, pero se procesa completo
        print("\n".join(running_config.splitlines()[:30]))
        print("... [Configuración completa recibida con éxito] ...")
        
        # ---------------------------------------------------------
        # ▪ Obtener el show version
        # ---------------------------------------------------------
        print("\n=== REQUISITO 4: SHOW VERSION ===")
        show_version = net_connect.send_command('show version')
        # Imprimimos las líneas que muestran el modelo del router y la versión de IOS-XE
        print("\n".join(show_version.splitlines()[:15]))
        
        # Cerrar la conexión de forma segura
        net_connect.disconnect()
        print("\nProcess finished successfully. Connection closed.")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == '__main__':
    ejecutar_examen_item7()