# 🏪 Shiloh Store — Sistema de Inventario Web

Sistema web para gestión de inventario de tienda de celulares y accesorios tecnológicos. Desarrollado con Python y Flask.

🌐 **Demo en vivo:** https://inventario-web-7dzv.onrender.com

---

## 📸 Capturas

<img width="959" height="440" alt="logingit" src="https://github.com/user-attachments/assets/8afc90a3-d614-4cac-82d3-f5daa9b33a40" />
<img width="959" height="439" alt="dashgit" src="https://github.com/user-attachments/assets/cb18ca4c-0f5e-48de-834b-9fcfbd297342" />
<img width="959" height="233" alt="usuariosgit" src="https://github.com/user-attachments/assets/773ddda9-c57f-47ff-9eb5-e98926557c81" />
<img width="959" height="304" alt="ubicaciongit" src="https://github.com/user-attachments/assets/6ef7761d-9920-4123-8f5c-d76bc7866bbc" />
<img width="959" height="386" alt="agregargit" src="https://github.com/user-attachments/assets/fa233525-c364-4aad-9276-280add71f569" />



---

## ✅ Funcionalidades

- 🔐 Login con roles (Jefe y Trabajador)
- 📦 CRUD completo de productos
- 📱 Especificaciones detalladas de celulares (IMEI, RAM, cámara, batería, etc.)
- 💰 Sistema de ventas con historial
- 🪟 Ubicaciones: Vitrina y Almacén
- 🏪 Dos tiendas: Shiloh Store y Nova Smart
- 📊 Estadísticas del inventario (total, stock bajo, valor total)
- 🔍 Buscador de productos
- 📱 Diseño responsive para móvil

---

## 🔐 Roles del sistema

| Rol | Permisos |
|---|---|
| **Jefe** | Ver, agregar, editar, eliminar productos y usuarios |
| **Trabajador** | Solo visualizar el inventario y registrar ventas |

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje principal |
| Flask | Framework web |
| SQLAlchemy | ORM para base de datos |
| Flask-Login | Autenticación y sesiones |
| Werkzeug | Encriptación de contraseñas |
| PostgreSQL | Base de datos en producción |
| SQLite | Base de datos local |
| Bootstrap 5 | Diseño responsive |
| Jinja2 | Motor de plantillas |
| Gunicorn | Servidor WSGI |
| Render | Deploy en la nube |
| GitHub | Control de versiones |

---

## 🚀 Instalación local

```bash
# 1 - Clona el repositorio
git clone https://github.com/SantiagoRojas12/inventario-web.git
cd inventario-web

# 2 - Crea el entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3 - Instala dependencias
pip install -r requirements.txt

# 4 - Ejecuta
python run.py
```

Abre el navegador en `http://127.0.0.1:5000`

---

## ⚙️ Variables de entorno

Para producción configura estas variables:

SECRET_KEY=tu_clave_secreta

DATABASE_URL=postgresql://...

---

## 👤 Autor

**Santiago Rojas**
- GitHub: [@SantiagoRojas12](https://github.com/SantiagoRojas12)
- LinkedIn: https://www.linkedin.com/in/pedro-santiago-jara-rojas-124a65173/

---

## 📄 Licencia

Este proyecto es de uso privado para Shiloh Store.
