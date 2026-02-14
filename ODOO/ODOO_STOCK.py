from ODOO_CONEXION import conectarOdoo, db, password

def crearStock(product_ids, quantity=50):
    models, uid = conectarOdoo()

    location = models.execute_kw(
        db,
        uid,
        password,
        "stock.location",
        "search_read",
        [[("usage", "=", "internal")]],
        {"limit": 1}
    )

    if not location:
        raise Exception("❌ Localización no encontrada")
    
    location_id = location[0]["id"]

    stock_quants = []
    for product_id in product_ids:
        stock_quants.append({
            "product_id": product_id,
            "location_id": location_id,
            "quantity": quantity
        })

    quant_ids = models.execute_kw(
        db,
        uid,
        password,
        "stock.quant",
        "create",
        [stock_quants]
    )

    return {
        "created_stock": quant_ids,
        "count": len(quant_ids)
    }
