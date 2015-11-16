SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `forumdb` ;
CREATE SCHEMA IF NOT EXISTS `forumdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `forumdb` ;

-- -----------------------------------------------------
-- Table `forumdb`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`User` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NULL,
  `email` VARCHAR(64) NOT NULL,
  `name` VARCHAR(64) NULL,
  `isAnonymous` TINYINT(1) NOT NULL DEFAULT FALSE,
  `about` TEXT NULL,
  PRIMARY KEY (`id`, `email`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `reverse` (`email` ASC, `id` ASC),
  UNIQUE INDEX `id_desc` (`id` DESC, `email` ASC),
  INDEX `reverse_desc` (`email` ASC, `id` DESC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Forum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`Forum` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`Forum` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(64) NOT NULL,
  `short_name` VARCHAR(128) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`, `name`, `short_name`),
  INDEX `fk_Forums_Users1_idx` (`user` ASC),
  UNIQUE INDEX `short_name_UNIQUE` (`short_name` ASC, `id` ASC),
  CONSTRAINT `fk_Forum_User1`
    FOREIGN KEY (`user`)
    REFERENCES `forumdb`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Follow`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`Follow` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`Follow` (
  `user` VARCHAR(64) NOT NULL,
  `follow` VARCHAR(64) NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`user`, `follow`),
  UNIQUE INDEX `userToFollowing` (`follow` ASC, `user` ASC),
  CONSTRAINT `fk_Follow_User_m`
    FOREIGN KEY (`user`)
    REFERENCES `forumdb`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Follow_User_m1`
    FOREIGN KEY (`follow`)
    REFERENCES `forumdb`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Thread`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`Thread` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`Thread` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(64) NOT NULL,
  `forum` VARCHAR(128) NOT NULL,
  `date` DATETIME NULL,
  `likes` INT NOT NULL DEFAULT 0,
  `dislikes` INT NOT NULL DEFAULT 0,
  `posts` INT NOT NULL DEFAULT 0,
  `message` TEXT NULL,
  `slug` VARCHAR(128) NOT NULL,
  `title` VARCHAR(128) NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL DEFAULT FALSE,
  `isClosed` TINYINT(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`id`, `user`, `forum`),
  INDEX `fk_Threads_Forums1_idx` (`forum` ASC),
  INDEX `fk_Threads_Users1_idx` (`user` ASC),
  INDEX `date_order` (`date` ASC, `id` ASC),
  INDEX `date_order_rev` (`date` DESC, `id` ASC),
  CONSTRAINT `fk_Thread_Forum1`
    FOREIGN KEY (`forum`)
    REFERENCES `forumdb`.`Forum` (`short_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Thread_User1`
    FOREIGN KEY (`user`)
    REFERENCES `forumdb`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Subscription`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`Subscription` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`Subscription` (
  `user` VARCHAR(64) NOT NULL,
  `thread_id` INT NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`user`, `thread_id`),
  INDEX `fk_Subscriprions_Users1_idx` (`user` ASC),
  INDEX `fk_Subscriprions_Threads1_idx` (`thread_id` ASC),
  UNIQUE INDEX `subscription` (`user` ASC, `thread_id` ASC),
  CONSTRAINT `fk_Subscription_User1`
    FOREIGN KEY (`user`)
    REFERENCES `forumdb`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Subscription_Thread1`
    FOREIGN KEY (`thread_id`)
    REFERENCES `forumdb`.`Thread` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`Post` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`Post` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `thread` INT NOT NULL,
  `user` VARCHAR(64) NOT NULL,
  `forum` VARCHAR(128) NOT NULL,
  `parent` INT NULL,
  `message` TEXT NOT NULL,
  `date` DATETIME NOT NULL,
  `likes` INT NOT NULL DEFAULT 0,
  `dislikes` INT NOT NULL DEFAULT 0,
  `isApproved` TINYINT(1) NULL,
  `isHighlighted` TINYINT(1) NULL,
  `isEdited` TINYINT(1) NULL,
  `isSpam` TINYINT(1) NULL,
  `isDeleted` TINYINT(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`id`, `thread`, `user`, `forum`),
  INDEX `fk_Posts_Threads1_idx` (`thread` ASC),
  INDEX `fk_Posts_Users1_idx` (`user` ASC),
  INDEX `fk_Posts_Posts1_idx` (`parent` ASC),
  INDEX `fk_Posts_Forums1_idx` (`forum` ASC),
  INDEX `date_ordering` (`date` DESC, `id` ASC),
  INDEX `date_order_rev` (`date` DESC, `id` ASC),
  CONSTRAINT `fk_Post_Thread1`
    FOREIGN KEY (`thread`)
    REFERENCES `forumdb`.`Thread` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Post_User1`
    FOREIGN KEY (`user`)
    REFERENCES `forumdb`.`User` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Post_Post1`
    FOREIGN KEY (`parent`)
    REFERENCES `forumdb`.`Post` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Post_Forum1`
    FOREIGN KEY (`forum`)
    REFERENCES `forumdb`.`Forum` (`short_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;