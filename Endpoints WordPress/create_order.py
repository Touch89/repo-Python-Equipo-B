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
        "payment_method": "bacs",
        "payment_method_title": "Transferencia bancaria",
        "status": "processing",
        "billing": {
            "first_name": "Juan",
            "last_name": "Pérez",
            "address_1": "Calle Falsa 123",
            "city": "Ciudad de México",
            "postcode": "06600",
            "country": "MX",
            "email": "juan.perez@example.com",
            "phone": "5512345678"
        },
        "line_items": [
            {
                "product_id": 1,   # reemplaza con un ID de producto real en WooCommerce
                "quantity": 2
            }
        ]
    }

    response = wcapi.post("orders", data)

    if response.status_code in [200, 201]:
        orden = response.json()
        print("Orden creada correctamente")
        print(f"ID: {orden['id']} | Número: {orden.get('number', '')} | Total: ${orden['total']}")
    else:
        print(f"Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"Hubo un error de conexión: {e}")
