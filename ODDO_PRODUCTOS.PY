import requests


url = "http://localhost:8069/jsonrpc"
db = "modelo-test"
username = "emiliovad1205@gmail.com"
password = ""  


payload = {
    "jsonrpc": "2.0",
    "params": {
        "service": "common",
        "method": "login",
        "args": [db, username, password]
    }
}

response = requests.post(url, json=payload)
print("LOGIN:", response.json())

uid = response.json().get("result")
if not uid:
    raise Exception("❌ No se pudo hacer login")

print("UID:", uid)


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