from app import create_app, db

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        columnas = [
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS marca VARCHAR(50)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS almacenamiento VARCHAR(50)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS color VARCHAR(50)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS camara_trasera VARCHAR(100)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS camara_frontal VARCHAR(100)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS bateria VARCHAR(50)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS cargador_watts VARCHAR(50)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS conectividad VARCHAR(50)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS imei1 VARCHAR(20)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS imei2 VARCHAR(20)",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS tienda VARCHAR(50) DEFAULT 'Shiloh Store'",
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS ram VARCHAR(50)",
        ]
        for sql in columnas:
            conn.execute(db.text(sql))
        conn.commit()
        print('✅ Columnas agregadas correctamente')