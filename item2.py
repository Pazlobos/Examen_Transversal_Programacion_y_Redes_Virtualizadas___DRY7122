import requests
import urllib.parse

# 1. Configuración de la API
API_KEY = "b4aa19fa-386d-4f45-98c3-a0a12df1c4c3" 
GEOC_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(ciudad):
    """Obtiene latitud y longitud de una ciudad mediante Geocoding API"""
    url = GEOC_URL + urllib.parse.urlencode({"q": ciudad, "locale": "es", "key": API_KEY})
    response = requests.get(url).json()
    
    if "hits" in response and len(response["hits"]) > 0:
        point = response["hits"][0]["point"]
        return point["lat"], point["lng"]
    else:
        print(f"Error: No se encontraron coordenadas para {ciudad}")
        return None

def calcular_ruta():
    print("=== Planificador de Viajes - API Graphhopper ===")
    
    # Solicitar datos al usuario
    origen = input("Ciudad de Origen: ")
    destino = input("Ciudad de Destino: ")
    
    # Obtener coordenadas
    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)
    
    if not coord_origen or not coord_destino:
        return

    # 2. Configurar parámetros para la solicitud de ruta
    params = {
        "point": [f"{coord_origen[0]},{coord_origen[1]}", f"{coord_destino[0]},{coord_destino[1]}"],
        "vehicle": "car",
        "locale": "es",       # Solicita las instrucciones en español de forma nativa
        "instructions": "true",
        "key": API_KEY
    }
    
    # Realizar petición de la ruta
    response = requests.get(ROUTE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        ruta = data["paths"][0]
        
        # 3. Procesar datos de la ruta
        distancia_km = ruta["distance"] / 1000  # Graphhopper entrega en metros
        duracion_min = ruta["time"] / 1000 / 60  # Entrega en milisegundos
        horas = int(duracion_min // 60)
        minutos = int(duracion_min % 60)
        
        # Cálculo de combustible aproximado (ej: 12 km por litro)
        combustible = distancia_km / 12

        # 4. Mostrar resultados en pantalla
        print("\n" + "="*40)
        print(f"INFORMACIÓN DEL VIAJE: {origen.upper()} A {destino.upper()}")
        print("="*40)
        print(f"Distancia Total: {distancia_km:.2f} km")
        print(f"Duración Estimada: {horas} horas y {minutos} minutos")
        print(f"Combustible Estimado: {combustible:.2f} Litros (Aprox. 12km/L)")
        print("-"*40)
        print("NARRATIVA DEL VIAJE (PASO A PASO):")
        print("-"*40)
        
        # Mostrar instrucciones paso a paso
        for idx, paso in enumerate(ruta["instructions"], 1):
            texto_instruccion = paso["text"]
            dist_paso = paso["distance"]
            if dist_paso > 0:
                print(f"{idx}. {texto_instruccion} (avanzar {dist_paso:.0f} metros)")
            else:
                print(f"{idx}. {texto_instruccion}")
                
        print("="*40)
    else:
        print(f"Error al calcular la ruta. Código de estado: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    calcular_ruta()