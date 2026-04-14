from woocommerce import API
import xmlrpc.client

url = "http://localhost:8069"
db = "angeldb"
username = "15234649@modelo.edu.mx"
password = "7acefaef79670d8f67703b760101a52a9ca6630f"

wcapi = API(
    url="http://localhost:8080",
    consumer_key="ck_6ca7ce3cfe2e00e29777e448b45518707b22f404",
    consumer_secret="cs_ac042df24d3e1cb6f12bda36415605c0e26502ea",
    version="wc/v3",
    timeout=20
)

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

try:
    productos_odoo = models.execute_kw(
        db,
        uid,
        password,
        'product.template',
        'search_read',
        [[]],
        {'fields': ['name', 'list_price', 'default_code']}
    )

    print(f"--- {len(productos_odoo)} Productos encontrados en Odoo ---")

    for p in productos_odoo:
        sku = p["default_code"] or ""

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