# ETCD

一个采用 Go 语言实现的高可用的分布式键值（ Key-Value）数据库，主要用途是共享配置和服务发现，广泛用于分布式系统

Raft 协议 比 ZooKeeper 采用的 Zab 协议简单、易理解

## 应用场景：

### 分布式锁

为什么适合做分布式锁?

1、Raft 算法保持了数据的强一致性
2、提供了一套实现分布式锁原子操作 CAS（CompareAndSwap）的 API

因为etcdv3新引入的多键条件事务，能保证操作原子性
