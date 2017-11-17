-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Nov 16, 2017 alle 16:32
-- Versione del server: 10.1.25-MariaDB
-- Versione PHP: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `billtomail`
--
CREATE DATABASE IF NOT EXISTS `billtomail` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `billtomail`;

-- --------------------------------------------------------

--
-- Struttura della tabella `bandiera`
--

CREATE TABLE `bandiera` (
  `id` int(1) NOT NULL,
  `inizio` varchar(10) NOT NULL,
  `fine` varchar(10) NOT NULL,
  `forzata` int(1) NOT NULL,
  `esecuzione` int(1) NOT NULL
  `tot_mail` int(5) NULL
  `errore` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `bandiera`
--

INSERT INTO `bandiera` (`id`, `inizio`, `fine`, `forzata`, `esecuzione`) VALUES
(1, '20171116', '0', 0, 0);

-- --------------------------------------------------------

--
-- Struttura della tabella `date`
--

CREATE TABLE `date` (
  `id` int(3) NOT NULL,
  `inizio` varchar(10) NOT NULL,
  `fine` varchar(10) NOT NULL,
  `forzata` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `date`
--

INSERT INTO `date` (`id`, `inizio`, `fine`, `forzata`) VALUES
(2, '2017-04-11', '2017-10-31', 0);

-- --------------------------------------------------------

--
-- Struttura della tabella `invio`
--

CREATE TABLE `invio` (
  `id` int(11) NOT NULL,
  `fattura` varchar(10) NOT NULL,
  `data` varchar(30) NOT NULL,
  `anno` varchar(4) NOT NULL,
  `cod_cliente` varchar(10) NOT NULL,
  `cod_cliente_invio` varchar(10) NOT NULL,
  `mail` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `bandiera`
--
ALTER TABLE `bandiera`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `date`
--
ALTER TABLE `date`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `invio`
--
ALTER TABLE `invio`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `bandiera`
--
ALTER TABLE `bandiera`
  MODIFY `id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT per la tabella `date`
--
ALTER TABLE `date`
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT per la tabella `invio`
--
ALTER TABLE `invio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



GRANT ALL PRIVILEGES ON `billtomail` . * TO 'billtomail'@'localhost' IDENTIFIED BY 'billtomail';
GRANT ALL PRIVILEGES ON `billtomail` . * TO 'billtomail'@'%' IDENTIFIED BY 'billtomail';
FLUSH PRIVILEGES;


