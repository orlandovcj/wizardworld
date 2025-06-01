-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           8.0.32 - MySQL Community Server - GPL
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Copiando estrutura para tabela wizardworld.battlefield
CREATE TABLE IF NOT EXISTS `battlefield` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `wallet` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `adventure` int DEFAULT NULL,
  `mission` int DEFAULT NULL,
  `level` int DEFAULT NULL,
  `round` int DEFAULT NULL,
  `magic` int DEFAULT NULL,
  `enemymp` int DEFAULT NULL,
  `bluepotions` int DEFAULT NULL,
  `redpotions` int DEFAULT NULL,
  `yellowpotions` int DEFAULT NULL,
  `purplepotions` int DEFAULT NULL,
  `invisible` int DEFAULT NULL,
  `updated` varchar(1) DEFAULT NULL,
  `nextmission` datetime DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL,
  `skart` decimal(20,8) DEFAULT NULL,
  `acum_skart` decimal(20,8) DEFAULT NULL,
  `last_reward` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=311 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='Mantém o inventário de itens dos jogadores';

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela wizardworld.inventory
CREATE TABLE IF NOT EXISTS `inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `wallet` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `asset` varchar(13) DEFAULT NULL,
  `tipo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `name_asset` varchar(300) DEFAULT NULL,
  `img` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `mp` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9750 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Mantém o inventário de itens dos jogadores';

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela wizardworld.userinfo
CREATE TABLE IF NOT EXISTS `userinfo` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) DEFAULT NULL,
  `chat_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cod`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela wizardworld.wizardsbattle
CREATE TABLE IF NOT EXISTS `wizardsbattle` (
  `id` varchar(50) DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `wallet` varchar(50) DEFAULT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `credit` int DEFAULT NULL,
  `terraforce` int DEFAULT NULL,
  `terracourage` int DEFAULT NULL,
  `terrahabil` int DEFAULT NULL,
  `terraintel` int DEFAULT NULL,
  `terraveloc` int DEFAULT NULL,
  `aguaforce` int DEFAULT NULL,
  `aguacourage` int DEFAULT NULL,
  `aguahabil` int DEFAULT NULL,
  `aguaintel` int DEFAULT NULL,
  `aguaveloc` int DEFAULT NULL,
  `fogoforce` int DEFAULT NULL,
  `fogocourage` int DEFAULT NULL,
  `fogohabil` int DEFAULT NULL,
  `fogointel` int DEFAULT NULL,
  `fogoveloc` int DEFAULT NULL,
  `arforce` int DEFAULT NULL,
  `arcourage` int DEFAULT NULL,
  `arhabil` int DEFAULT NULL,
  `arintel` int DEFAULT NULL,
  `arveloc` int DEFAULT NULL,
  `battleID` int DEFAULT NULL,
  `battleelement` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
