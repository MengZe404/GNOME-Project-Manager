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
    auto_refresh INT,
    PRIMARY KEY (ID)
);


CREATE TABLE repos (
    REPO_ID int NOT NULL,
    repo_name VARCHAR(255) NOT NULL,
    repo_url VARCHAR(255) NOT NULL,
    created_date VARCHAR(25) NOT NULL,
    repo_description VARCHAR(255),
    forks INT,
    repo_language VARCHAR(255),
    repo_status INT,
    user_id int NOT NULL,
    PRIMARY KEY (REPO_ID),
    FOREIGN KEY (user_id) REFERENCES users(ID)
);


CREATE TABLE ideas(
    IDEA_ID int NOT NULL,
    idea_name VARCHAR(255) NOT NULL,
    idea_language VARCHAR(255),
    idea_type VARCHAR(255),
    idea_audience VARCHAR(255),
    idea_feature VARCHAR(255),
    idea_detail VARCHAR(255),
    idea_date VARCHAR(25) NOT NULL,
    user_id int NOT NULL,
    PRIMARY KEY (IDEA_ID),
    FOREIGN KEY (user_id) REFERENCES users(ID)
);


CREATE TABLE projects(
    PROJECT_ID int NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    project_language VARCHAR(255),
    project_type VARCHAR(255),
    project_audience VARCHAR(255),
    project_feature VARCHAR(255),
    project_detail VARCHAR(255),
    project_url VARCHAR(255),
    project_date VARCHAR(25) NOT NULL,
    project_status INT,
    user_id int NOT NULL,
    repo_id int,
    PRIMARY KEY (PROJECT_ID),
    FOREIGN KEY (user_id) REFERENCES users(ID),
    FOREIGN KEY (repo_id) REFERENCES repos(REPO_ID)
);