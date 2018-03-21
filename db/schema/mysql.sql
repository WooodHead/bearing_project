DROP DATABASE IF EXISTS `bearing_project`;
CREATE DATABASE `bearing_project` /*!40100 DEFAULT CHARACTER SET utf8 */;


use bearing_project;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '姓名',
  `role_id` TINYINT NOT NULL DEFAULT 0 COMMENT '角色（0:默认,1:系统,2:销售,3:经理）',
  `parent_id` INT NOT NULL DEFAULT 0 COMMENT '上级用户ID',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户全局注册表';


DROP TABLE IF EXISTS `user_auth`;
CREATE TABLE `user_auth` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `type_auth` TINYINT NOT NULL DEFAULT 0 COMMENT '认证类型（0:账号,1:邮箱,2:手机,3:QQ,4:微信,5:微博）',
  `auth_key` VARCHAR(60) NOT NULL DEFAULT '' COMMENT '授权账号（账号;邮箱;手机;第三方登陆，这里是openid）',
  `auth_secret` VARCHAR(60) NOT NULL DEFAULT '' COMMENT '密码凭证（密码;token）',
  `status_verified` TINYINT NOT NULL DEFAULT 0 COMMENT '认证状态（0:未认证,1:已认证）',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`user_id`),
  UNIQUE (`type_auth`, `auth_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户认证表';


DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '角色名称（0:默认,1:系统,2:销售,3:经理）',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '角色备注',
  `section` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '版块权限(产品,客户,报价,统计,用户,角色,系统)',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限表';


DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `company_address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司地址',
  `company_site` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司官网',
  `company_tel` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司电话',
  `company_fax` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司传真',
  `company_type` TINYINT NOT NULL DEFAULT 0 COMMENT '公司类型（0:未知,1:中间商2:终端）',
  `owner_uid` INT NOT NULL DEFAULT 0 COMMENT '所属用户ID（未分配为0）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户表';


DROP TABLE IF EXISTS `customer_invoice`;
CREATE TABLE `customer_invoice` (
  `cid` INT NOT NULL,
  `company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `company_tax_id` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '单位税号',
  `company_address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '单位地址',
  `company_tel` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司电话',
  `company_bank_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '开户银行',
  `company_bank_account` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '银行账号',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户开票资料';


DROP TABLE IF EXISTS `customer_contact`;
CREATE TABLE `customer_contact` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cid` INT NOT NULL DEFAULT 0 COMMENT '客户ID',
  `name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '姓名',
  `salutation` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '称呼',
  `mobile` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '手机',
  `tel` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '座机（包含分机）',
  `fax` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '传真（包含分机）',
  `department` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '部门（采购、技术、销售、仓库、经理）',
  `address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '地址（办公地点、仓库地址）',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '备注',
  `status_default` TINYINT NOT NULL DEFAULT 0 COMMENT '默认状态（0:未默认,1:已默认）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户联系方式';


DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_brand` VARCHAR(16) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `product_model` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品型号',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '型号备注',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`product_model`),
  KEY (`product_brand`, `product_model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='产品明细';


DROP TABLE IF EXISTS `quote`;
CREATE TABLE `quote` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `contact_id` INT NOT NULL COMMENT '联系方式ID',
  `amount` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '订单总额',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '报价备注',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_order` TINYINT NOT NULL DEFAULT 0 COMMENT '订单状态（0:待下单,1:下单成功,2:下单失败）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `order_time` TIMESTAMP NULL COMMENT '下单时间（成功、失败）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='报价总表';


DROP TABLE IF EXISTS `quote_item`;
CREATE TABLE `quote_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quote_id` INT NOT NULL COMMENT '报价总表ID',
  `product_id` INT NOT NULL COMMENT '产品ID',
  `product_brand` VARCHAR(16) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `product_model` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品型号',
  `product_note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '型号备注',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '订单数量',
  `unit_price` DECIMAL(8, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`quote_id`),
  KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='报价明细';
