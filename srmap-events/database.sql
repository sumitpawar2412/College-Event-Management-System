-- Create Database
CREATE DATABASE IF NOT EXISTS srmap_events;
USE srmap_events;

-- =========================
-- 1. STUDENTS TABLE
-- =========================
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(50),
    INDEX(email)
);

-- =========================
-- 2. ADMINS TABLE
-- =========================
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- =========================
-- 3. VENUES TABLE
-- =========================
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    location VARCHAR(150),
    capacity INT
);

-- =========================
-- 4. ORGANIZERS TABLE
-- =========================
CREATE TABLE organizers (
    organizer_id INT AUTO_INCREMENT PRIMARY KEY,
    organizer_name VARCHAR(100) NOT NULL,
    contact VARCHAR(15),
    email VARCHAR(100)
);

-- =========================
-- 5. EVENTS TABLE
-- =========================
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue_id INT,
    organizer_id INT,
    capacity INT DEFAULT 100,

    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL,
    FOREIGN KEY (organizer_id) REFERENCES organizers(organizer_id) ON DELETE SET NULL,

    INDEX(event_date)
);

-- =========================
-- 6. REGISTRATIONS TABLE
-- =========================
CREATE TABLE registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,

    UNIQUE(student_id, event_id)
);

-- =========================
-- 7. NOTIFICATIONS TABLE
-- =========================
CREATE TABLE notifications (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 8. LOGIN ACTIVITY TABLE
-- =========================
CREATE TABLE login_activity (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NULL,
    admin_id INT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admins(admin_id) ON DELETE CASCADE
);