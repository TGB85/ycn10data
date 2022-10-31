-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Gegenereerd op: 28 okt 2022 om 10:51
-- Serverversie: 10.4.25-MariaDB
-- PHP-versie: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coinmarketcap`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `crypto`
--

CREATE TABLE `crypto` (
  `id` int(11) NOT NULL,
  `Name` varchar(25) NOT NULL,
  `MarketCap` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Gegevens worden geëxporteerd voor tabel `crypto`
--

INSERT INTO `crypto` (`id`, `Name`, `MarketCap`) VALUES
(1, 'Bitcoin', '$385,657,914,032'),
(2, 'Ethereum', '$183,019,836,851'),
(3, 'Tether', '$68,893,532,459'),
(4, 'BNB', '$45,865,527,688'),
(5, 'USD Coin', '$43,909,620,805'),
(6, 'XRP', '$22,962,702,736'),
(7, 'Binance USD', '$21,571,769,797'),
(8, 'Cardano', '$13,098,829,185'),
(9, 'Solana', '$10,876,750,646'),
(10, 'Dogecoin', '$10,060,162,360');

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `crypto`
--
ALTER TABLE `crypto`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `crypto`
--
ALTER TABLE `crypto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
