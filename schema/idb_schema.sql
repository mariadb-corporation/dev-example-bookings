DROP DATABASE IF EXISTS travel;

CREATE DATABASE travel;

USE travel;

-- Create syntax for TABLE 'airlines'
CREATE TABLE airlines (
  iata_code CHAR(2) DEFAULT NULL,
  airline VARCHAR(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'airports'
CREATE TABLE airports (
  iata_code CHAR(3) DEFAULT NULL,
  airport VARCHAR(80) DEFAULT NULL,
  city VARCHAR(30) DEFAULT NULL,
  `state` CHAR(2) DEFAULT NULL,
  country VARCHAR(30) DEFAULT NULL,
  latitude FLOAT DEFAULT NULL,
  longitude FLOAT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'flights'
CREATE TABLE `flights` (
  `year` smallint(6) DEFAULT NULL,
  `month` tinyint(4) DEFAULT NULL,
  `day` tinyint(4) DEFAULT NULL,
  `day_of_week` tinyint(4) DEFAULT NULL,
  `fl_date` date DEFAULT NULL,
  `carrier` char(2) DEFAULT NULL,
  `tail_num` char(6) DEFAULT NULL,
  `fl_num` smallint(6) DEFAULT NULL,
  `origin` varchar(5) DEFAULT NULL,
  `dest` varchar(5) DEFAULT NULL,
  `crs_dep_time` char(4) DEFAULT NULL,
  `dep_time` char(4) DEFAULT NULL,
  `dep_delay` smallint(6) DEFAULT NULL,
  `taxi_out` smallint(6) DEFAULT NULL,
  `wheels_off` char(4) DEFAULT NULL,
  `wheels_on` char(4) DEFAULT NULL,
  `taxi_in` smallint(6) DEFAULT NULL,
  `crs_arr_time` char(4) DEFAULT NULL,
  `arr_time` char(4) DEFAULT NULL,
  `arr_delay` smallint(6) DEFAULT NULL,
  `cancelled` smallint(6) DEFAULT NULL,
  `cancellation_code` char(1) DEFAULT NULL,
  `diverted` smallint(6) DEFAULT NULL,
  `crs_elapsed_time` smallint(6) DEFAULT NULL,
  `actual_elapsed_time` smallint(6) DEFAULT NULL,
  `air_time` smallint(6) DEFAULT NULL,
  `distance` smallint(6) DEFAULT NULL,
  `carrier_delay` smallint(6) DEFAULT NULL,
  `weather_delay` smallint(6) DEFAULT NULL,
  `nas_delay` smallint(6) DEFAULT NULL,
  `security_delay` smallint(6) DEFAULT NULL,
  `late_aircraft_delay` smallint(6) DEFAULT NULL
) ENGINE=InnoDB;

-- Create syntax for TABLE 'tickets'
CREATE TABLE `tickets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `fl_date` date NOT NULL,
  `fl_num` smallint(6) NOT NULL,
  `carrier` char(2) NOT NULL DEFAULT '',
  `origin` varchar(5) NOT NULL DEFAULT '',
  `dest` varchar(5) NOT NULL DEFAULT '',
  `price` decimal(9,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'trips'
CREATE TABLE `trips` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ticket_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
