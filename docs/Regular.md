# Regular

单字符匹配

字符 | 功能
--- | ---
. | 匹配任意1个字符（除了\n）
[] | 匹配[]中列举的字符
\d | 匹配数字（0-9）
\D | 匹配非数字
\s | 匹配空白（空格、tab）
\S | 匹配非空白
\w | 匹配单词字符（a-z、A-Z、0-9、_）
\W | 匹配非单词字符

数量字符匹配（匹配前一个字符的出现次数）

字符 | 功能
--- | ---
* | 0或无限次
+ | 至少1次
? | 0或1次
{m} | m次
{m,} | 至少m次
{m,n} | m到n次

边界字符匹配

字符 | 功能
--- | ---
^ | 字符串开头
$ | 字符串结尾
\b | 1个单词的边界
\B | 非单词边界

分组匹配

字符 | 功能
--- | ---
&#124; | 匹配左右任意一个表达式
() | 将括号中字符昨晚一个分组

贪婪与非贪婪

字符 | 功能
--- | ---
&#32; | 贪婪（默认），最长匹配
? | 非贪婪，最短匹配
