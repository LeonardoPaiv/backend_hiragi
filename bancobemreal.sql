-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: saco
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_arquivo`
--

DROP TABLE IF EXISTS `tb_arquivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_arquivo` (
  `idt_arquivo` int NOT NULL AUTO_INCREMENT,
  `nme_arquivo` varchar(75) NOT NULL,
  `arquivo` blob NOT NULL,
  `formato_arquivo` varchar(20) NOT NULL,
  `cod_ocorrencia` int NOT NULL,
  PRIMARY KEY (`idt_arquivo`),
  KEY `fk_tb_arquivo_tb_ocorrencias1_idx` (`cod_ocorrencia`),
  CONSTRAINT `fk_tb_arquivo_tb_ocorrencias1` FOREIGN KEY (`cod_ocorrencia`) REFERENCES `tb_ocorrencia` (`idt_ocorrencia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_arquivo`
--

LOCK TABLES `tb_arquivo` WRITE;
/*!40000 ALTER TABLE `tb_arquivo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_arquivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_atendimento`
--

DROP TABLE IF EXISTS `tb_atendimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_atendimento` (
  `idt_atendimento` int NOT NULL AUTO_INCREMENT,
  `cod_ocorrencia` int NOT NULL,
  `dsc_atendimento` varchar(300) NOT NULL,
  `cod_pessoa` int NOT NULL,
  `data_inicial_atendimento` datetime NOT NULL,
  `data_final_atendimento` datetime NOT NULL,
  PRIMARY KEY (`idt_atendimento`),
  KEY `fk_tb_ocorrencia_status_tb_ocorrencias1_idx` (`cod_ocorrencia`),
  KEY `fk_tb_atendimento_tb_pessoas1_idx` (`cod_pessoa`),
  CONSTRAINT `fk_tb_atendimento_tb_pessoas1` FOREIGN KEY (`cod_pessoa`) REFERENCES `tb_pessoa` (`idt_pessoa`),
  CONSTRAINT `fk_tb_ocorrencia_status_tb_ocorrencias1` FOREIGN KEY (`cod_ocorrencia`) REFERENCES `tb_ocorrencia` (`idt_ocorrencia`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_atendimento`
--

