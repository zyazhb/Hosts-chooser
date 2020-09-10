[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/zyazhb/Hosts-chooser)

# dns精选器
[![img](https://badgen.net/badge/license/MIT/blue)](https://github.com/zyazhb/Hosts-chooser/blob/master/LICENSE)
[![img](https://badgen.net/github/last-commit/zyazhb/Hosts-chooser)](https://github.com/zyazhb/Hosts-chooser/commits/master)
[![img](https://badgen.net/github/contributors/zyazhb/Hosts-chooser)](https://github.com/zyazhb/Hosts-chooser/graphs/contributors)
## 基本功能

为被dns污染的站点自动匹配最佳ip地址

## 功能特性
- [x]  多线程 
- [x]  本地模式和网络模式获取ip
- [x]  ip存活检验测速
- [x]  读取文件批量识别
- [x]  Linux自动更新hosts
- [ ]  Windows自动更新hosts

## 环境要求

需要python3.7+环境

## 运行

### Linux

```bash
./Host-chooser-linux [-h] [-t TARGET] [-r READ] [--clean]
                  [--area [{china,asia,europe,africa,oceania,north_america,south_america}]]
                  [--thread THREAD]
```

### Windows

首先安装依赖

```bash
pip install -r requirement.txt
```

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
7. `--update` 在linux下，更新hosts中的dns
8. `--auto` 开启crontab 定时自动更新hosts


## 作者
- [zyazhb](https://github.com/zyazhb)
- [cuteloong](https://github.com/CuteLoong)
- [mashiro01](https://github.com/mashiro01)
- [yueqsun](https://github.com/yueqsun)
- [Dizzk](https://github.com/Dizzk)
