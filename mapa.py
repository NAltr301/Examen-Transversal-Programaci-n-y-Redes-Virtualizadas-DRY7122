import requests

API_KEY = "6c8b13f1-ce20-48a1-a662-1c54eef1595c"

def geocodificar(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {"q": ciudad, "locale": "es", "limit": 1, "key": API_KEY}
    r = requests.get(url, params=params).json()
    hit = r["hits"][0]
    return hit["point"]["lat"], hit["point"]["lng"]

vehiculos = {"1": "car", "2": "bike", "3": "foot"}

while True:
    origen = input("Ciudad de Origen (o 's' para salir): ")
    if origen.lower() == "s":
        break
    destino = input("Ciudad de Destino: ")

    print("Elija medio de transporte: 1) Auto  2) Bicicleta  3) A pie")
    opcion = input("Opción: ")
    perfil = vehiculos.get(opcion, "car")

    lat1, lon1 = geocodificar(origen)
    lat2, lon2 = geocodificar(destino)

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{lat1},{lon1}", f"{lat2},{lon2}"],
        "vehicle": perfil,
        "locale": "es",
        "key": API_KEY,
        "instructions": "true",
    }
    resp = requests.get(url, params=params).json()
    path = resp["paths"][0]

    millas = path["distance"] / 1609.34
    km = path["distance"] / 1000
    duracion_min = path["time"] / 60000

    print(f"\nDistancia: {km:.2f} km / {millas:.2f} millas")
    print(f"Duración estimada: {duracion_min:.1f} minutos")
    print("Narrativa del viaje:")
    for paso in path["instructions"]:
        print(f" - {paso['text']}")
    print()