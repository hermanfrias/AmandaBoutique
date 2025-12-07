# 👗 Amanda Mateo Boutique

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.7-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

**Sistema de Gestión Integral para Boutique de Vestidos de Quinceañera**

[🇪🇸 Español](#español) • [🇺🇸 English](#english) • [📹 Video Demo](https://youtu.be/XqdgIVWoqEk)

</div>

---

## 🇪🇸 Español

### 📋 Descripción

**Amanda Mateo Boutique** es un sistema de gestión integral desarrollado en Django para administrar todos los aspectos de una boutique especializada en vestidos de quinceañera hechos a medida. El sistema incluye un showroom dinámico, gestión de inventario, control de citas, seguimiento de clientes y proveedores, y un completo módulo de flujo de caja con conversión automática de divisas.

### ✨ Características Principales

#### 🏠 **Showroom Dinámico**

- Catálogo visual de vestidos con imágenes
- Visualización automática de todos los modelos disponibles
- Información detallada de cada diseño (estilo, precio, descripción)
- Generación de catálogos PDF en dos formatos:
  - Lista de productos
  - Fichas individuales por modelo

#### 📅 **Gestión de Citas**

- Calendario interactivo con FullCalendar
- Registro de citas con información completa del cliente
- Seguimiento de fechas de entrega
- Registro de medidas (copa, busto, cintura, largo, tiras)
- Control de pagos (precio, abono, pago total)
- Soporte para múltiples monedas (USD/Bs)
- Generación de reportes PDF filtrados por fecha

#### 👥 **Gestión de Clientes**

- Base de datos completa de clientes
- Búsqueda rápida por nombre
- Información de contacto y dirección
- Historial de citas y compras

#### 🏭 **Gestión de Proveedores**

- Registro de proveedores
- Información de contacto
- Búsqueda y filtrado

#### 💰 **Flujo de Caja**

- Control de ingresos y egresos
- Conversión automática Bs → USD usando cotización del día
- **Filtros avanzados:**
  - Filtro por rango de fechas (inicio y fin)
  - Filtro por tipo de movimiento (Todos/Ingreso/Gasto)
- Dashboard financiero con:
  - Resumen mensual y anual
  - Totales acumulados
  - Métricas de rentabilidad
- Exportación a Excel y PDF con filtros aplicados
- Columnas de montos alineadas a la derecha para mejor legibilidad

#### 💵 **Cotización del Dólar**

- Registro de tasas de cambio diarias
- Conversión automática en movimientos de caja
- Historial de cotizaciones

#### 👤 **Gestión de Usuarios**

- Sistema de autenticación completo
- Perfiles de usuario personalizados
- Control de acceso a funciones administrativas
- Registro, login y logout

### 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.11+ / Django 5.2.7
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5.3
- **PDF Generation:** WeasyPrint + GTK3 Runtime
- **Calendario:** FullCalendar
- **Exportación:** OpenPyXL (Excel)
- **Deployment:** WhiteNoise (archivos estáticos)

### 📦 Instalación

#### Prerrequisitos

- Python 3.11 o superior
- GTK3 Runtime (requerido para WeasyPrint)

#### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/AmandaBoutique.git
cd AmandaBoutique
```

2. **Crear entorno virtual**

```bash
python -m venv .venv
```

3. **Activar entorno virtual**

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Instalar GTK3 Runtime** (Windows)

   - Descargar desde: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
   - Ejecutar el instalador
   - Agregar GTK3 al PATH del sistema

6. **Configurar variables de entorno**

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
```

7. **Aplicar migraciones**

```bash
python manage.py migrate
```

8. **Crear superusuario**

```bash
python manage.py createsuperuser
```

9. **Recolectar archivos estáticos**

```bash
python manage.py collectstatic
```

10. **Ejecutar servidor de desarrollo**

```bash
python manage.py runserver
```

11. **Acceder a la aplicación**

- Aplicación: http://localhost:8000
- Admin: http://localhost:8000/admin

### 🚀 Despliegue en Producción

#### Configuración como Servicio Windows (NSSM)

1. **Descargar NSSM**

   - https://nssm.cc/download

2. **Instalar el servicio**

```powershell
nssm install DjangoBoutique "C:\ruta\a\.venv\Scripts\python.exe" "C:\ruta\a\server.py"
nssm set DjangoBoutique AppDirectory "C:\ruta\a\AmandaBoutique"
nssm set DjangoBoutique DisplayName "Amanda Boutique - Django Server"
nssm set DjangoBoutique Description "Servidor Django para Amanda Mateo Boutique"
nssm start DjangoBoutique
```

3. **Configurar variables de entorno en .env**

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-segura
ALLOWED_HOSTS=192.168.1.193,tudominio.com
```

### 📁 Estructura del Proyecto

```
AmandaBoutique/
├── AmandaProjecto/          # Configuración principal del proyecto
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # WSGI para producción
├── BoutiqueApp/             # App principal - Showroom y Catálogo
│   ├── models.py            # Modelo: Catalogo
│   ├── views.py             # Vistas y lógica
│   ├── forms.py             # Formularios
│   ├── urls.py              # URLs de la app
│   └── templates/           # Templates HTML
├── ClientesApp/             # Gestión de Clientes
│   ├── models.py            # Modelo: Cliente
│   └── ...
├── ProveedoresApp/          # Gestión de Proveedores
│   ├── models.py            # Modelo: Proveedor
│   └── ...
├── citas/                   # Gestión de Citas
│   ├── models.py            # Modelo: Cita
│   └── ...
├── flujo/                   # Flujo de Caja
│   ├── models.py            # Modelos: MovimientoCaja, CotizacionDolar
│   └── ...
├── LoginApp/                # Autenticación y Perfiles
│   ├── models.py            # Modelo: PerfilUsuario
│   └── ...
├── static/                  # Archivos estáticos
│   ├── css/
│   │   └── estilos.css      # Estilos personalizados
│   └── ...
├── media/                   # Archivos subidos (imágenes)
├── db.sqlite3               # Base de datos
├── manage.py                # Utilidad de Django
├── requirements.txt         # Dependencias
└── README.md                # Este archivo
```

### 🎨 Modelos de Datos

#### Catalogo

- Código, Modelo, Estilo, Descripción, Precio, Imagen

#### Cliente

- Identificación, Nombre, Apellido, Dirección, Teléfono, Email

#### Proveedor

- Código, Nombre, Dirección, Teléfono, Email

#### Cita

- Cliente, Teléfono, Fecha, Hora, Acción
- Fecha de Entrega
- Medidas: Copa, Busto, Cintura, Largo, Tiras
- Precio, Abono, Pago Total, Moneda
- Descripción

#### MovimientoCaja

- Fecha, Descripción, Tipo (Ingreso/Egreso)
- Monto, Moneda, Monto USD

#### CotizacionDolar

- Fecha, Tasa de Cambio

#### PerfilUsuario

- Usuario, Email, Avatar
- Ciudad, País, Teléfono, Fecha de Nacimiento

### 📖 Uso del Sistema

1. **Acceso al Sistema**

   - Iniciar sesión con credenciales de usuario
   - Los usuarios no autenticados solo pueden ver el showroom público

2. **Panel de Administración**

   - Acceso rápido desde el navbar mediante menú desplegable
   - Enlaces organizados en una sola columna
   - Diseño coherente con el tema rosa del sitio
   - Acceso a todos los módulos: Administración, Citas, Catálogo, Clientes, Proveedores, Flujo de Caja, Cotización, Resumen

3. **Gestión de Catálogo**

   - Agregar nuevos modelos con imágenes
   - Editar información de vestidos existentes
   - Generar catálogos PDF

4. **Gestión de Citas**

   - Crear citas con información completa
   - Ver calendario visual
   - Generar reportes de citas

5. **Control Financiero**
   - Registrar ingresos y egresos
   - Ver dashboard con métricas
   - Exportar reportes

### 🔒 Seguridad

- Autenticación requerida para funciones administrativas
- SECRET_KEY configurable vía variables de entorno
- CSRF protection habilitado
- Validación de formularios
- Control de acceso por usuario

### 📝 Notas Importantes

- **GTK3 Runtime** es obligatorio para la generación de PDFs
- El sistema usa **SQLite** por defecto (apropiado para pequeñas/medianas empresas)
- Para producción, se recomienda configurar **DEBUG=False** en `.env`
- Los archivos de media se almacenan en `/media/`

### 🤝 Contribuciones

Este es un proyecto personal, pero las sugerencias y mejoras son bienvenidas.

### 👨‍💻 Autor

**Herman Frias**

### 📄 Licencia

Este proyecto es de uso privado para Amanda Mateo Boutique.

---

## 🇺🇸 English

### 📋 Description

**Amanda Mateo Boutique** is a comprehensive management system developed in Django to manage all aspects of a boutique specialized in custom-made quinceañera dresses. The system includes a dynamic showroom, inventory management, appointment scheduling, customer and supplier tracking, and a complete cash flow module with automatic currency conversion.

### ✨ Key Features

#### 🏠 **Dynamic Showroom**

- Visual dress catalog with images
- Automatic display of all available models
- Detailed information for each design (style, price, description)
- PDF catalog generation in two formats:
  - Product list
  - Individual model cards

#### 📅 **Appointment Management**

- Interactive calendar with FullCalendar
- Appointment registration with complete customer information
- Delivery date tracking
- Measurements recording (cup, bust, waist, length, straps)
- Payment control (price, deposit, total payment)
- Multi-currency support (USD/Bs)
- PDF report generation filtered by date

#### 👥 **Customer Management**

- Complete customer database
- Quick search by name
- Contact information and address
- Appointment and purchase history

#### 🏭 **Supplier Management**

- Supplier registration
- Contact information
- Search and filtering

#### 💰 **Cash Flow**

- Income and expense control
- Automatic Bs → USD conversion using daily exchange rate
- **Advanced filters:**
  - Date range filter (start and end)
  - Movement type filter (All/Income/Expense)
- Financial dashboard with:
  - Monthly and annual summary
  - Cumulative totals
  - Profitability metrics
- Excel and PDF export with applied filters
- Amount columns right-aligned for better readability

#### 💵 **Dollar Exchange Rate**

- Daily exchange rate recording
- Automatic conversion in cash movements
- Exchange rate history

#### 👤 **User Management**

- Complete authentication system
- Custom user profiles
- Access control to administrative functions
- Registration, login, and logout

### 🛠️ Technologies Used

- **Backend:** Python 3.11+ / Django 5.2.7
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5.3
- **PDF Generation:** WeasyPrint + GTK3 Runtime
- **Calendar:** FullCalendar
- **Export:** OpenPyXL (Excel)
- **Deployment:** WhiteNoise (static files)

### 📦 Installation

#### Prerequisites

- Python 3.11 or higher
- GTK3 Runtime (required for WeasyPrint)

#### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/your-user/AmandaBoutique.git
cd AmandaBoutique
```

2. **Create virtual environment**

```bash
python -m venv .venv
```

3. **Activate virtual environment**

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Install GTK3 Runtime** (Windows)

   - Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
   - Run the installer
   - Add GTK3 to system PATH

6. **Configure environment variables**

```bash
# Copy example file
copy .env.example .env

# Edit .env with your settings
```

7. **Apply migrations**

```bash
python manage.py migrate
```

8. **Create superuser**

```bash
python manage.py createsuperuser
```

9. **Collect static files**

```bash
python manage.py collectstatic
```

10. **Run development server**

```bash
python manage.py runserver
```

11. **Access the application**

- Application: http://localhost:8000
- Admin: http://localhost:8000/admin

### 🚀 Production Deployment

#### Windows Service Configuration (NSSM)

1. **Download NSSM**

   - https://nssm.cc/download

2. **Install the service**

```powershell
nssm install DjangoBoutique "C:\path\to\.venv\Scripts\python.exe" "C:\path\to\server.py"
nssm set DjangoBoutique AppDirectory "C:\path\to\AmandaBoutique"
nssm set DjangoBoutique DisplayName "Amanda Boutique - Django Server"
nssm set DjangoBoutique Description "Django server for Amanda Mateo Boutique"
nssm start DjangoBoutique
```

3. **Configure environment variables in .env**

```env
DEBUG=False
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=192.168.1.193,yourdomain.com
```

### 📝 Important Notes

- **GTK3 Runtime** is mandatory for PDF generation
- The system uses **SQLite** by default (suitable for small/medium businesses)
- For production, it's recommended to set **DEBUG=False** in `.env`
- Media files are stored in `/media/`

### 🤝 Contributions

This is a personal project, but suggestions and improvements are welcome.

### 👨‍💻 Author

**Herman Frias**

### 📄 License

This project is for private use by Amanda Mateo Boutique.

---

<div align="center">

**Hecho con ❤️ para Amanda Mateo Boutique**

[⬆ Volver arriba](#-amanda-mateo-boutique)

</div>
