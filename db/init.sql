CREATE TABLE users (
    ID int NOT NULL,
    uname VARCHAR(255) NOT NULL,
    pword VARCHAR(16) NOT NULL,
    names VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    github VARCHAR(255),
    register_date date NOT NULL,
    PRIMARY KEY (ID)
)
