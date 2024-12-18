
# Comparador de Supermercados

Este proyecto es una aplicación que permite comparar los precios de productos en diferentes supermercados. El usuario puede crear una lista de la compra y ver en qué supermercado puede encontrar los productos a mejor precio.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.x
- PostgreSQL (o cualquier otra base de datos que elijas)

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/comparador-app.git
   cd comparador-app
   ```

2. **Instalar dependencias:**
   - Si no tienes un entorno virtual configurado, crea uno y actívalo:
     ```bash
     python -m venv venv
     # En Windows:
     venv\Scripts\activate
     # En macOS/Linux:
     source venv/bin/activate
     ```

   - Instala las dependencias necesarias:
     ```bash
     pip install -r requirements.txt
     ```

## Creación de la Base de Datos

### 1. Crear la Base de Datos

Puedes crear la base de datos con el siguiente comando SQL en PostgreSQL (o en el sistema de base de datos que prefieras):

```sql
CREATE DATABASE comparador_app;
```

### 2. Crear las Tablas

A continuación, crea las tablas necesarias para el funcionamiento de la aplicación. Ejecuta el siguiente SQL para crear la estructura básica de la base de datos:

```sql
-- Tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Tabla de supermercados
CREATE TABLE supermercados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL NOT NULL,
    supermercados_id INTEGER REFERENCES supermercados(id)
);

-- Tabla de listas de compra
CREATE TABLE listas_compra (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL
);
```

### 3. Relación entre las tablas

- La tabla `usuarios` tiene una relación de **uno a muchos** con `listas_compra`, ya que un usuario puede tener varias listas de compra.
- La tabla `productos` tiene una relación de **uno a muchos** con `listas_compra`, ya que un producto puede estar presente en varias listas de compra.
- La tabla `productos` tiene una relación de **muchos a uno** con `supermercados`, ya que un supermercado puede vender varios productos.

## Poblar la Base de Datos con Datos de Prueba

A continuación, te proporciono algunos ejemplos de cómo agregar datos de prueba a las tablas:

### **Insertar Supermercados**

```sql
INSERT INTO supermercados (nombre) VALUES ('Mercadona');
INSERT INTO supermercados (nombre) VALUES ('Dia');
INSERT INTO supermercados (nombre) VALUES ('Carrefour');
```

### **Insertar Productos**

```sql
INSERT INTO productos (nombre, precio, supermercados_id) VALUES ('Pan', 1.50, 1);
INSERT INTO productos (nombre, precio, supermercados_id) VALUES ('Leche', 0.90, 1);
INSERT INTO productos (nombre, precio, supermercados_id) VALUES ('Pan', 1.40, 2);
INSERT INTO productos (nombre, precio, supermercados_id) VALUES ('Leche', 1.00, 2);
INSERT INTO productos (nombre, precio, supermercados_id) VALUES ('Pan', 1.45, 3);
INSERT INTO productos (nombre, precio, supermercados_id) VALUES ('Leche', 1.10, 3);
```

### **Insertar Usuarios**

```sql
INSERT INTO usuarios (username, password, email) VALUES ('usuario1', 'password123', 'usuario1@example.com');
INSERT INTO usuarios (username, password, email) VALUES ('usuario2', 'password456', 'usuario2@example.com');
```

### **Insertar Listas de Compra**

```sql
-- Lista de compra de usuario1
INSERT INTO listas_compra (usuario_id, producto_id, cantidad) VALUES (1, 1, 2);  -- 2 panes
INSERT INTO listas_compra (usuario_id, producto_id, cantidad) VALUES (1, 2, 1);  -- 1 leche

-- Lista de compra de usuario2
INSERT INTO listas_compra (usuario_id, producto_id, cantidad) VALUES (2, 1, 1);  -- 1 pan
INSERT INTO listas_compra (usuario_id, producto_id, cantidad) VALUES (2, 2, 2);  -- 2 leches
```

## Uso de la Aplicación

### 1. **Iniciar la Aplicación**

Para iniciar la aplicación, asegúrate de haber completado la instalación y creado la base de datos correctamente. Luego ejecuta el script principal de tu aplicación:

```bash
python main.py
```

### 2. **Probar la Funcionalidad de la Aplicación**

- **Login de usuario**: Ingresa con las credenciales de los usuarios previamente insertados en la base de datos.
- **Crear una lista de la compra**: Selecciona productos y añade cantidades.
- **Comparar precios entre supermercados**: Una vez que hayas creado una lista de la compra, la aplicación te mostrará el supermercado más barato y los precios en cada uno.

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación utilizado.
- **Tkinter**: Biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
- **CustomTkinter**: Una extensión de Tkinter que proporciona una interfaz gráfica más moderna y personalizable.
- **PostgreSQL**: Sistema de gestión de bases de datos utilizado para almacenar los datos.
- **asyncio**: Módulo de Python para realizar operaciones asincrónicas y manejar conexiones a la base de datos sin bloquear la ejecución.
