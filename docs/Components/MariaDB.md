# MariaDB


## 事务

一般来说，事务是必须满足4个条件（ACID）：
1. 原子性（Atomicity，或称不可分割性）
2. 一致性（Consistency）
3. 隔离性（Isolation，又称独立性）
4. 持久性（Durability）


- **原子性**：一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。

- **一致性**：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度、串联性以及后续数据库可以自发性地完成预定的工作。

- **隔离性**：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。

- **持久性**：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。


## 测试 “幻读”（phantom read）

因高并发场景下, 会出现同一时刻交叉多个事务的情况, 接下来通过2个例子的模拟, 观察一下对数据库及业务产生的影响

准备测试数据表
```
MariaDB [flask_restful]> DROP TABLE IF EXISTS `t_products`;
CREATE TABLE `t_products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL DEFAULT '' COMMENT 'product name',
  `num` INT NOT NULL DEFAULT '0' COMMENT 'stock num',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='stock table';
MariaDB [flask_restful]> select @@global.tx_isolation, @@tx_isolation;
+-----------------------+-----------------+
| @@global.tx_isolation | @@tx_isolation  |
+-----------------------+-----------------+
| REPEATABLE-READ       | REPEATABLE-READ |
+-----------------------+-----------------+
```
InnoDB事务的隔离级别有四级，默认是“可重复读”（REPEATABLE READ）


1. 插入库存（不存在则插入）
```
T Session A                                     Session B
|
| START TRANSACTION;                            START TRANSACTION;
|
| SELECT * FROM t_products WHERE name='a';
| empty set
|                                               INSERT INTO t_products (`name`, `num`) VALUES ('a', 5);
|
| SELECT * FROM t_products;                     SELECT * FROM t_products WHERE name='a';
| empty set                                     +----+------+-----+
|                                               | id | name | num |
|                                               +----+------+-----+
|                                               |  1 | a    |   5 |
|                                               +----+------+-----+
|
|                                               COMMIT;
|
| SELECT * FROM t_products WHERE name='a';
| empty set
|
| INSERT INTO t_products (`name`, `num`) VALUES ('a', 5);
| ERROR 1062 (23000): Duplicate entry 'a' for key 'uk_name'
-
```
虽然因幻读导致数据库级别插入异常, 但是异常回滚不会影响业务


2. 抢购秒杀（库存存在则扣除库存数量）

假定库存为1
```
MariaDB [flask_restful]> UPDATE t_products SET num=1;
```

模拟2个用户同时抢购
```
T Session A                                         Session B
|
| START TRANSACTION;                                START TRANSACTION;
|
| SELECT num FROM t_products WHERE id=1;            SELECT num FROM t_products WHERE id=1;
| +-----+                                           +-----+
| | num |                                           | num |
| +-----+                                           +-----+
| |   1 |                                           |   1 |
| +-----+                                           +-----+
|
| UPDATE t_products SET num=num-1 WHERE id=1 and num>0;
|
| SELECT num FROM t_products WHERE id=1;            SELECT num FROM t_products WHERE id=1;
| +-----+                                           +-----+
| | num |                                           | num |
| +-----+                                           +-----+
| |   0 |                                           |   1 |
| +-----+                                           +-----+
|
| COMMIT;
|
|                                                   SELECT num FROM t_products WHERE id=1;
|                                                   +-----+
|                                                   | num |
|                                                   +-----+
|                                                   |   1 |
|                                                   +-----+
|
|                                                   UPDATE t_products SET num=num-1 WHERE id=1 and num>0;
|
|                                                   SELECT num FROM t_products WHERE id=1;
|                                                   +-----+
|                                                   | num |
|                                                   +-----+
|                                                   |  -1 |
|                                                   +-----+
|
|                                                   COMMIT;
|
-
```
因幻读, 并没有导致数据库更新异常, 但是出现了库存超卖的现象, 即业务层面的异常

如何避免, 通过悲观锁（FOR UPDATE）方式处理:
```
MariaDB [flask_restful]> UPDATE t_products SET num=1;

T Session A                                         Session B
|
| START TRANSACTION;                                START TRANSACTION;
|
| SELECT num FROM t_products WHERE id=1 FOR UPDATE;
| +-----+
| | num |
| +-----+
| |   1 |
| +-----+
|
|                                                   SELECT num FROM t_products WHERE id=1 FOR UPDATE;
|                                                   等待...直到超时, 当其他事物提交返回更新后的结果
|
| UPDATE t_products SET num=num-1 WHERE id=1 and num>0;
|
| SELECT num FROM t_products WHERE id=1;
| +-----+
| | num |
| +-----+
| |   0 |
| +-----+
|
| COMMIT;
|
|                                                   +-----+
|                                                   | num |
|                                                   +-----+
|                                                   |   0 |
|                                                   +-----+
|
|                                                   UPDATE t_products SET num=num-1 WHERE id=1 and num>0;
|
|                                                   SELECT num FROM t_products WHERE id=1;
|                                                   +-----+
|                                                   | num |
|                                                   +-----+
|                                                   |   0 |
|                                                   +-----+
|
|                                                   COMMIT;
|
-
```
通过悲观锁的方式, 可以防止高并发场景下的超卖现象

如果指定主键, 为行级别锁, 否则为表级别锁


## Flask + Sqlalchemy 测试

1. 默认不加锁
```
inventory_obj = db.session.query(Inventory).filter(Inventory.id == inventory_id)
import time
time.sleep(2)
if inventory_obj.one().stock_qty >= num:
    time.sleep(2)
    data = {
        'stock_qty': Inventory.stock_qty - num
    }
    inventory_obj.update(data)
    db.session.commit()
