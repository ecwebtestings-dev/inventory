-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2026 at 08:28 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `category` varchar(50) NOT NULL,
  `supplier` varchar(100) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL CHECK (`unit_price` >= 0),
  `quantity_in_stock` int(11) NOT NULL DEFAULT 0 CHECK (`quantity_in_stock` >= 0),
  `reorder_level` int(11) NOT NULL DEFAULT 0 CHECK (`reorder_level` >= 0),
  `date_added` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `category`, `supplier`, `unit_price`, `quantity_in_stock`, `reorder_level`, `date_added`) VALUES
(2, 'Electronics', 'Groceries', 'Mukwano', 15000.00, 6, 10, '2026-11-03'),
(3, 'Exercise Book', 'Stationery', 'Aristoc', 1200.00, 120, 30, '2026-11-03'),
(4, 'Keyboards', 'Hp', 'Mink technologies Kampala', 25000.00, 20, 5, '2026-11-03'),
(5, 'Perfumes', 'Ladies fumes', 'Banks', 15000.00, 20, 20, '2026-11-03'),
(12, 'Humidifers', '30Mhz', 'Nike', 40000.00, 20, 5, '2026-11-03'),
(13, 'RAM', 'Electronics', 'Liberty Computers', 50000.00, 200, 50, '2026-11-05'),
(14, 'Wireless Mouse', 'Electronics', 'Tech Supplies Uganda', 25000.00, 35, 10, '2026-11-05'),
(15, 'USB Flash Drive 32GB', 'Electronics', 'Digital World Ltd', 18000.00, 50, 15, '2026-11-05'),
(16, 'Keyboard', 'Electronics', 'Tech Supplies Uganda', 35000.00, 20, 5, '2026-11-05'),
(17, 'Bluetooth Speaker', 'Electronics', 'SoundTech Uganda', 65000.00, 8, 10, '2026-11-05'),
(18, 'USB Charger', 'Electronics', 'Electro Hub Uganda', 20000.00, 40, 10, '2026-11-05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
