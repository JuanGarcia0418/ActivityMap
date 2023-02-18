-- Crear base de datos
CREATE DATABASE cytoscape_db;

-- Usar base de datos
USE cytoscape_db;

-- Crear tabla nodes
CREATE TABLE nodes (
  name VARCHAR(255) PRIMARY KEY,
  date DATE,
  description TEXT
);

-- Crear tabla edges
CREATE TABLE edges (
  id INT PRIMARY KEY AUTO_INCREMENT,
  source VARCHAR(255),
  target VARCHAR(255),
  FOREIGN KEY (source) REFERENCES nodes(name),
  FOREIGN KEY (target) REFERENCES nodes(name)
);