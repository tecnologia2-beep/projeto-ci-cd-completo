CREATE DATABASE IF NOT EXISTS db_produtos;

USE db_produtos;

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(8) UNIQUE NOT NULL,
    sec INT NOT NULL,
    Grupo CHAR(1) NOT NULL,
    Tipo_Alimento CHAR(1) NOT NULL,
    Pais CHAR(2) NOT NULL
);

INSERT INTO produtos (codigo, sec, Grupo, Tipo_Alimento, Pais) VALUES
('BRC0001A',1,'C','A','BR'),
('BRC0002A',2,'C','A','BR'),
('BRC0003C',3,'C','C','BR');
