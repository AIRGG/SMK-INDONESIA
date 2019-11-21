/*
SQLyog Enterprise v12.5.1 (64 bit)
MySQL - 10.4.8-MariaDB : Database - smkindonesia
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`smkindonesia` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `smkindonesia`;

/*Table structure for table `guru` */

DROP TABLE IF EXISTS `guru`;

CREATE TABLE `guru` (
  `kode_guru` int(3) NOT NULL AUTO_INCREMENT,
  `nama` varchar(50) NOT NULL,
  `alamat` text NOT NULL,
  PRIMARY KEY (`kode_guru`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `guru` */

insert  into `guru`(`kode_guru`,`nama`,`alamat`) values 
(1,'Pak DikoQ','CiteureupA'),
(2,'Pak Hanan','Bogor'),
(3,'Bu Salsa','Bojong'),
(4,'Mr GG','Jauhh'),
(11,'asbdash','dbshbd');

/*Table structure for table `jadwal` */

DROP TABLE IF EXISTS `jadwal`;

CREATE TABLE `jadwal` (
  `id_jdwl` int(11) NOT NULL AUTO_INCREMENT,
  `id_mg` int(11) NOT NULL,
  `kode_kelas` int(11) NOT NULL,
  PRIMARY KEY (`id_jdwl`),
  KEY `id_mg` (`id_mg`),
  KEY `kode_kelas` (`kode_kelas`),
  CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`id_mg`) REFERENCES `mapel_guru` (`id_mg`),
  CONSTRAINT `jadwal_ibfk_2` FOREIGN KEY (`kode_kelas`) REFERENCES `kelas` (`kode_kelas`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `jadwal` */

insert  into `jadwal`(`id_jdwl`,`id_mg`,`kode_kelas`) values 
(4,1,1),
(5,3,2),
(6,2,3),
(8,3,3);

/*Table structure for table `kelas` */

DROP TABLE IF EXISTS `kelas`;

CREATE TABLE `kelas` (
  `kode_kelas` int(11) NOT NULL AUTO_INCREMENT,
  `kode_prodi` varchar(5) NOT NULL,
  `kelas` varchar(3) NOT NULL,
  `ket` varchar(1) NOT NULL,
  PRIMARY KEY (`kode_kelas`),
  KEY `kode_prodi` (`kode_prodi`),
  CONSTRAINT `kelas_ibfk_1` FOREIGN KEY (`kode_prodi`) REFERENCES `prodi` (`kode_prodi`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `kelas` */

insert  into `kelas`(`kode_kelas`,`kode_prodi`,`kelas`,`ket`) values 
(1,'RPL','X','1'),
(2,'RPL','X','2'),
(3,'MM','X','1');

/*Table structure for table `kelas_siswa` */

DROP TABLE IF EXISTS `kelas_siswa`;

CREATE TABLE `kelas_siswa` (
  `id_ks` int(11) NOT NULL AUTO_INCREMENT,
  `nis` varchar(10) NOT NULL,
  `kode_kelas` int(11) NOT NULL,
  PRIMARY KEY (`id_ks`),
  KEY `nis` (`nis`),
  KEY `kode_kelas` (`kode_kelas`),
  CONSTRAINT `kelas_siswa_ibfk_1` FOREIGN KEY (`nis`) REFERENCES `siswa` (`nis`),
  CONSTRAINT `kelas_siswa_ibfk_2` FOREIGN KEY (`kode_kelas`) REFERENCES `kelas` (`kode_kelas`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `kelas_siswa` */

insert  into `kelas_siswa`(`id_ks`,`nis`,`kode_kelas`) values 
(1,'1017007631',1),
(2,'1017007632',1);

/*Table structure for table `mapel` */

DROP TABLE IF EXISTS `mapel`;

CREATE TABLE `mapel` (
  `kode_mapel` varchar(5) NOT NULL,
  `nama_mapel` varchar(30) NOT NULL,
  PRIMARY KEY (`kode_mapel`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `mapel` */

insert  into `mapel`(`kode_mapel`,`nama_mapel`) values 
('BINDO','Bahasa Indonesia'),
('BING','Bahasa Inggris'),
('MTK','Matematika');

/*Table structure for table `mapel_guru` */

DROP TABLE IF EXISTS `mapel_guru`;

CREATE TABLE `mapel_guru` (
  `id_mg` int(11) NOT NULL AUTO_INCREMENT,
  `kode_mapel` varchar(5) NOT NULL,
  `kode_guru` int(3) NOT NULL,
  PRIMARY KEY (`id_mg`),
  KEY `kode_guru` (`kode_guru`),
  KEY `kode_mapel` (`kode_mapel`),
  CONSTRAINT `mapel_guru_ibfk_1` FOREIGN KEY (`kode_guru`) REFERENCES `guru` (`kode_guru`),
  CONSTRAINT `mapel_guru_ibfk_2` FOREIGN KEY (`kode_mapel`) REFERENCES `mapel` (`kode_mapel`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `mapel_guru` */

insert  into `mapel_guru`(`id_mg`,`kode_mapel`,`kode_guru`) values 
(1,'MTK',1),
(2,'BING',3),
(3,'BINDO',2);

/*Table structure for table `nilai` */

DROP TABLE IF EXISTS `nilai`;

CREATE TABLE `nilai` (
  `id_nilai` int(11) NOT NULL AUTO_INCREMENT,
  `id_mg` int(11) NOT NULL,
  `nis` varchar(10) NOT NULL,
  `uh` int(3) NOT NULL,
  `uts` int(3) NOT NULL,
  `uas` int(3) NOT NULL,
  `na` varchar(5) NOT NULL,
  PRIMARY KEY (`id_nilai`),
  KEY `id_mg` (`id_mg`),
  KEY `nis` (`nis`),
  CONSTRAINT `nilai_ibfk_1` FOREIGN KEY (`id_mg`) REFERENCES `mapel_guru` (`id_mg`),
  CONSTRAINT `nilai_ibfk_2` FOREIGN KEY (`nis`) REFERENCES `siswa` (`nis`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `nilai` */

insert  into `nilai`(`id_nilai`,`id_mg`,`nis`,`uh`,`uts`,`uas`,`na`) values 
(1,1,'1017007631',50,70,60,'60'),
(2,2,'1017007631',80,80,80,'80'),
(3,3,'1017007631',60,60,60,'60');

/*Table structure for table `prodi` */

DROP TABLE IF EXISTS `prodi`;

CREATE TABLE `prodi` (
  `kode_prodi` varchar(5) NOT NULL,
  `nama_prodi` text NOT NULL,
  PRIMARY KEY (`kode_prodi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `prodi` */

insert  into `prodi`(`kode_prodi`,`nama_prodi`) values 
('MM','Multimedia'),
('RPL','Rekayasa Perangkat Lunak'),
('TKJ','Teknik Komputer & Jaringan');

/*Table structure for table `siswa` */

DROP TABLE IF EXISTS `siswa`;

CREATE TABLE `siswa` (
  `nis` varchar(10) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `jk` varchar(1) DEFAULT NULL,
  `alamat` text NOT NULL,
  PRIMARY KEY (`nis`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `siswa` */

insert  into `siswa`(`nis`,`nama`,`jk`,`alamat`) values 
('1017007631','GG','l','cikaret'),
('1017007632','QQ','l','Bogor'),
('1017007633','Amanda','p','SUkahati'),
('1253621','dgasfdgSS','l','asdasdAA');

/*Table structure for table `userprofile` */

DROP TABLE IF EXISTS `userprofile`;

CREATE TABLE `userprofile` (
  `userid` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `level` int(1) DEFAULT NULL,
  `kode_guru` int(3) DEFAULT NULL,
  `nis` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `userprofile` */

insert  into `userprofile`(`userid`,`password`,`level`,`kode_guru`,`nis`) values 
('admin','123',1,NULL,NULL),
('dikoQ','1233',2,1,NULL),
('hanan','123',2,2,NULL),
('salsa','123',2,3,NULL),
('mrgg','123',2,4,NULL),
('gg','123',3,NULL,'1017007631'),
('qq','123',3,NULL,'1017007632'),
('manda','123',3,NULL,'1017007633'),
('saghd','hdgshgd',2,9,NULL),
('usermuridQ','dghsgd',3,NULL,'1253621'),
('baruu','123',2,11,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
