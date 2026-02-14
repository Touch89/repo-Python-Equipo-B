from ODOO_CONEXION import conectarOdoo, db, password

def crearProveedores():
    models, uid = conectarOdoo()

    proveedores = []
    for i in range(1, 6):
        proveedores.append({
            "name": f"Proveedor {i}",
            "email": f"proveedor{i}@gmail.com",
            "phone": f"999000{i}",
            "supplier_rank": 1
        })

    proveedor_ids = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "create",
        [proveedores]
    )

    return {
        "created_suppliers": proveedor_ids,
        "count": len(proveedor_ids)
    }
