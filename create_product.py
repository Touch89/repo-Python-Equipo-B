from woocommerce import API

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_6ca7ce3cfe2e00e29777e448b45518707b22f404",
    consumer_secret="cs_ac042df24d3e1cb6f12bda36415605c0e26502ea",
    version="wc/v3",
    timeout=20
)

try:
    data = {
        "name": "Producto X",
        "type": "X",
        "regular_price": "100.00",
        "description": "Producto de prueba",
        "sku": "001"
    }

    response = wcapi.post("products", data)

    if response.status_code in [200, 201]:
        producto = response.json()
        print("Producto creado correctamente")
        print(f"ID: {producto['id']} | Nombre: {producto['name']}")
    else:
        print(f"Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"Hubo un error de conexión: {e}")