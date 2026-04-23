CREATE DATABASE IF NOT EXISTS srmap_events;
USE srmap_events;

CREATE TABLE departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        ON DELETE SET NULL
);

CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE organizers (
    organizer_id INT AUTO_INCREMENT PRIMARY KEY,
    organizer_name VARCHAR(100) NOT NULL
);

CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue VARCHAR(100),
    organizer_id INT,
    capacity INT DEFAULT 100,
    FOREIGN KEY (organizer_id) REFERENCES organizers(organizer_id)
        ON DELETE SET NULL
);

CREATE TABLE registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
        ON DELETE CASCADE,
    UNIQUE(student_id, event_id)
);

CREATE TABLE notifications (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    event_id INT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
        ON DELETE SET NULL
);

CREATE TABLE login_activity (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NULL,
    admin_id INT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (student_id IS NOT NULL AND admin_id IS NULL) OR
        (student_id IS NULL AND admin_id IS NOT NULL)
    ),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
        ON DELETE CASCADE
);
