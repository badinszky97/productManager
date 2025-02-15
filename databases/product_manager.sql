-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Dec 28, 2024 at 02:13 PM
-- Server version: 11.6.2-MariaDB-ubu2404
-- PHP Version: 8.2.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `product_manager`
--

-- --------------------------------------------------------

--
-- Table structure for table `consist`
--

CREATE TABLE `consist` (
  `Container` int(11) NOT NULL,
  `Element` int(11) NOT NULL,
  `Pieces` int(10) UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `elements`
--

CREATE TABLE `elements` (
  `ID` int(11) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Type` int(11) NOT NULL,
  `Code` varchar(10) NOT NULL,
  `Icon` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
-- --------------------------------------------------------

--
-- Table structure for table `element_types`
--

CREATE TABLE `element_types` (
  `ID` int(11) NOT NULL,
  `Description` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `element_types`
--

INSERT INTO `element_types` (`ID`, `Description`) VALUES
(1, 'Part'),
(2, 'Operation'),
(3, 'Assembly'),
(4, 'Product'),
(5, 'Project');

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `ID` int(11) NOT NULL,
  `path` varchar(40) NOT NULL,
  `Description` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `file_connects`
--

CREATE TABLE `file_connects` (
  `file_id` int(11) NOT NULL,
  `element_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orderable`
--

CREATE TABLE `orderable` (
  `VendorCode` int(11) NOT NULL,
  `ElementCode` int(11) NOT NULL,
  `orderCode` varchar(20) NOT NULL,
  `Price` float NOT NULL,
  `PriceUnit` int(11) NOT NULL,
  `link` text NOT NULL,
  `unit` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `price_units`
--

CREATE TABLE `price_units` (
  `ID` int(11) NOT NULL,
  `UnitType` varchar(10) NOT NULL,
  `ShortTerm` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `price_units`
--

INSERT INTO `price_units` (`ID`, `UnitType`, `ShortTerm`) VALUES
(1, 'HUF', 'Ft'),
(2, 'EUR', '€'),
(3, 'USD', '$');

-- --------------------------------------------------------

--
-- Table structure for table `vendors`
--

CREATE TABLE `vendors` (
  `ID` int(11) NOT NULL,
  `Company` varchar(20) NOT NULL,
  `Address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;


--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
  `ID` int(11) NOT NULL,
  `element_id` int(11) NOT NULL,
  `pieces` int(11) NOT NULL DEFAULT 0,
  `description` varchar(15) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;


--
-- Indexes for dumped tables
--

--
-- Indexes for table `consist`
--
ALTER TABLE `consist`
  ADD UNIQUE KEY `ContElementIndex` (`Container`,`Element`) USING BTREE,
  ADD KEY `consist_ibfk_2` (`Element`);

--
-- Indexes for table `elements`
--
ALTER TABLE `elements`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `CodeUnique` (`Code`),
  ADD KEY `IconIndex` (`Icon`),
  ADD KEY `TypeIndex` (`Type`) USING BTREE;

--
-- Indexes for table `element_types`
--
ALTER TABLE `element_types`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `file_connects`
--
ALTER TABLE `file_connects`
  ADD KEY `file_id_index` (`file_id`),
  ADD KEY `element_id_index` (`element_id`);

--
-- Indexes for table `orderable`
--
ALTER TABLE `orderable`
  ADD PRIMARY KEY (`VendorCode`,`ElementCode`),
  ADD KEY `VendorCodeIndex` (`VendorCode`),
  ADD KEY `ElementCodeIndex` (`ElementCode`),
  ADD KEY `PriceUnitIndex` (`PriceUnit`);

--
-- Indexes for table `price_units`
--
ALTER TABLE `price_units`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `vendors`
--
ALTER TABLE `vendors`
  ADD PRIMARY KEY (`ID`);


--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `element_id_key` (`element_id`);


--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `elements`
--
ALTER TABLE `elements`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `element_types`
--
ALTER TABLE `element_types`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `price_units`
--
ALTER TABLE `price_units`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `vendors`
--
ALTER TABLE `vendors`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `consist`
--
ALTER TABLE `consist`
  ADD CONSTRAINT `consist_ibfk_1` FOREIGN KEY (`Container`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consist_ibfk_2` FOREIGN KEY (`Element`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `elements`
--
ALTER TABLE `elements`
  ADD CONSTRAINT `elements_ibfk_1` FOREIGN KEY (`Type`) REFERENCES `element_types` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `elements_ibfk_2` FOREIGN KEY (`Icon`) REFERENCES `files` (`ID`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `file_connects`
--
ALTER TABLE `file_connects`
  ADD CONSTRAINT `file_connects_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `files` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `file_connects_ibfk_2` FOREIGN KEY (`element_id`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orderable`
--
ALTER TABLE `orderable`
  ADD CONSTRAINT `orderable_ibfk_1` FOREIGN KEY (`PriceUnit`) REFERENCES `price_units` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `orderable_ibfk_2` FOREIGN KEY (`VendorCode`) REFERENCES `vendors` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `orderable_ibfk_3` FOREIGN KEY (`ElementCode`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `element_id_key` FOREIGN KEY (`element_id`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
