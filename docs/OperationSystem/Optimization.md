# System Optimization

Reference:
- [ECS做负载均衡需要做额外的配置](https://help.aliyun.com/knowledge_detail/39428.html)
- [Linux实例常用内核网络参数介绍](https://help.aliyun.com/knowledge_detail/41334.html)

查看内核配置
```
sysctl -a
```

/etc/sysctl.conf
```
vm.swappiness = 0
kernel.sysrq = 1

# net.ipv4.tcp_max_syn_backlog = 1024
# net.core.somaxconn = 128
net.core.somaxconn = 262144

net.ipv4.neigh.default.gc_stale_time = 120

# see details in https://help.aliyun.com/knowledge_detail/39428.html
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 0
net.ipv4.conf.default.arp_announce = 2
net.ipv4.conf.lo.arp_announce = 2
net.ipv4.conf.all.arp_announce = 2

# see details in https://help.aliyun.com/knowledge_detail/41334.html
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.tcp_synack_retries = 2


net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```

/etc/security/limits.conf
```
root soft nofile 65535
root hard nofile 65535
* soft nofile 65535
* hard nofile 65535
```

/proc/sys/vm/max_map_count
```
# default: 65530
262144
```
