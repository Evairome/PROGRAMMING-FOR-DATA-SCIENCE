-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pollution-db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pollution-db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pollution-db` DEFAULT CHARACTER SET utf8 ;
USE `pollution-db` ;

-- -----------------------------------------------------
-- Table `pollution-db`.`schema_sql`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution-db`.`schema_sql` (
  `measure` VARCHAR(100) NOT NULL,
  `description` VARCHAR(150) NULL,
  `unit` VARCHAR(40) NULL,
  PRIMARY KEY (`measure`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution-db`.`site`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution-db`.`site` (
  `siteid` MEDIUMINT(45) NOT NULL,
  `location` VARCHAR(50) NULL,
  `geo_point_2d` VARCHAR(60) NULL,
  PRIMARY KEY (`siteid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution-db`.`reading`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution-db`.`reading` (
  `reading_id` INT NOT NULL AUTO_INCREMENT,
  `date_time` DATETIME NULL,
  `nox` FLOAT NULL,
  `no2` FLOAT NULL,
  `no` FLOAT NULL,
  `siteid` MEDIUMINT(45) NOT NULL,
  `pm10` FLOAT NULL,
  `nvpm10` FLOAT NULL,
  `vpm10` FLOAT NULL,
  `nvpm2.5` FLOAT NULL,
  `pm2.5` FLOAT NULL,
  `vpm2.5` FLOAT NULL,
  `co` FLOAT NULL,
  `o3` FLOAT NULL,
  `so2` FLOAT NULL,
  `temperature` FLOAT NULL,
  `rh` FLOAT NULL,
  `air_pressure` FLOAT NULL,
  `datestart` DATETIME NULL,
  `dateend` DATETIME NULL,
  `current` TINYINT NULL,
  `instrument type` VARCHAR(100) NULL,
  PRIMARY KEY (`reading_id`, `siteid`),
  INDEX `siteid_idx` (`siteid` ASC),
  CONSTRAINT `siteid`
    FOREIGN KEY (`siteid`)
    REFERENCES `pollution-db`.`site` (`siteid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