return True
```
出现超卖现象

2. 加悲观锁/排它锁（with_for_update）
```
inventory_obj = db.session.query(Inventory).filter(Inventory.id == inventory_id)
import time
time.sleep(2)
if inventory_obj.with_for_update().one().stock_qty >= num:
    time.sleep(2)
    data = {
        'stock_qty': Inventory.stock_qty - num
    }
    inventory_obj.update(data)
    db.session.commit()
return True
```
一切正常, 没有超卖, 会阻塞其它事务, 性能较差

需要注意的是`for update`要放到`mysql`的事务中，即`begin`和`commit`中，否者不起作用。

3. 乐观锁

通过版本机制实现乐观锁
```mysql
update table set x=x+1, version=version+1 where id=#{id} and version=#{version};
```

4. 分布式锁

很多时候，我们需要对某一个共享变量进行多线程/多进程同步访问

为了确保分布式锁可用，我们至少要确保锁的实现同时满足以下四个条件：
```
互斥性。在任意时刻，只有一个客户端能持有锁。
不会发生死锁。即使有一个客户端在持有锁的期间崩溃而没有主动解锁，也能保证后续其他客户端能加锁。
具有容错性。只要大部分的Redis节点正常运行，客户端就可以加锁和解锁。
解铃还须系铃人。加锁和解锁必须是同一个客户端，客户端自己不能把别人加的锁给解了。
```

- Redis 方案

```
127.0.0.1:6379> SETNX lock_key request_id
(integer) 1
127.0.0.1:6379> SETNX lock_key 2018
(integer) 0
127.0.0.1:6379> TTL lock_key
(integer) -1
127.0.0.1:6379> EXPIRE lock_key 10
(integer) 1
127.0.0.1:6379> TTL lock_key
(integer) 9
127.0.0.1:6379> DEL lock_key
(integer) 1
127.0.0.1:6379> DEL lock_key
(integer) 0
127.0.0.1:6379> TTL lock_key
(integer) -2
```

锁操作名称 | redis操作
--- | ---
获取锁 | SETNX
释放锁 | DEL
防死锁 | EXPIRE


以上方案看起来不错，有两个问题:

1. `SETNX`与`EXPIRE`是2个命令，不是原子的，如果中间崩溃，将会死锁
2. 先拿到锁的事务，如果事务处理时间超过锁过期时间，会出现锁被抢占

改进：

锁操作名称 | redis操作
--- | ---
获取锁 | SET(NX, EX) 将2个操作变成一个原子操作
释放锁 | DEL


- Etcd 方案

TODO


## 死锁

说到锁, 必然要考虑死锁的情况

应避免非主键条件的更新操作


## OLTP 和 OLAP

- OLTP On-Line Transaction Processing 联机事务处理
- OLAP On-Line Analytical Processing 联机分析处理

已有的两个主流开源数据库，MySQL和PostgreSQL都是针对OLTP环境的，在OLAP在线分析需求下它们的性能明显不足。


## ETL

ETL，Extraction-Transformation-Loading的缩写，即数据抽取（Extract）、转换（Transform）、装载（Load）的过程，它是构建数据仓库的重要环节。


## Innodb事务锁相关的三个表：`INNODB_TRX`、`INNODB_LOCKS`、`INNODB_LOCK_WAITS`

`INNODB_TRX`表主要是包含了正在InnoDB引擎中执行的所有事务的信息，包括`waiting for a lock`和`running`的事务
```mysql
SELECT * FROM information_schema.INNODB_TRX\G
```

`INNODB_LOCKS`表主要包含了InnoDB事务锁的具体情况，包括事务正在申请加的锁和事务加上的锁。
```mysql
SELECT * FROM information_schema.INNODB_LOCKS\G
```

`INNODB_LOCK_WAITS`表包含了`blocked`的事务的锁等待的状态
```mysql
SELECT * FROM information_schema.INNODB_LOCK_WAITS\G
```


## 缓存

```
MariaDB [None]> show variables like '%query_cache%';
+------------------------------+----------+
| Variable_name                | Value    |
+------------------------------+----------+
| have_query_cache             | YES      |
| query_cache_limit            | 131072   |
| query_cache_min_res_unit     | 4096     |
| query_cache_size             | 67108864 |
| query_cache_strip_comments   | OFF      |
| query_cache_type             | ON       |
| query_cache_wlock_invalidate | OFF      |
+------------------------------+----------+
7 rows in set (0.00 sec)
```

- mysql 有查询缓存, 调试时需要关闭查询缓存
```mysql
EXPLAIN SELECT * FROM `table_name` WHERE field_name="test";
SELECT SQL_NO_CACHE * FROM `table_name` WHERE field_name="test";
```

- postgres 没有查询缓存, 使用的是系统缓存`/proc/sys/vm/drop_caches`

```bash
sync; sudo service postgresql stop; echo 1 > /proc/sys/vm/drop_caches; sudo service postgresql start
```

```postgresql
EXPLAIN (buffers, analyze, verbose) SELECT * FROM table_name WHERE field_name="test";
```

## 索引

1、联合索引，最左原则：建了一个(a,b,c)的复合索引，那么实际等于建了(a),(a,b),(a,b,c)三个索引
2、索引类型，查询条件值类型必须与定义一致，特别注意数值类型和字符类型