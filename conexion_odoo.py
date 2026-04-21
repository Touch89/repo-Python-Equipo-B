from woocommerce import API
import xmlrpc.client

url = "http://localhost:8069"
db = "db-examen"
username = "emicamposdaguer@gmail.com"
password = "1234"
api_key = "c2a2bafaafa1c25f36e3e70f118248d78efd3dea"

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_9c6d28c23a59b2eafd8509daadc67fed2e37b4db",
    consumer_secret="cs_e78854f36a3a1c9a568221fa1b5e328351271571",
    version="wc/v3",
    timeout=20
)

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, api_key, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

try:
    productos_odoo = models.execute_kw(
        db,
        uid,
        api_key,
        'product.template',
        'search_read',
        [[]],
        {'fields': ['name', 'list_price', 'default_code']}
    )

    print(f"--- {len(productos_odoo)} Productos encontrados en Odoo ---")

    for p in productos_odoo:
        sku = p["default_code"] or ""

        if sku:
            existing = wcapi.get("products", params={"sku": sku}).json()
            if existing:
                print(f"El producto ya existe: {p['name']}")
                continue

        data = {
            "name": p["name"],
            "type": "simple",
            "regular_price": str(p["list_price"]),
            "sku": sku,
            "description": "Importado desde Odoo"
        }

        response = wcapi.post("products", data)

        if response.status_code in [200, 201]:
            print(f"Creado: {p['name']}")
        else:
            print(f"Error {p['name']}: {response.text}")

except Exception as e:
    print(f"Hubo un error de conexión: {e}")