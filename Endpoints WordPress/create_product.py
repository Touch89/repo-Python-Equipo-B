from woocommerce import API

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_9c6d28c23a59b2eafd8509daadc67fed2e37b4db",
    consumer_secret="cs_e78854f36a3a1c9a568221fa1b5e328351271571",
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