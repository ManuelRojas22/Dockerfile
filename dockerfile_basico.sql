-- ============================================================================
--  dockerfile_basico.sql
--  Sitio "Dockerize"  ·  Django 6 + MySQL 8
-- ----------------------------------------------------------------------------
--  Archivo único con TODA la base de datos "docker_basico":
--    · Sección 1 → creación de la base de datos
--    · Sección 2 → las 15 tablas (CREATE TABLE)
--    · Sección 3 → los datos de contenido (planes, características, equipo)
--
--  Este archivo NO incluye usuarios, perfiles, sesiones ni registros del
--  panel de administración. El primer usuario admin se crea con:
--      python manage.py createsuperuser
--
--  CÓMO IMPORTARLO
--    Opción 1 - línea de comandos:
--        mysql -u root -p < dockerfile_basico.sql
--
--    Opción 2 - phpMyAdmin:
--        Pestaña "Importar" → elige este archivo → "Continuir"
--
--    Opción 3 - MySQL Workbench:
--        Selecciona tu servidor → Schema → clic derecho → "Import SQL Script"
--
--    Opción 4 - contra el MySQL de Docker:
--        docker compose exec -T db mysql -uroot -proot < dockerfile_basico.sql
--
--  NOTA
--    Si tu servidor ya tiene una base con otro nombre, edita las dos líneas
--    CREATE DATABASE y USE de la sección 1.
--
--    Generado con mysqldump 8.0.43
-- ============================================================================


-- ============================================================================
--  SECCIÓN 1 · BASE DE DATOS
-- ============================================================================

CREATE DATABASE IF NOT EXISTS `docker_basico`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `docker_basico`;


-- ============================================================================
--  SECCIÓN 2 · ESTRUCTURA (15 TABLAS)
-- ============================================================================
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: docker_basico
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_contactmessage`
--

DROP TABLE IF EXISTS `core_contactmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_contactmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_plan`
--

DROP TABLE IF EXISTS `core_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_plan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` smallint unsigned NOT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tagline` varchar(140) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price_monthly` decimal(10,2) NOT NULL,
  `price_yearly` decimal(10,2) NOT NULL,
  `currency` varchar(4) COLLATE utf8mb4_unicode_ci NOT NULL,
  `badge` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  CONSTRAINT `core_plan_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_planfeature`
--

DROP TABLE IF EXISTS `core_planfeature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_planfeature` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` smallint unsigned NOT NULL,
  `title` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_highlighted` tinyint(1) NOT NULL,
  `plan_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_planfeature_plan_id_ec006ebb_fk_core_plan_id` (`plan_id`),
  CONSTRAINT `core_planfeature_plan_id_ec006ebb_fk_core_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `core_plan` (`id`),
  CONSTRAINT `core_planfeature_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_teammember`
--

DROP TABLE IF EXISTS `core_teammember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_teammember` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` smallint unsigned NOT NULL,
  `full_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `initials` varchar(4) COLLATE utf8mb4_unicode_ci NOT NULL,
  `linkedin_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `github_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `core_teammember_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-05 15:01:15
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: docker_basico
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `core_plan`
--

LOCK TABLES `core_plan` WRITE;
/*!40000 ALTER TABLE `core_plan` DISABLE KEYS */;
INSERT INTO `core_plan` VALUES (1,'2026-10-05 18:43:55.644531','2026-10-05 18:43:55.644627',1,1,'Hobby','hobby','Para aprender Docker sin tarjeta de credito.','Todo lo necesario para construir tus primeras imagenes y probarlas localmente.',0.00,0.00,'USD','Gratis',0),(2,'2026-10-05 18:43:55.665860','2026-10-05 18:43:55.665969',1,2,'Pro','pro','Para equipos que despliegan todas las semanas.','Registros privados, CI/CD con cache de capas y despliegue sin friccion.',29.00,290.00,'USD','Mas popular',1),(3,'2026-10-05 18:43:55.693372','2026-10-05 18:43:55.693455',1,3,'Enterprise','enterprise','Para organizaciones con requisitos de cumplimiento.','SSO, auditoria, alta disponibilidad y soporte dedicado con SLA.',99.00,990.00,'USD','Negocio',0);
/*!40000 ALTER TABLE `core_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `core_planfeature`
--

