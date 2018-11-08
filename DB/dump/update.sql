ALTER TABLE `quantcoin`.`strategy`
ADD COLUMN `coin_category` VARCHAR(45) NULL COMMENT '\'BTC,EOS,ETH\'' AFTER `method_name`,
ADD COLUMN `init_balance` DECIMAL(20,6) NULL COMMENT '初始化资金' AFTER `coin_category`,
ADD COLUMN `start_time` TIMESTAMP NULL COMMENT '开始时间' AFTER `init_balance`,
ADD COLUMN `end_time` TIMESTAMP NULL COMMENT '截止时间' AFTER `start_time`;


ALTER TABLE `quantcoin`.`strategy_conf_item`
CHANGE COLUMN `strategy_conf_id` `strategy_id` INT(11) NULL DEFAULT NULL ;