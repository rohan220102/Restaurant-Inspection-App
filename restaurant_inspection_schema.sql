-- Neil Bhutada


-- Table: establishment
CREATE TABLE establishment (
    license_no INTEGER PRIMARY KEY,
    dba_name TEXT,
    aka_name TEXT,
    facility_type TEXT,
    risk_level INTEGER,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    latitude REAL,
    longitude REAL,
    ward INTEGER
);

-- Table: employee
CREATE TABLE employee (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    phone TEXT,
    title TEXT,
    salary INTEGER,
    supervisor INTEGER
);

-- Table: inspection
CREATE TABLE inspection (
    inspection_id INTEGER PRIMARY KEY,
    inspection_date DATE,
    inspection_type TEXT,
    results TEXT,
    employee_id INTEGER,
    license_no INTEGER,
    followup_to INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (license_no) REFERENCES establishment(license_no)
);

-- Table: inspection_point
CREATE TABLE inspection_point (
    point_id TEXT PRIMARY KEY,
    Description TEXT,
    category TEXT,
    code TEXT,
    fine INTEGER,
    point_level TEXT
);

-- Table: violation
CREATE TABLE violation (
    inspection_id INTEGER,
    point_id TEXT,
    fine INTEGER,
    inspector_comment TEXT,
    PRIMARY KEY (inspection_id, point_id),
    FOREIGN KEY (inspection_id) REFERENCES inspection(inspection_id)
);