LOCK TABLES `core_planfeature` WRITE;
/*!40000 ALTER TABLE `core_planfeature` DISABLE KEYS */;
INSERT INTO `core_planfeature` VALUES (1,'2026-10-05 18:43:55.651710','2026-10-05 18:43:55.651765',1,1,'1 proyecto activo','',0,1),(2,'2026-10-05 18:43:55.653621','2026-10-05 18:43:55.653675',1,2,'Imagenes ilimitadas en builds locales','',0,1),(3,'2026-10-05 18:43:55.655476','2026-10-05 18:43:55.655565',1,3,'Docker Compose basico','',0,1),(4,'2026-10-05 18:43:55.657470','2026-10-05 18:43:55.657525',1,4,'Documentacion de inicio','',1,1),(5,'2026-10-05 18:43:55.659522','2026-10-05 18:43:55.659591',1,5,'Soporte por comunidad','',0,1),(6,'2026-10-05 18:43:55.672693','2026-10-05 18:43:55.672755',1,1,'10 proyectos activos','',1,2),(7,'2026-10-05 18:43:55.674598','2026-10-05 18:43:55.674653',1,2,'Registros privados con escaneo de imagenes','',1,2),(8,'2026-10-05 18:43:55.677953','2026-10-05 18:43:55.678030',1,3,'CI/CD con cache de capas','',1,2),(9,'2026-10-05 18:43:55.682279','2026-10-05 18:43:55.682453',1,4,'Despliegues ilimitados','',1,2),(10,'2026-10-05 18:43:55.685283','2026-10-05 18:43:55.685358',1,5,'Logs agregados por 30 dias','',1,2),(11,'2026-10-05 18:43:55.687263','2026-10-05 18:43:55.687322',1,6,'Soporte prioritario en 24h','',0,2),(12,'2026-10-05 18:43:55.699703','2026-10-05 18:43:55.699795',1,1,'Proyectos ilimitados','',1,3),(13,'2026-10-05 18:43:55.702996','2026-10-05 18:43:55.703067',1,2,'SSO SAML / OIDC y roles granulares','',1,3),(14,'2026-10-05 18:43:55.705462','2026-10-05 18:43:55.705533',1,3,'Registro de auditoria','',1,3),(15,'2026-10-05 18:43:55.707798','2026-10-05 18:43:55.707867',1,4,'Alta disponibilidad y DR','',1,3),(16,'2026-10-05 18:43:55.710041','2026-10-05 18:43:55.710117',1,5,'Cuenta dedicada y SLA 99.9%','',1,3),(17,'2026-10-05 18:43:55.711787','2026-10-05 18:43:55.711827',1,6,'Consultoria de arquitectura','',0,3);
/*!40000 ALTER TABLE `core_planfeature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `core_teammember`
--

LOCK TABLES `core_teammember` WRITE;
/*!40000 ALTER TABLE `core_teammember` DISABLE KEYS */;
INSERT INTO `core_teammember` VALUES (1,'2026-10-05 18:43:55.724059','2026-10-05 18:43:55.724120',1,1,'Laura Mendoza','Cofundadora / Backend','Dieciocho anos construyendo APIs. Escribe los servicios que sostienen este sitio.','LM','https://www.linkedin.com/','https://github.com/'),(2,'2026-10-05 18:43:55.731487','2026-10-05 18:43:55.731551',1,2,'Carlos Rincon','Cofundador / Plataforma','Automatiza pipelines y registries. Obsesionado con builds reproducibles.','CR','https://www.linkedin.com/','https://github.com/'),(3,'2026-10-05 18:43:55.739395','2026-10-05 18:43:55.739457',1,3,'Ana Torres','Frontend','Traduce ideas a interfaces. Cree en que el rendimiento tambien es diseno.','AT','https://www.linkedin.com/',''),(4,'2026-10-05 18:43:55.746480','2026-10-05 18:43:55.746564',1,4,'Diego Salinas','SRE','Guardia de produccion: alertas, metricas y despliegues sin sustos a las 3 AM.','DS','https://www.linkedin.com/','');
/*!40000 ALTER TABLE `core_teammember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-10-05 18:43:00.722186'),(2,'auth','0001_initial','2026-10-05 18:43:02.521354'),(3,'admin','0001_initial','2026-10-05 18:43:02.927010'),(4,'admin','0002_logentry_remove_auto_add','2026-10-05 18:43:02.954409'),(5,'admin','0003_logentry_add_action_flag_choices','2026-10-05 18:43:02.977981'),(6,'contenttypes','0002_remove_content_type_name','2026-10-05 18:43:03.438269'),(7,'auth','0002_alter_permission_name_max_length','2026-10-05 18:43:03.654273'),(8,'auth','0003_alter_user_email_max_length','2026-10-05 18:43:03.784869'),(9,'auth','0004_alter_user_username_opts','2026-10-05 18:43:03.814761'),(10,'auth','0005_alter_user_last_login_null','2026-10-05 18:43:03.988494'),(11,'auth','0006_require_contenttypes_0002','2026-10-05 18:43:03.996762'),(12,'auth','0007_alter_validators_add_error_messages','2026-10-05 18:43:04.026097'),(13,'auth','0008_alter_user_username_max_length','2026-10-05 18:43:04.255546'),(14,'auth','0009_alter_user_last_name_max_length','2026-10-05 18:43:04.466082'),(15,'auth','0010_alter_group_name_max_length','2026-10-05 18:43:04.523294'),(16,'auth','0011_update_proxy_permissions','2026-10-05 18:43:04.546345'),(17,'auth','0012_alter_user_first_name_max_length','2026-10-05 18:43:04.792814'),(18,'core','0001_initial','2026-10-05 18:43:05.119490'),(19,'sessions','0001_initial','2026-10-05 18:43:05.224171'),(20,'accounts','0001_initial','2026-10-05 18:52:17.408734');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (11,'accounts','profile'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'core','contactmessage'),(8,'core','plan'),(9,'core','planfeature'),(10,'core','teammember'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add mensaje de contacto',7,'add_contactmessage'),(26,'Can change mensaje de contacto',7,'change_contactmessage'),(27,'Can delete mensaje de contacto',7,'delete_contactmessage'),(28,'Can view mensaje de contacto',7,'view_contactmessage'),(29,'Can add plan',8,'add_plan'),(30,'Can change plan',8,'change_plan'),(31,'Can delete plan',8,'delete_plan'),(32,'Can view plan',8,'view_plan'),(33,'Can add integrante',10,'add_teammember'),(34,'Can change integrante',10,'change_teammember'),(35,'Can delete integrante',10,'delete_teammember'),(36,'Can view integrante',10,'view_teammember'),(37,'Can add caracteristica de plan',9,'add_planfeature'),(38,'Can change caracteristica de plan',9,'change_planfeature'),(39,'Can delete caracteristica de plan',9,'delete_planfeature'),(40,'Can view caracteristica de plan',9,'view_planfeature'),(41,'Can add perfil',11,'add_profile'),(42,'Can change perfil',11,'change_profile'),(43,'Can delete perfil',11,'delete_profile'),(44,'Can view perfil',11,'view_profile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-05 15:01:15


-- ============================================================================
--  SECCION 3 - DATOS DE CONTENIDO
-- ============================================================================
