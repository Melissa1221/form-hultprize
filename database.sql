CREATE DATABASE IF NOT EXISTS hult_prize_db;
USE hult_prize_db;

CREATE TABLE teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    startup_name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    university VARCHAR(255) NOT NULL,
    sdg VARCHAR(100) NOT NULL,
    hp_history TEXT,
    lead_source VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE team_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    member_type ENUM('captain', 'member2', 'member3', 'member4') NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    country VARCHAR(100),
    city VARCHAR(100),
    university VARCHAR(255),
    is_different_university BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (team_id) REFERENCES teams(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 