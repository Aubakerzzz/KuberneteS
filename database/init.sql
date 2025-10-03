CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    price FLOAT NOT NULL,
    date DATE NOT NULL
);

-- AAPL dummy data
INSERT INTO stocks (ticker, price, date) VALUES
('AAPL', 180, '2025-09-28'),
('AAPL', 182, '2025-09-29'),
('AAPL', 178, '2025-09-30'),
('AAPL', 185, '2025-10-01'),
('AAPL', 190, '2025-10-02');

-- MSFT dummy data
INSERT INTO stocks (ticker, price, date) VALUES
('MSFT', 300, '2025-09-28'),
('MSFT', 305, '2025-09-29'),
('MSFT', 310, '2025-09-30'),
('MSFT', 295, '2025-10-01'),
('MSFT', 298, '2025-10-02');
