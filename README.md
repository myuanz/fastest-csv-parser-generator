# fastest-csv-parser-generator
Generate an efficient parser based on as much information as possible. 

Zero Cost Abstractions.


## 使用
书写一个如下定义即可运行生成C++代码

```python
# test.py
import main as m


t = m.CSVRowDef([
    m.CSVDecimal('x', 16), 
    m.CSVDecimal('y', 16)
])
print(t.generate())
```

```
python test.py | clang-format > output.cpp
```

## 类型

- 整数
    - 十进制纯整数 ✅
    - *十六进制整数*
        - *无前导的十六进制整数*
        - *带0x的十六进制整数*
        - *带\x的十六进制整数*
- 字符串
    - ASCII字符串
        - 定长
        - 变长有上限
        - 变长无上限
    - *UNICODE字符串*
        - *定长*
        - *变长有上限*
        - *变长无上限*


## 设计细节

先按照行生成一个枚举
```C++
enum RowItem{
    item_a, item_b, item_c, item_d
}
```
之后生成处理代码，处理部分的结构如下：
```C++

switch(*f){
    case SEP:
        switch(current_row){
            case item_a:
                pass
        }
    case '\n':
        pass;
    default:
        switch(current_row){
            case item_a:
                pass
        }
}

```

大致分为：
- 切换到下一个条目前
- 行结束时
- 匹配到条目时

使用时面向两种场景
- 使用迭代器按行读取一轮
- 需要将所有行都读入内存

面向两个语言：
- C++
- C++包装到的Python

目前因性能先不支持C++迭代器式获取