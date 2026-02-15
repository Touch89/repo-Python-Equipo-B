from fastapi import FastAPI, Query
import requests

app = FastAPI(title="API Odoo - Equipo B")

ODOO_URL = "http://localhost:8069/jsonrpc"
DB = "modelo-test"
USERNAME = "emiliovad1205@gmail.com"
PASSWORD = ""


def odoo_login():
    payload = {
        "jsonrpc": "2.0",
        "params": {
            "service": "common",
            "method": "login",
            "args": [DB, USERNAME, PASSWORD]
        }
    }
    r = requests.post(ODOO_URL, json=payload)
    uid = r.json().get("result")
    if not uid:
        raise Exception("No se pudo hacer login en Odoo")
    return uid


def odoo_execute_kw(uid, model, method, args, kwargs=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [DB, uid, PASSWORD, model, method, args, kwargs or {}]
        }
    }
    r = requests.post(ODOO_URL, json=payload)
    return r.json().get("result")


@app.get("/categories")
def get_categories(limit: int = 100, offset: int = 0):

    uid = odoo_login()

    categories = odoo_execute_kw(
        uid,
        "product.category",
        "search_read",
        [[]],
        {
            "fields": ["id", "name", "parent_id", "complete_name"],
            "limit": limit,
            "offset": offset
        }
    )

    return {"count": len(categories), "data": categories}
