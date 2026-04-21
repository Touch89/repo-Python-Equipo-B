from woocommerce import API

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_9c6d28c23a59b2eafd8509daadc67fed2e37b4db",
    consumer_secret="cs_e78854f36a3a1c9a568221fa1b5e328351271571",
    version="wc/v3",
    timeout=20
)

try:
    response = wcapi.get("orders", params={"per_page": 10})

    if response.status_code == 200:
        ordenes = response.json()
        print(f"--- Se encontraron {len(ordenes)} órdenes ---")

        for o in ordenes:
            cliente = o["billing"].get("first_name", "") + " " + o["billing"].get("last_name", "")
            print(
                f"ID: {o['id']} | "
                f"Ref: {o.get('number', '')} | "
                f"Cliente: {cliente.strip()} | "
                f"Total: ${o['total']} | "
                f"Estado: {o['status']}"
            )
    else:
        print(f"Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"Hubo un error de conexión: {e}")
