-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 24, 2026 at 01:51 AM
-- Server version: 8.0.30
-- PHP Version: 8.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `presensi_polda`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` varchar(30) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `nama`, `email`, `password`) VALUES
('A001', 'Admin Utama', 'admin@mail.com', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `anggota`
--

CREATE TABLE `anggota` (
  `id_anggota` varchar(30) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `jabatan` varchar(50) DEFAULT NULL,
  `pangkat` varchar(50) DEFAULT NULL,
  `NRP` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `anggota`
--

INSERT INTO `anggota` (`id_anggota`, `nama`, `email`, `password`, `jabatan`, `pangkat`, `NRP`) VALUES
('A001', 'Saufi', 'Saufi@mail.com', 'Pegawai123', 'WAKAPOLDA', 'MAWAR 3', 1234);

-- --------------------------------------------------------

--
-- Table structure for table `absensi`
--

CREATE TABLE `absensi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_anggota` varchar(30) NOT NULL,
  `tanggal` datetime DEFAULT (now()),
  `waktu_masuk` datetime DEFAULT (now()),
  `status` varchar(20) NOT NULL,
  `keterangan` text,
  `foto` longtext,
  `tanda_tangan` longtext,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jabatan`
--

CREATE TABLE `jabatan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nama` (`nama`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jabatan`
--

INSERT INTO `jabatan` (`nama`) VALUES
('Kapolda'), ('Wakapolda'), ('Irwasda'), ('Karo Ops'), ('Karo SDM'), ('Karo Log'), ('Karo Rena'), 
('Dirintelkam'), ('Dirreskrimum'), ('Dirreskrimsus'), ('Dirresnarkoba'), ('Dirbinmas'), 
('Dirsamapta'), ('Dirlantas'), ('Dirpamobvit'), ('Dirpolairud'), ('Kabid Humas'), 
('Kabid Propam'), ('Kabid Kum'), ('Kabid TI'), ('Kabid Dokkes'), ('Kabid Keu'), 
('Dansat Brimob'), ('Kepala SPN');

-- --------------------------------------------------------

--
-- Table structure for table `pangkat`
--

CREATE TABLE `pangkat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nama` (`nama`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pangkat`
--

INSERT INTO `pangkat` (`nama`) VALUES
('Jenderal Polisi'), ('Komisaris Jenderal Polisi'), ('Inspektur Jenderal Polisi'), ('Brigadir Jenderal Polisi'),
('Komisaris Besar Polisi'), ('Ajun Komisaris Besar Polisi'), ('Komisaris Polisi'),
('Ajun Komisaris Polisi'), ('Inspektur Polisi Satu'), ('Inspektur Polisi Dua'),
('Ajun Inspektur Polisi Satu'), ('Ajun Inspektur Polisi Dua'),
('Brigadir Polisi Kepala'), ('Brigadir Polisi'), ('Brigadir Polisi Satu'), ('Brigadir Polisi Dua'),
('Ajun Brigadir Polisi'), ('Ajun Brigadir Polisi Satu'), ('Ajun Brigadir Polisi Dua'),
('Bhayangkara Kepala'), ('Bhayangkara Satu'), ('Bhayangkara Dua');

-- --------------------------------------------------------

--
-- Table structure for table `pengaturan`
--

CREATE TABLE `pengaturan` (
  `kunci` varchar(50) NOT NULL,
  `nilai` text NOT NULL,
  PRIMARY KEY (`kunci`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengaturan`
--

INSERT INTO `pengaturan` (`kunci`, `nilai`) VALUES
('jam_masuk_normal', '08:00'),
('jam_masuk_jumat', '07:30'),
('polda_lat', '-3.4883075'),
('polda_lon', '114.8307329'),
('geofence_radius', '200');

-- --------------------------------------------------------

--
-- Table structure for table `cuti`
--

CREATE TABLE `cuti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_anggota` varchar(30) NOT NULL,
  `tanggal_mulai` datetime NOT NULL,
  `tanggal_selesai` datetime NOT NULL,
  `jenis_cuti` varchar(50) NOT NULL,
  `keterangan` text,
  `status` varchar(20) DEFAULT 'Pending',
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `anggota`
--
ALTER TABLE `anggota`
  ADD PRIMARY KEY (`id_anggota`),
  ADD UNIQUE KEY `email` (`email`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

