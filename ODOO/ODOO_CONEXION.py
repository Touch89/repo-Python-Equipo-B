import xmlrpc.client

url = "http://localhost:8069/jsonrpc"
db = "modelo-test"
username = "emiliovad1205@gmail.com"
password = ""

def conectarOdoo():
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    if not uid:
        raise Exception("❌ No se pudo hacer login")
    
    print("UID:", uid)

    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return models, uid
