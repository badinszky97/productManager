SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `consist`;
CREATE TABLE `consist` (
  `Container` int(11) NOT NULL,
  `Element` int(11) NOT NULL,
  `Pieces` int(10) UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

DROP TABLE IF EXISTS `elements`;
CREATE TABLE `elements` (
  `ID` int(11) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Type` int(11) NOT NULL,
  `Code` varchar(10) NOT NULL,
  `InStock` int(11) NOT NULL DEFAULT 0,
  `Icon` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

DROP TABLE IF EXISTS `element_types`;
CREATE TABLE `element_types` (
  `ID` int(11) NOT NULL,
  `Description` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

INSERT INTO `element_types` (`ID`, `Description`) VALUES
(1, 'Part'),
(2, 'Operation'),
(3, 'Assembly'),
(4, 'Product'),
(5, 'Project');

DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
  `ID` int(11) NOT NULL,
  `path` varchar(40) NOT NULL,
  `Description` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

DROP TABLE IF EXISTS `file_connects`;
CREATE TABLE `file_connects` (
  `file_id` int(11) NOT NULL,
  `element_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

DROP TABLE IF EXISTS `orderable`;
CREATE TABLE `orderable` (
  `VendorCode` int(11) NOT NULL,
  `ElementCode` int(11) NOT NULL,
  `orderCode` varchar(20) NOT NULL,
  `Price` float NOT NULL,
  `PriceUnit` int(11) NOT NULL,
  `link` text NOT NULL,
  `unit` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

DROP TABLE IF EXISTS `price_units`;
CREATE TABLE `price_units` (
  `ID` int(11) NOT NULL,
  `UnitType` varchar(10) NOT NULL,
  `ShortTerm` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

INSERT INTO `price_units` (`ID`, `UnitType`, `ShortTerm`) VALUES
(1, 'HUF', 'Ft'),
(2, 'EUR', '€'),
(3, 'USD', '$');

DROP TABLE IF EXISTS `vendors`;
CREATE TABLE `vendors` (
  `ID` int(11) NOT NULL,
  `Company` varchar(20) NOT NULL,
  `Address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;


ALTER TABLE `consist`
  ADD UNIQUE KEY `ContElementIndex` (`Container`,`Element`) USING BTREE,
  ADD KEY `consist_ibfk_2` (`Element`);

ALTER TABLE `elements`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `CodeUnique` (`Code`),
  ADD KEY `IconIndex` (`Icon`),
  ADD KEY `TypeIndex` (`Type`) USING BTREE;

ALTER TABLE `element_types`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `files`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `file_connects`
  ADD KEY `file_id_index` (`file_id`),
  ADD KEY `element_id_index` (`element_id`);

ALTER TABLE `orderable`
  ADD PRIMARY KEY (`VendorCode`,`ElementCode`),
  ADD KEY `VendorCodeIndex` (`VendorCode`),
  ADD KEY `ElementCodeIndex` (`ElementCode`),
  ADD KEY `PriceUnitIndex` (`PriceUnit`);

ALTER TABLE `price_units`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `vendors`
  ADD PRIMARY KEY (`ID`);


ALTER TABLE `elements`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `element_types`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `files`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `price_units`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `vendors`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `consist`
  ADD CONSTRAINT `consist_ibfk_1` FOREIGN KEY (`Container`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consist_ibfk_2` FOREIGN KEY (`Element`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `elements`
  ADD CONSTRAINT `elements_ibfk_1` FOREIGN KEY (`Type`) REFERENCES `element_types` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `elements_ibfk_2` FOREIGN KEY (`Icon`) REFERENCES `files` (`ID`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `file_connects`
  ADD CONSTRAINT `file_connects_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `files` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `file_connects_ibfk_2` FOREIGN KEY (`element_id`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `orderable`
  ADD CONSTRAINT `orderable_ibfk_1` FOREIGN KEY (`PriceUnit`) REFERENCES `price_units` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `orderable_ibfk_2` FOREIGN KEY (`VendorCode`) REFERENCES `vendors` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `orderable_ibfk_3` FOREIGN KEY (`ElementCode`) REFERENCES `elements` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;
