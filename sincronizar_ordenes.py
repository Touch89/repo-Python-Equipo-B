from woocommerce import API
import xmlrpc.client

url = "http://localhost:8069"
db = "db-examen"
username = "emicamposdaguer@gmail.com"
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


def obtener_producto_wc_por_sku(sku):
    if not sku:
        return None
    resultado = wcapi.get("products", params={"sku": sku}).json()
    if resultado and isinstance(resultado, list):
        return resultado[0]["id"]
    return None


def obtener_producto_wc_por_nombre(nombre):
    if not nombre:
        return None
    resultado = wcapi.get("products", params={"search": nombre, "per_page": 10}).json()
    if not isinstance(resultado, list) or not resultado:
        return None

    nombre_normalizado = nombre.strip().lower()
    for producto in resultado:
        if (producto.get("name") or "").strip().lower() == nombre_normalizado:
            return producto.get("id")

    return resultado[0].get("id")


def obtener_datos_producto_odoo(product_id):
    producto = models.execute_kw(
        db, uid, api_key,
        'product.product', 'read',
        [[product_id]],
        {'fields': ['default_code', 'name', 'product_tmpl_id']}
    )[0]

    sku = producto.get("default_code") or ""
    nombre = producto.get("name") or ""

    if not sku and producto.get("product_tmpl_id"):
        template_id = producto["product_tmpl_id"][0]
        template = models.execute_kw(
            db, uid, api_key,
            'product.template', 'read',
            [[template_id]],
            {'fields': ['default_code', 'name']}
        )[0]
        sku = template.get("default_code") or ""
        if not nombre:
            nombre = template.get("name") or ""

    return sku, nombre


def email_valido(email):
    if not email or "@" not in email:
        return False
    local, dominio = email.rsplit("@", 1)
    return bool(local.strip()) and "." in dominio and not dominio.startswith(".") and not dominio.endswith(".")


def orden_ya_existe_en_wc(numero_odoo):
    resultado = wcapi.get("orders", params={"search": numero_odoo, "per_page": 5}).json()
    if isinstance(resultado, list):
        for o in resultado:
            metas = {m["key"]: m["value"] for m in o.get("meta_data", [])}
            if metas.get("_odoo_ref") == numero_odoo:
                return True
    return False


try:
    ordenes_odoo = models.execute_kw(
        db, uid, api_key,
        'sale.order', 'search_read',
        [[['state', 'in', ['sale', 'done']]]],
        {'fields': ['name', 'partner_id', 'date_order', 'amount_total', 'order_line']}
    )

    print(f"--- {len(ordenes_odoo)} órdenes encontradas en Odoo ---")

    for orden in ordenes_odoo:
        numero = orden["name"]

        if orden_ya_existe_en_wc(numero):
            print(f"Ya existe en WooCommerce: {numero}")
            continue

        partner_id = orden["partner_id"][0]
        partner = models.execute_kw(
            db, uid, api_key,
            'res.partner', 'read',
            [[partner_id]],
            {'fields': ['name', 'email', 'phone', 'street', 'city', 'zip', 'country_id']}
        )[0]

        nombre_partes = partner["name"].split(" ", 1)
        first_name = nombre_partes[0]
        last_name = nombre_partes[1] if len(nombre_partes) > 1 else ""
        country_code = partner["country_id"][1] if partner["country_id"] else "MX"
        email_partner = (partner.get("email") or "").strip()
        if not email_valido(email_partner):
            email_partner = "cliente.odoo@example.com"

        lineas = models.execute_kw(
            db, uid, api_key,
            'sale.order.line', 'read',
            [orden["order_line"]],
            {'fields': ['product_id', 'product_uom_qty', 'price_unit', 'name']}
        )

        line_items = []
        for linea in lineas:
            sku = ""
            nombre_producto = linea.get("name") or ""
            if linea["product_id"]:
                sku, nombre_producto_odoo = obtener_datos_producto_odoo(linea["product_id"][0])
                if nombre_producto_odoo:
                    nombre_producto = nombre_producto_odoo

            wc_product_id = obtener_producto_wc_por_sku(sku)
            if wc_product_id is None:
                wc_product_id = obtener_producto_wc_por_nombre(nombre_producto)

            if wc_product_id is None:
                print(
                    f"  [!] Producto no encontrado en WooCommerce. "
                    f"SKU='{sku}' | Nombre='{nombre_producto}'. Se omite la línea."
                )
                continue

            line_items.append({
                "product_id": wc_product_id,
                "quantity": int(linea["product_uom_qty"]),
                "price": str(linea["price_unit"])
            })

        if not line_items:
            print(f"  [!] Orden {numero} sin líneas válidas, se omite.")
            continue

        data = {
            "payment_method": "bacs",
            "payment_method_title": "Transferencia bancaria",
            "status": "processing",
            "billing": {
                "first_name": first_name,
                "last_name": last_name,
                "address_1": partner.get("street") or "",
                "city": partner.get("city") or "",
                "postcode": partner.get("zip") or "",
                "country": country_code,
                "email": email_partner,
                "phone": partner.get("phone") or ""
            },
            "line_items": line_items,
            "meta_data": [
                {"key": "_odoo_ref", "value": numero}
            ]
        }

        response = wcapi.post("orders", data)

        if response.status_code in [200, 201]:
            wc_orden = response.json()
            print(f"Creada: {numero} → WC ID {wc_orden['id']} | Total: ${wc_orden['total']}")
        else:
            print(f"Error al crear {numero}: {response.text}")

except Exception as e:
    print(f"Hubo un error: {e}")
