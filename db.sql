-- ============================================================
--  db.sql — Script de creación de la base de datos
--  Ejecutar una sola vez antes de arrancar la aplicación:
--      mysql -u root -p < db.sql
-- ============================================================

-- Crea la base de datos si no existe y la selecciona como activa.
-- 'taller_flask' es el nombre que debe coincidir con el campo
-- 'database' en DB_CONFIG dentro de app.py.
CREATE DATABASE IF NOT EXISTS taller_flask;
USE taller_flask;

-- ============================================================
--  Tabla: tareas
--  Almacena cada tarea del gestor. Una fila = una tarea.
-- ============================================================
CREATE TABLE IF NOT EXISTS tareas (

    -- Identificador único, entero positivo que MySQL incrementa
    -- automáticamente con cada INSERT. PRIMARY KEY garantiza que
    -- no puede haber dos filas con el mismo id.
    id          INT AUTO_INCREMENT PRIMARY KEY,

    -- Título obligatorio: VARCHAR(200) limita a 200 caracteres.
    -- NOT NULL prohíbe insertar una tarea sin título.
    titulo      VARCHAR(200) NOT NULL,

    -- Descripción opcional (puede quedar vacía). TEXT permite
    -- cadenas largas sin límite fijo, ideal para descripciones.
    descripcion TEXT,

    -- Estado de la tarea. BOOLEAN en MySQL se almacena como
    -- TINYINT(1): 0 = pendiente, 1 = completada.
    -- DEFAULT FALSE → toda tarea nueva nace como pendiente.
    completada  BOOLEAN DEFAULT FALSE,

    -- Fecha y hora de creación. TIMESTAMP almacena el momento
    -- exacto (zona horaria del servidor). DEFAULT CURRENT_TIMESTAMP
    -- lo rellena automáticamente al hacer INSERT, sin que la
    -- aplicación tenga que enviar el valor.
    creada_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
