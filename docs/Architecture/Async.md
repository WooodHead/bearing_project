# 同步与异步、阻塞与非阻塞

这里不讨论系统IO模型, 仅仅讨论编程模型

- 同步 (Synchronous)
- 异步 (Asynchronous)
- 阻塞 (Blocking)
- 非阻塞 (Nonblocking)

## 同步与异步

运行模式

- 同步: 发起请求, 直到当前任务结束;
- 异步: 发起请求, 允许中间切换任务;

## 阻塞与非阻塞

调用方式

- 阻塞: 一直等待结果出来才返回
- 非阻塞: 查询结果, 直接返回（空/结果）

## 差异

- 阻塞/非阻塞: 进程/线程需要操作的数据如果尚未就绪，是否妨碍了当前进程/线程的后续操作。
- 同步/异步: 数据如果尚未就绪，是否需要等待数据结果。
