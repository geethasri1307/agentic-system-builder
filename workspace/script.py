# Continuing the database design...

-- Completing SUBJECTS table
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Teacher-Subject Assignment Table
CREATE TABLE teacher_subject (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id    INT NOT NULL,
    subject_id    INT NOT NULL,
    class_id      INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,  -- e.g., "2024-25"
    semester      INT NOT NULL,
    assigned_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active     BOOLEAN DEFAULT TRUE,
    UNIQUE KEY unique_assignment (teacher_id, subject_id, class_id, academic_year, semester),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- ENROLLMENTS Table (Student-Class-Subject mapping)
CREATE TABLE enrollments (
    enroll_id     INT AUTO_INCREMENT PRIMARY KEY,
    student_id    INT NOT NULL,
    class_id      INT NOT NULL,
    subject_id    INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    semester      INT NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    status        ENUM('active','completed','dropped') DEFAULT 'active',
    final_grade   VARCHAR(2),
    UNIQUE KEY unique_enrollment (student_id, class_id, subject_id, academic_year, semester),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- MARKS Table
CREATE TABLE marks (
    mark_id       INT AUTO_INCREMENT PRIMARY KEY,
    student_id    INT NOT NULL,
    subject_id    INT NOT NULL,
    class_id      INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    semester      INT NOT NULL,
    exam_type     ENUM('midterm','final','quiz','assignment',' practical') NOT NULL,
    marks_obtained DECIMAL(5,2) NOT NULL,
    max_marks     DECIMAL(5,2) NOT NULL,
    grade         VARCHAR(2),
    attendance_percentage DECIMAL(5,2),
    entered_by    INT NOT NULL,  -- teacher_id or admin_id
    entered_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_mark_record (student_id, subject_id, exam_type, academic_year, semester),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (entered_by) REFERENCES users(user_id),
    INDEX idx_student_subject (student_id, subject_id),
    INDEX idx_exam_type (exam_type)
);

-- ATTENDANCE Table
CREATE TABLE attendance (
    att_id        INT AUTO_INCREMENT PRIMARY KEY,
    student_id    INT NOT NULL,
    subject_id    INT NOT NULL,
    class_id      INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    semester      INT NOT NULL,
    date          DATE NOT NULL,
    status        ENUM('present','absent','late','excused') NOT NULL,
    marked_by     INT NOT NULL,  -- teacher_id
    marked_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_attendance_record (student_id, subject_id, date),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (marked_by) REFERENCES teachers(teacher_id),
    INDEX idx_student_subject_date (student_id, subject_id, date),
    INDEX idx_date (date)
);

-- NOTICES Table
CREATE TABLE notices (
    notice_id     INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(100) NOT NULL,
    content       TEXT NOT NULL,
    category      ENUM('general','academic','event','alert') DEFAULT 'general',
    target_role   ENUM('student','teacher','admin','all') DEFAULT 'all',
    target_class  INT,  -- NULL for all classes
    target_year   VARCHAR(9),  -- NULL for all years
    posted_by     INT NOT NULL,
    posted_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at    TIMESTAMP NULL,
    is_active     BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (posted_by) REFERENCES users(user_id),
    INDEX idx_category (category),
    INDEX idx_target_role (target_role),
    INDEX idx_active (is_active, expires_at)
);

-- GRADES Scale Table (for reference)
CREATE TABLE grade_scale (
    grade VARCHAR(2) PRIMARY KEY,
    min_percentage DECIMAL(5,2) NOT NULL,
    max_percentage DECIMAL(5,2) NOT NULL,
    description VARCHAR(100)
);

-- INSERT SAMPLE GRADES
INSERT INTO grade_scale VALUES
('A+', 90.00, 100.00, 'Excellent'),
('A', 80.00, 89.99, 'Very Good'),
('B+', 70.00, 79.99, 'Good'),
('B', 60.00, 69.99, 'Above Average'),
('C+', 50.00, 59.99, 'Average'),
('C', 40.00, 49.99, 'Pass'),
('F', 0.00, 39.99, 'Fail');

-- CLASSES Table (for completeness)
CREATE TABLE classes (
    class_id      INT AUTO_INCREMENT PRIMARY KEY,
    class_name    VARCHAR(50) NOT NULL,  -- e.g., "BCA Semester 2"
    dept_id       INT NOT NULL,
    semester      INT NOT NULL,
    section       VARCHAR(5) NOT NULL,  -- e.g., "A", "B"
    academic_year VARCHAR(9) NOT NULL,
    strength      INT DEFAULT 0,  -- Current student count
    capacity      INT NOT NULL,
    coordinator   INT,  -- Teacher ID
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
    FOREIGN KEY (coordinator) REFERENCES teachers(teacher_id),
    UNIQUE KEY unique_class (class_name, section, academic_year),
    INDEX idx_dept_sem (dept_id, semester)
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX idx_user_role ON users(role);
CREATE INDEX idx_student_dept ON students(dept_id);
CREATE INDEX idx_teacher_dept ON teachers(dept_id);
CREATE INDEX idx_enroll_student ON enrollments(student_id);
CREATE INDEX idx_marks_student ON marks(student_id);
CREATE INDEX idx_attendance_student ON attendance(student_id);