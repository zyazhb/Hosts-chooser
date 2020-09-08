# dns精选器

## 基本功能

防止dns污染自动匹配被DNS污染但是ip没有被屏蔽的网站

## 使用方法

所需环境为python3.7.6

```bash
python main.py [-h] [-t TARGET] [-r READ] [--clean]
                  [--area [{china,asia,europe,africa,oceania,north_america,south_america}]]
                  [--thread THREAD]
```

## 参数解释

1. `-h` 获取基本使用方法
2. `-t` 选择目标域名
3. `-r` 批量读取<dns.txt>文件内的目标域名进行dns解析并批量输出
4. `--clean` 显示详细信息
5. `--area` 选择所需要的的地区/区域
6. `--thread` 选择所需要的进程数(默认为3)

## 示例

```bash
1. python mian.py -h    # 获取基本使用方法
2. python mian.py -t www.github.com --clean --area china --thread 3     # 获取github在中国的dns解析结果
```

