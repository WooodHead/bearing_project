## AlertManager

[https://hub.docker.com/r/prom/alertmanager](https://hub.docker.com/r/prom/alertmanager)

```
docker pull prom/alertmanager:v0.20.0
```

[https://github.com/prometheus/alertmanager](https://github.com/prometheus/alertmanager)

示例参考：

[https://github.com/prometheus/alertmanager/tree/master/examples](https://github.com/prometheus/alertmanager/tree/master/examples)

```
# 开启 webhook 服务
sh examples/webhook.sh

# 测试报警
sh examples/send_alerts.sh
```

检查端口（9090: Prometheus; 9093: AlertManager; 5001: TestWebHook）
```
netstat -ant | grep -E "9090|9093|5001"
```

## 告警方案

1. 如果只用Prometheus，告警需要AlertManager来支持
2. 如果有Grafana，并且配置了Prometheus数据源，那么直接使用Grafana自带的告警就行了
