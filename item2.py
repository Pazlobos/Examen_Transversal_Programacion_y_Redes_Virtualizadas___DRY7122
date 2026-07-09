# item2.py
import requests

def obtener_coordenadas(ciudad):
    """Obtiene la latitud y longitud de una ciudad usando el geocodificador libre de OpenStreetMap."""
    url = f"https://nominatim.openstreetmap.org/search?q={ciudad}&format=json&limit=1"
    headers = {'User-Agent': 'ExamenTransversal_DRY7122_App'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return float(data['lat']), float(data['lon']), data['display_name']
    return None

def calcular_ruta(lat_origen, lon_origen, lat_destino, lon_destino, perfil):
    """Calcula la distancia, duración e indicaciones detalladas usando el motor OSRM de OpenStreetMap."""
    # steps=true obliga a la API a devolver la narrativa detallada de cada calle
    url = f"http://router.project-osrm.org/route/v1/{perfil}/{lon_origen},{lat_origen};{lon_destino},{lat_destino}?overview=false&steps=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return None

def traducir_maniobra(tipo, modificador):
    """Traduce las maniobras técnicas en inglés de la API a un español fluido."""
    traducciones = {
        "turn-right": "Gira a la derecha",
        "turn-left": "Gira a la izquierda",
        "turn-slight right": "Gira levemente a la derecha",
        "turn-slight left": "Gira levemente a la izquierda",
        "turn-sharp right": "Gira bruscamente a la derecha",
        "turn-sharp left": "Gira bruscamente a la izquierda",
        "merge-left": "Incorpórate a la izquierda",
        "merge-right": "Incorpórate a la derecha",
        "depart": "Sal de la ubicación inicial",
        "arrive": "Llegada al destino",
        "fork-right": "Toma la bifurcación a la derecha",
        "fork-left": "Toma la bifurcación a la izquierda",
        "roundabout": "En la rotonda toma la salida",
        "continue": "Continúa recto"
    }
    llave = f"{tipo}-{modificador}" if modificador else tipo
    return traducciones.get(llave, traducciones.get(tipo, "Continúa"))

def main():
    print("====================================================")
    print(" Sistema de Medición de Viajes (OpenStreetMap API) ")
    print("====================================================")
    
    while True:
        origen = input("\nCiudad de Origen en Chile (o 's' para salir): ").strip()
        if origen.lower() == 's': break
            
        destino = input("Ciudad de Destino en Argentina (o 's' para salir): ").strip()
        if destino.lower() == 's': break

        print("\nSeleccione el medio de transporte:")
        print("1. Automóvil")
        print("2. Bicicleta")
        print("3. Caminando")
        opcion = input("Opción (1-3): ").strip()
        
        perfiles = {"1": "driving", "2": "bicycle", "3": "foot"}
        transportes = {"1": "Automóvil", "2": "Bicicleta", "3": "A pie"}
        
        perfil = perfiles.get(opcion, "driving")
        medio = transportes.get(opcion, "Automóvil")

        print(f"\nBuscando coordenadas en vivo para {origen} y {destino}...")
        coord_origen = obtener_coordenadas(f"{origen}, Chile")
        coord_destino = obtener_coordenadas(f"{destino}, Argentina")

        if not coord_origen or not coord_destino:
            print("❌ No se pudieron encontrar las ubicaciones en OpenStreetMap. Intente nuevamente.")
            continue

        lat_o, lon_o, name_o = coord_origen
        lat_d, lon_d, name_d = coord_destino

        print(f"\n📍 Desde: {name_o}")
        print(f"📍 Hasta: {name_d}")

        # Realizar la consulta de ruta real a la API
        ruta_data = calcular_ruta(lat_o, lon_o, lat_d, lon_d, perfil)

        if ruta_data and "routes" in ruta_data and len(ruta_data["routes"]) > 0:
            ruta = ruta_data["routes"][0]
            
            distancia_metros = ruta["distance"]
            duracion_segundos = ruta["duration"]

            # Conversiones matemáticas requeridas en la rúbrica
            km = distancia_metros / 1000
            millas = km * 0.621371
            
            horas = int(duracion_segundos // 3600)
            minutos = int((duracion_segundos % 3600) // 60)

            # Mostrar Resumen
            print("\n---------------- RESUMEN DEL VIAJE ----------------")
            print(f"Medio de transporte: {medio}")
            print(f"Distancia en Kilómetros: {km:.2f} km")
            print(f"Distancia en Millas: {millas:.2f} mi")
            print(f"Duración estimada: {horas} horas y {minutos} minutos")
            print("---------------------------------------------------")
            
            # --- SECCIÓN NARRATIVA PASO A PASO REAL ---
            print("\nNARRATIVA DETALLADA EN VIVO:")
            print("===================================================")
            
            contador_paso = 1
            for leg in ruta["legs"]:
                for step in leg["steps"]:
                    tipo = step["maneuver"]["type"]
                    modificador = step["maneuver"].get("modifier", "")
                    
                    # Traducir acción
                    accion = traducir_maniobra(tipo, modificador)
                    
                    # Extraer calle real de los mapas
                    calle = step.get("name", "")
                    calle_str = f" por '{calle}'" if calle else " por la vía asignada"
                    
                    # Distancia de este tramo específico
                    dist_tramo_metros = step["distance"]
                    if dist_tramo_metros >= 1000:
                        dist_str = f"durante {dist_tramo_metros/1000:.1f} km"
                    else:
                        dist_str = f"durante {int(dist_tramo_metros)} metros"
                    
                    if tipo == "arrive":
                        print(f" Paso {contador_paso}: Llegada a tu destino final en {destino}.")
                    else:
                        print(f" Paso {contador_paso}: {accion}{calle_str} y avanza {dist_str}.")
                    
                    contador_paso += 1
                    
            print("===================================================")
        else:
            print("❌ La API no pudo trazar una ruta terrestre directa entre estos puntos.")

if __name__ == "__main__":
    main()