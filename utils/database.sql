CREATE DATABASE IF NOT EXISTS wemech;

USE wemech;
-- Table for users
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Table for maintenance logs
CREATE TABLE IF NOT EXISTS MaintenanceLogs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    date_of_service DATE NOT NULL,
    type_of_service VARCHAR(255) NOT NULL,
    service_provider VARCHAR(255) NOT NULL,
    CONSTRAINT fk_plate_number
        FOREIGN KEY (plate_number)
        REFERENCES Users(plate_number)
        ON DELETE CASCADE
);
-- Sample Users
INSERT INTO Users (plate_number, username, email, password) VALUES
('ABC123', 'Ali Khan', 'ali.khan@example.com', 'password123'),
('XYZ456', 'Fatima Ahmed', 'fatima.ahmed@example.com', 'password456'),
('DEF789', 'Hassan Ali', 'hassan.ali@example.com', 'password789'),
('GHI101', 'Sana Khan', 'sana.khan@example.com', 'password101'),
('JKL112', 'Ahmed Mahmood', 'ahmed.mahmood@example.com', 'password112'),
('MNO123', 'Ayesha Malik', 'ayesha.malik@example.com', 'password123'),
('PQR456', 'Bilal Khan', 'bilal.khan@example.com', 'password456'),
('STU789', 'Zainab Khan', 'zainab.khan@example.com', 'password789'),
('VWX101', 'Imran Ali', 'imran.ali@example.com', 'password101'),
('YZA112', 'Nadia Mahmood', 'nadia.mahmood@example.com', 'password112'),
('BCD123', 'Saad Ahmed', 'saad.ahmed@example.com', 'password123'),
('EFG456', 'Amina Khan', 'amina.khan@example.com', 'password456'),
('HIJ789', 'Faisal Malik', 'faisal.malik@example.com', 'password789'),
('KLM101', 'Saima Ahmed', 'saima.ahmed@example.com', 'password101'),
('NOP112', 'Nabeel Khan', 'nabeel.khan@example.com', 'password112');


-- Sample Maintenance Logs
INSERT INTO MaintenanceLogs (plate_number, date_of_service, type_of_service, service_provider) VALUES
('ABC123', '2024-01-15', 'Oil Change', 'ABC Auto Service'),
('ABC123', '2024-03-20', 'Tire Rotation', 'ABC Auto Service'),
('XYZ456', '2024-02-10', 'Brake Inspection', 'XYZ Auto Care'),
('DEF789', '2024-04-05', 'Battery Replacement', 'DEF Auto Solutions'),
('GHI101', '2024-01-30', 'Oil Change', 'GHI Car Service'),
('JKL112', '2024-02-20', 'Wheel Alignment', 'JKL Motors'),
('ABC123', '2024-05-01', 'Engine Tune-up', 'ABC Auto Service'),
('XYZ456', '2024-03-10', 'Air Filter Replacement', 'XYZ Auto Care'),
('DEF789', '2024-05-02', 'Brake Pad Replacement', 'DEF Auto Solutions'),
('GHI101', '2024-04-20', 'Transmission Flush', 'GHI Car Service'),
('JKL112', '2024-03-15', 'Coolant Flush', 'JKL Motors'),
('ABC123', '2024-02-05', 'Wheel Balancing', 'ABC Auto Service'),
('XYZ456', '2024-01-20', 'Spark Plug Replacement', 'XYZ Auto Care'),
('DEF789', '2024-03-05', 'Oil Filter Change', 'DEF Auto Solutions'),
('GHI101', '2024-04-10', 'Radiator Flush', 'GHI Car Service');

SELECT * FROM MaintenanceLogs WHERE plate_number = 'ABC123';

SELECT * FROM MaintenanceLogs WHERE plate_number = 'ABC123' AND date_of_service BETWEEN '2024-01-01' AND '2024-12-31';

