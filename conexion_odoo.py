from woocommerce import API
import xmlrpc.client

url = "http://localhost:8069"
db = "EMIDB"
username = "emiliovad1205@gmail.com"
password = "Emilio#121105"
api_key = "3c04e0ec525ffc1e2ed2a76a46f04e1cf5e88592"

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_60afc1def93687705868d1dcae2f4448d9719355",
    consumer_secret="cs_fbf5b942b4445ebf0340a17384bb5e934a3f2c12",
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