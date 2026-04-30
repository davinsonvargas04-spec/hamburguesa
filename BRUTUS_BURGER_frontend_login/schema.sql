CREATE DATABASE IF NOT EXISTS tienda_contabilidad
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tienda_contabilidad;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  correo VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
