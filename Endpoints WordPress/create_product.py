from woocommerce import API

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_60afc1def93687705868d1dcae2f4448d9719355",
    consumer_secret="cs_fbf5b942b4445ebf0340a17384bb5e934a3f2c12",
    version="wc/v3",
    timeout=20
)

try:
    data = {
        "name": "Producto x",
        "type": "simple",
        "regular_price": "100.00",
        "description": "Producto de prueba",
        "sku": "009"
    }

    response = wcapi.post("products", data)

    if response.status_code in [200, 201]:
        producto = response.json()
        print("Producto creado correctamente")
        print(f"ID: {producto['id']} | Nombre: {producto['name']} | Precio: {producto['regular_price']}")
    else:
        print(f"Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"Hubo un error de conexión: {e}")