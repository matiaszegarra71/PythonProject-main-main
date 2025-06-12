-- Configuración inicial de la base de datos
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS flask_notes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE flask_notes_db;

-- Configurar zona horaria
SET time_zone = '+00:00';

-- Configuraciones de MySQL para mejor rendimiento
SET GLOBAL innodb_buffer_pool_size = 128M;
SET GLOBAL max_connections = 100;

-- Mensaje de confirmación
SELECT 'Base de datos inicializada correctamente' AS status;
