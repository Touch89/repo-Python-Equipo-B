from woocommerce import API

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_6ca7ce3cfe2e00e29777e448b45518707b22f404",
    consumer_secret="cs_ac042df24d3e1cb6f12bda36415605c0e26502ea",
    version="wc/v3",
    timeout=20
)

try:
    response = wcapi.get("products", params={"per_page": 10})

    if response.status_code == 200:
        productos = response.json()
        print(f"--- Se encontraron {len(productos)} productos ---")

        for p in productos:
            print(f"ID: {p['id']} | Nombre: {p['name']} | Precio: ${p['price']}")
    else:
        print(f"Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"Hubo un error de conexión: {e}")