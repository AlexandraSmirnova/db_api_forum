


DROP SCHEMA IF EXISTS `forumdb2` ;

CREATE SCHEMA IF NOT EXISTS `forumdb2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;

USE `forumdb2` ;

-- -----------------------------------------------------
-- Table `forumdb`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb2`.`User` ;








CREATE TABLE IF NOT EXISTS `forumdb2`.`User` (
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
DROP TABLE IF EXISTS `forumdb2`.`Forum` ;

CREATE TABLE IF NOT EXISTS `forumdb2`.`Forum` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(64) NOT NULL,
  `short_name` VARCHAR(128) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`, `name`, `short_name`),
  INDEX `fk_Forums_Users1_idx` (`user` ASC),
  UNIQUE INDEX `short_name_UNIQUE` (`short_name` ASC, `id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Follow`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb2`.`Follow` ;

CREATE TABLE IF NOT EXISTS `forumdb2`.`Follow` (
  `user` VARCHAR(64) NOT NULL,
  `follow` VARCHAR(64) NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`user`, `follow`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Thread`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb2`.`Thread` ;

CREATE TABLE IF NOT EXISTS `forumdb2`.`Thread` (
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
  INDEX `date_order_rev` (`date` DESC, `id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`Subscription`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb2`.`Subscription` ;

CREATE TABLE IF NOT EXISTS `forumdb2`.`Subscription` (
  `user` VARCHAR(64) NOT NULL,
  `thread_id` INT NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`user`, `thread_id`),
  INDEX `fk_Subscriprions_Users1_idx` (`user` ASC),
  INDEX `fk_Subscriprions_Threads1_idx` (`thread_id` ASC),
  UNIQUE INDEX `subscription` (`user` ASC, `thread_id` ASC))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `forumdb`.`Post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb2`.`Post` ;

CREATE TABLE IF NOT EXISTS `forumdb2`.`Post` (
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
  INDEX `date_order_rev` (`date` DESC, `id` ASC))
ENGINE = InnoDB;
