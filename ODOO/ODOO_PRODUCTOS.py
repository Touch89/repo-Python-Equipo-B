import requests
from ODOO_CONEXION import conectarOdoo, url, db, password

def crearProductos():
    models, uid = conectarOdoo()

    products = []
    
    for i in range(1, 21):
        products.append({
            "name": f"Producto Prueba {i}",
            "default_code": f"PRD-{str(i).zfill(3)}",
            "list_price": 100 + i,
            "standard_price": 60 + i,
            "type": "product",
            "sale_ok": True,
            "purchase_ok": True
        })
    
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                db,
                uid,
                password,
                "product.template",
                "create",
                [products]
            ]
        }
    }

    response = requests.post(url, json=payload)
    print("CREATE:", response.json())