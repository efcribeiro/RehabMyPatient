CREATE USER 'projete'@'%' IDENTIFIED BY '****';
GRANT SELECT, INSERT, UPDATE, DELETE ON projete.* TO 'projete'@'%';
FLUSH PRIVILEGES;

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT,
    cpf VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255),
    cidade VARCHAR(255),
    uf VARCHAR(255) ,
    idade INT,
    altura FLOAT,
    peso FLOAT,
    problema TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE exames (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    id_paciente INT NOT NULL,
    nome_do_exame VARCHAR(255) NOT NULL,
    resultado TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id)
);

INSERT INTO pacientes (nome, cpf, endereco, idade) VALUES
    ('João da Silva', '12398765409', '123 Rua Principal', 30),
    ('Maria Souza', '3679285675', '456 Avenida Secundária', 25),
    ('Pedro Santos', '28736545698','789 Rua do Centro', 35);


INSERT INTO exames (data, id_paciente, nome_do_exame, resultado) VALUES
    ('2023-09-01', 1, 'Flexão e extenção de cotovelo', 'teste'),
    ('2023-09-05', 2, 'Abdução e adução da mão', 'teste'),
    ('2023-09-10', 1, 'Flexão e extenção de ombro', 'teste'),
    ('2023-09-15', 3, 'Flexão e extenção de cotovelo', 'teste');
