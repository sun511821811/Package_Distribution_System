from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(128) NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'operator',
    `is_active` BOOL NOT NULL DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `packages` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `description` LONGTEXT,
    `type` VARCHAR(20) NOT NULL,
    `current_version` VARCHAR(50) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending',
    `download_url` VARCHAR(500),
    `file_size` BIGINT,
    `sha256` VARCHAR(64),
    `r2_original_path` VARCHAR(500),
    `r2_processed_path` VARCHAR(500),
    `is_distributing` BOOL NOT NULL DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    KEY `idx_packages_name_70b14c` (`name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `original_package_history` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(50) NOT NULL,
    `file_name` VARCHAR(255) NOT NULL,
    `file_size` BIGINT NOT NULL,
    `sha256` VARCHAR(64) NOT NULL,
    `r2_path` VARCHAR(500) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `package_id` INT NOT NULL,
    `uploaded_by_id` INT,
    CONSTRAINT `fk_original_packages_5893747c` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_original_users_078f71d3` FOREIGN KEY (`uploaded_by_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `process_tasks` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `task_id` VARCHAR(50) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending',
    `result_message` LONGTEXT,
    `retry_count` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `original_package_history_id` INT,
    `package_id` INT NOT NULL,
    CONSTRAINT `fk_process__original_a377521e` FOREIGN KEY (`original_package_history_id`) REFERENCES `original_package_history` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_process__packages_6c0f89f2` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE,
    KEY `idx_process_tas_task_id_d0c7d7` (`task_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `operation_logs` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50),
    `action` VARCHAR(50) NOT NULL,
    `target_type` VARCHAR(50) NOT NULL,
    `target_id` VARCHAR(50),
    `details` LONGTEXT,
    `ip_address` VARCHAR(50),
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT,
    CONSTRAINT `fk_operatio_users_53930007` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
