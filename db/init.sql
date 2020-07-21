CREATE TABLE users (
    ID int NOT NULL,
    github VARCHAR(255) NOT NULL,
    pword VARCHAR(16) NOT NULL,
    names VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    github_url VARCHAR(255),
    register_date date NOT NULL,
    company VARCHAR(255),
    user_location VARCHAR(255),
    follower INT,
    PRIMARY KEY (ID)
);


CREATE TABLE repos (
    REPO_ID int NOT NULL,
    repo_name VARCHAR(255) NOT NULL,
    repo_url VARCHAR(255) NOT NULL,
    created_date VARCHAR(25) NOT NULL,
    repo_description VARCHAR(255),
    forks INT,
    repo_status INT,
    user_id int NOT NULL,
    PRIMARY KEY (REPO_ID),
    FOREIGN KEY (user_id) REFERENCES users(ID)
)