LOCK TABLES `tb_atendimento` WRITE;
/*!40000 ALTER TABLE `tb_atendimento` DISABLE KEYS */;
INSERT INTO `tb_atendimento` VALUES (1,6,'Lixo foi devidamente retirado da estrada',1,'2023-07-09 10:30:00','2023-07-09 11:00:00'),(2,8,'Foram postas novas tampas no bueiro',2,'2023-11-10 08:20:00','2023-11-10 13:30:00');
/*!40000 ALTER TABLE `tb_atendimento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_ocorrencia`
--

DROP TABLE IF EXISTS `tb_ocorrencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_ocorrencia` (
  `idt_ocorrencia` int NOT NULL AUTO_INCREMENT,
  `nme_ocorrencia` varchar(75) NOT NULL,
  `dsc_ocorrencia` varchar(300) NOT NULL,
  `data_ocorrencia` datetime NOT NULL,
  `cep_ocorrencia` varchar(8) NOT NULL,
  `cod_pessoa` int NOT NULL,
  `cod_tipo_ocorrencia` int NOT NULL,
  `cod_status_ocorrencia` int NOT NULL,
  `latitude_ocorrencia` varchar(45) DEFAULT NULL,
  `longitude_ocorrencia` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idt_ocorrencia`),
  KEY `fk_tb_ocorrencias_tb_pessoas_idx` (`cod_pessoa`),
  KEY `fk_tb_ocorrencias_tb_ocorrencias_tipos1_idx` (`cod_tipo_ocorrencia`),
  KEY `fk_tb_ocorrencias_tb_ocorrencias_status1_idx` (`cod_status_ocorrencia`),
  CONSTRAINT `fk_tb_ocorrencias_tb_ocorrencias_status1` FOREIGN KEY (`cod_status_ocorrencia`) REFERENCES `tb_status_ocorrencia` (`idt_status_ocorrencia`),
  CONSTRAINT `fk_tb_ocorrencias_tb_ocorrencias_tipos1` FOREIGN KEY (`cod_tipo_ocorrencia`) REFERENCES `tb_tipo_ocorrencia` (`idt_tipo_ocorrencia`),
  CONSTRAINT `fk_tb_ocorrencias_tb_pessoas` FOREIGN KEY (`cod_pessoa`) REFERENCES `tb_pessoa` (`idt_pessoa`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_ocorrencia`
--

LOCK TABLES `tb_ocorrencia` WRITE;
/*!40000 ALTER TABLE `tb_ocorrencia` DISABLE KEYS */;
INSERT INTO `tb_ocorrencia` VALUES (1,'Buraco na estrada','entracontrado um buraco na estrada','2023-11-26 12:20:33','71996450',3,2,1,NULL,NULL),(2,'Acidente de trânsito','carros colidiram entre si no meio da estrada','2023-08-04 06:47:50','72007580',9,8,1,NULL,NULL),(3,'Buraco na calçada','Pequenas fraturas encontradas na calçada','2022-09-25 15:10:10','72501406',18,7,1,NULL,NULL),(4,'Barulhos muito autos','Barulhos incomodam os vizinhos','2023-10-08 23:45:09','70878000',20,8,1,NULL,NULL),(5,'Show da Luiza Sonza','Show da Luiza Sonza','2023-06-30 18:30:00','72339041',5,8,1,NULL,NULL),(6,'Lixo na rua','lixo acumulado na rua','2023-07-09 10:00:00','73015124',19,1,3,NULL,NULL),(7,'Assalto','Assalto a mão armada acontecido recentemente','2023-11-28 22:34:38','72578480',7,3,2,NULL,NULL),(8,'Bueiro sem tampa','Bueiro da rua está sem tampa','2023-11-10 07:20:00','70680392',15,4,3,NULL,NULL),(9,'Placa batida','Carro bateu na placa e ela está torta','2023-11-07 15:46:55','71071216',4,5,2,NULL,NULL),(10,'Calsada esburacada','Calcada chiea de buracos','2023-10-09 10:30:44','72547203',10,7,2,NULL,NULL);
/*!40000 ALTER TABLE `tb_ocorrencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_pessoa`
--

DROP TABLE IF EXISTS `tb_pessoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_pessoa` (
  `idt_pessoa` int NOT NULL AUTO_INCREMENT,
  `nme_pessoa` varchar(100) NOT NULL,
  `cpf_pessoa` varchar(11) NOT NULL,
  `email_pessoa` varchar(100) NOT NULL,
  `senha_pessoa` varchar(100) NOT NULL,
  `tipo_pessoa` int NOT NULL,
  PRIMARY KEY (`idt_pessoa`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_pessoa`
--

LOCK TABLES `tb_pessoa` WRITE;
/*!40000 ALTER TABLE `tb_pessoa` DISABLE KEYS */;
INSERT INTO `tb_pessoa` VALUES (1,'Sophie Antonella Almeida','94088852010','sophieantonellaalmeida@danielvasconcelos.com.br','a83a112f9b2a4d29404b69d60f39c10199f496df',1),(2,'Nicole Sabrina Rebeca da Mata','98612823943','nicole_sabrina_damata@flextroniocs.copm.br','5095ee15e7d576e8d1b7a45695ad466b1a8d0d96',1),(3,'Benedito Benedito Matheus da Silva','23352542007','beneditobeneditodasilva@villalobos.mu.br','4de720eb4023c956af5f5931ad38591e7ff627fe',0),(4,'Malu Isabela Hadassa Assis','07962497840','maluisabelaassis@nokia.com','b5066df18c32cfc23876b2acbccb5baced98a5ce',0),(5,'Pietro Danilo Leandro Monteiro','21964901138','pietro_monteiro@dizain.com.br','f12aaf6a5c5b3267844cb15e221c035bb33d0765',0),(6,'Caroline Vera da Paz','54947961406','caroline_vera_dapaz@comercialrafael.com.br','56ee98dab26a0934196899b12c5dfa06bb389d0d',0),(7,'Rayssa Aparecida Marlene Cavalcanti','46607718906','rayssa_aparecida_cavalcanti@petrobrais.com.br','d871a36447dfb6f4b3584f653025c37877fe9a5c',0),(8,'Ester Silvana Nogueira','79877437201','ester.silvana.nogueira@focusdm.com.br','76f5c8ce4e0ecb58ace945b5c082c82d78ebf317',0),(9,'Miguel Paulo Campos','06077045004','miguel_campos@atualecomex.com.br','1eb2dd14a4233be4b362572bf4e14c2286fcc733',0),(10,'Milena Francisca Barros','32054174610','milena_francisca_barros@projetemovelaria.com.br','21b3659a23b4b041e9bedfb4f9f0b774beb70af5',0),(11,'Hadassa Isabel Aparício','64534548745','hadassa_isabel_aparicio@rotauniformes.com.br','6d6a9e55c57589893cdebbbf5b4a8d9a1a13d195',0),(12,'Ruan Lucas Melo','42212875193','ruan_melo@db9.com.br','fca0c8e10bec1180a2ab8c37473b21adbd61103d',0),(13,'Bruno André Hugo Souza','00684662850','bruno.andre.souza@dprf.gov.br','4cf9b3fa9926f462159c4667621d406746c32124',0),(14,'Cecília Lavínia Malu Silva','11320287107','cecilia.lavinia.silva@audiogeni.com.br','9863f298acc4f259bedbbec6dacff74357dac1fd',0),(15,'Vitor Fernando Pedro Rocha','50225634600','vitor.fernando.rocha@limao.com.br','c1d076cef53616472ba4376ef8e3ee1ff18a1da3',0),(16,'Mário Yago Araújo','63158509520','marioyagoaraujo@eguia.com.br','5b41ce34df7c5e23d48d39a97ca7042e4e7edd7b',0),(17,'Juan Gustavo Pedro Porto','04789899977','juangustavoporto@gmx.net','40632934700e7186269ee221608e53133bd8fed1',0),(18,'Henry Enrico Alves','97404165270','henry.enrico.alves@embraer.com','c6d1b59ae205afe663d0fff6ea9a1f829b6f040a',0),(19,'Isabel Aline Nunes','73956467035','isabel-nunes73@renovacao.com.br','34528b40b9c987fc93c654c64daa70f3250850cb',0),(20,'Levi Ruan Thomas Fogaça','26664833719','levi-fogaca83@ozzape.com','267527663f2c01a393b66e41d4da9cec03048924',0);
/*!40000 ALTER TABLE `tb_pessoa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_status_ocorrencia`
--

DROP TABLE IF EXISTS `tb_status_ocorrencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_status_ocorrencia` (
  `idt_status_ocorrencia` int NOT NULL AUTO_INCREMENT,
  `nme_status_ocorrencia` varchar(70) NOT NULL,
  PRIMARY KEY (`idt_status_ocorrencia`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_status_ocorrencia`
--

LOCK TABLES `tb_status_ocorrencia` WRITE;
/*!40000 ALTER TABLE `tb_status_ocorrencia` DISABLE KEYS */;
INSERT INTO `tb_status_ocorrencia` VALUES (1,'Criado'),(2,'Em Atendimento'),(3,'Finalizado'),(4,'Inativado');
/*!40000 ALTER TABLE `tb_status_ocorrencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_tipo_ocorrencia`
--

DROP TABLE IF EXISTS `tb_tipo_ocorrencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_tipo_ocorrencia` (
  `idt_tipo_ocorrencia` int NOT NULL AUTO_INCREMENT,
  `nme_tipo_ocorrencia` varchar(45) NOT NULL,
  PRIMARY KEY (`idt_tipo_ocorrencia`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_tipo_ocorrencia`
--

LOCK TABLES `tb_tipo_ocorrencia` WRITE;
/*!40000 ALTER TABLE `tb_tipo_ocorrencia` DISABLE KEYS */;
INSERT INTO `tb_tipo_ocorrencia` VALUES (1,'Lixo'),(2,'Buraco em pista'),(3,'Assalto'),(4,'Bueiro sem proteção'),(5,'Placa danificada'),(6,'Banco danificado'),(7,'Calçada danificada'),(8,'Outros');
/*!40000 ALTER TABLE `tb_tipo_ocorrencia` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-29 15:59:37
