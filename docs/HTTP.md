# HTTP

名称 | 描述 | 缓存 | 可见 | 长度限制 | 安全
--- | --- | --- | --- | --- | ---
GET | 获取资源 | 可以缓存 | 浏览器地址可见 | 有限制（浏览器、服务器的限制; 与HTTP协议无关） | 容易CSRF
POST | 提交数据 | 无法缓存 | 浏览器地址不可见 | 无限制 | 可设置CSRF
