-- Create Category table if it does not already exist
CREATE TABLE IF NOT EXISTS Category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create Subcategory table with a foreign key relationship to Category
CREATE TABLE IF NOT EXISTS Subcategory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoryId INT,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (categoryId) REFERENCES Category(id) ON DELETE CASCADE
);

-- Create updated Complaint table without NOT NULL constraints on foreign keys
CREATE TABLE IF NOT EXISTS Complaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userComplaint TEXT NOT NULL,
    categoryId INT,
    subCategoryId INT,
    lastModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status TINYINT(1) DEFAULT 0,
    FOREIGN KEY (categoryId) REFERENCES Category(id) ON DELETE SET NULL,
    FOREIGN KEY (subCategoryId) REFERENCES Subcategory(id) ON DELETE SET NULL
);

-- Insert initial data into the Category table
INSERT INTO Category (name) VALUES
    ('Public Transit'),
    ('Parking'),
    ('Road Safety');

-- Insert initial data into the Subcategory table based on Category names
INSERT INTO Subcategory (categoryId, name)
VALUES
    -- Public Transit subcategories
    ((SELECT id FROM Category WHERE name = 'Public Transit'), 'Delays'),
    ((SELECT id FROM Category WHERE name = 'Public Transit'), 'Crowding'),
    ((SELECT id FROM Category WHERE name = 'Public Transit'), 'Fare'),
    ((SELECT id FROM Category WHERE name = 'Public Transit'), 'Accessibility'),
    ((SELECT id FROM Category WHERE name = 'Public Transit'), 'Cleanliness'),

    -- Parking subcategories
    ((SELECT id FROM Category WHERE name = 'Parking'), 'Availability'),
    ((SELECT id FROM Category WHERE name = 'Parking'), 'Pricing'),
    ((SELECT id FROM Category WHERE name = 'Parking'), 'Illegal Parking'),
    ((SELECT id FROM Category WHERE name = 'Parking'), 'Special Parking Needs'),

    -- Road Safety subcategories
    ((SELECT id FROM Category WHERE name = 'Road Safety'), 'Street Lighting'),
    ((SELECT id FROM Category WHERE name = 'Road Safety'), 'Pedestrian Crossings'),
    ((SELECT id FROM Category WHERE name = 'Road Safety'), 'Traffic Signs'),
    ((SELECT id FROM Category WHERE name = 'Road Safety'), 'Accident Hotspots'),
    ((SELECT id FROM Category WHERE name = 'Road Safety'), 'Speeding Zones');
