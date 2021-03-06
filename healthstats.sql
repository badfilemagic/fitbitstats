-- MySQL Script generated by MySQL Workbench
-- Sat Mar 24 16:25:52 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema healthstats
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `healthstats` ;

-- -----------------------------------------------------
-- Schema healthstats
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `healthstats` DEFAULT CHARACTER SET latin1 ;
USE `healthstats` ;

-- -----------------------------------------------------
-- Table `healthstats`.`body`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `healthstats`.`body` ;

CREATE TABLE IF NOT EXISTS `healthstats`.`body` (
  `days` DATE NOT NULL,
  `weight` FLOAT NULL DEFAULT NULL,
  `bmi` FLOAT NULL DEFAULT NULL,
  `fat` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`days`),
  UNIQUE INDEX `days_UNIQUE` (`days` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `healthstats`.`fbact`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `healthstats`.`fbact` ;

CREATE TABLE IF NOT EXISTS `healthstats`.`fbact` (
  `days` DATE NOT NULL,
  `calsburned` INT(11) NULL DEFAULT NULL,
  `steps` INT(11) NULL DEFAULT NULL,
  `distance` FLOAT NULL DEFAULT NULL,
  `floors` INT(11) NULL DEFAULT NULL,
  `ms` INT(11) NULL DEFAULT NULL,
  `mla` INT(11) NULL DEFAULT NULL,
  `mfa` INT(11) NULL DEFAULT NULL,
  `mva` INT(11) NULL DEFAULT NULL,
  `actcals` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`days`),
  UNIQUE INDEX `days_UNIQUE` (`days` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `healthstats`.`foodlog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `healthstats`.`foodlog` ;

CREATE TABLE IF NOT EXISTS `healthstats`.`foodlog` (
  `days` DATE NULL DEFAULT NULL,
  `meal` INT(11) NULL DEFAULT NULL,
  `food` VARCHAR(45) NULL DEFAULT NULL,
  `calories` INT(11) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `healthstats`.`meals`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `healthstats`.`meals` ;

CREATE TABLE IF NOT EXISTS `healthstats`.`meals` (
  `idmeals` INT(11) NOT NULL AUTO_INCREMENT,
  `mealname` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idmeals`),
  UNIQUE INDEX `idmeals_UNIQUE` (`idmeals` ASC),
  UNIQUE INDEX `mealname_UNIQUE` (`mealname` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `healthstats`.`nutrition`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `healthstats`.`nutrition` ;

CREATE TABLE IF NOT EXISTS `healthstats`.`nutrition` (
  `days` DATE NULL DEFAULT NULL,
  `calories` INT(11) NULL DEFAULT NULL,
  `fat` VARCHAR(10) NULL DEFAULT NULL,
  `fiber` VARCHAR(10) NULL DEFAULT NULL,
  `carbs` VARCHAR(10) NULL DEFAULT NULL,
  `sodium` VARCHAR(10) NULL DEFAULT NULL,
  `protein` VARCHAR(10) NULL DEFAULT NULL,
  `water` FLOAT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `healthstats`.`sleep`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `healthstats`.`sleep` ;

CREATE TABLE IF NOT EXISTS `healthstats`.`sleep` (
  `starttime` DATETIME NULL DEFAULT NULL,
  `endtime` DATETIME NULL DEFAULT NULL,
  `minsleep` INT(11) NULL DEFAULT NULL,
  `minwake` INT(11) NULL DEFAULT NULL,
  `numwakes` INT(11) NULL DEFAULT NULL,
  `minbed` INT(11) NULL DEFAULT NULL,
  `minrem` INT(11) NULL DEFAULT NULL,
  `minlight` INT(11) NULL DEFAULT NULL,
  `mindeep` INT(11) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
