# Linux 课程知识体系

## 模块一：Linux 基础入门
- Linux 发行版概述、系统安装
- 命令行基础、终端使用
- 文件系统层次结构（FHS）
- 基本命令：ls, cd, pwd, mkdir, rmdir, cp, mv, rm, touch, cat, less, head, tail
- 通配符与文件匹配

## 模块二：文件与权限管理
- 文件类型与属性（ls -l 解读）
- 权限模型（rwx、ugo）
- chmod（符号模式和数字模式）
- chown、chgrp
- umask 默认权限
- 特殊权限（SUID、SGID、Sticky Bit）
- ACL 访问控制列表

## 模块三：文本处理
- 重定向：>、>>、<、<<
- 管道：| 和 xargs
- grep 与正则表达式（基础/扩展）
- sed 流编辑器（替换、删除、插入）
- awk 文本处理（字段、模式、动作）
- cut、sort、uniq、wc、tr、diff
- vim 基本操作

## 模块四：用户与组管理
- 用户账号文件：/etc/passwd、/etc/shadow、/etc/group
- useradd、usermod、userdel
- groupadd、groupmod、groupdel
- passwd、chage
- su、sudo 配置（/etc/sudoers）
- 用户环境配置文件（.bashrc、.profile、.bash_profile）

## 模块五：进程管理
- 进程概念（PID、PPID、状态）
- ps、top、htop
- 信号机制：kill、killall、pkill
- 前台/后台任务：jobs、bg、fg、nohup
- 进程优先级：nice、renice
- /proc 文件系统

## 模块六：Shell 脚本编程
- Shebang、注释、变量（本地/环境/特殊变量）
- 条件判断：test、[ ]、[[ ]]
- 分支结构：if-else、case
- 循环结构：for、while、until
- 函数定义与调用
- 参数传递（$1, $@, $#）
- 数组操作
- 调试技巧（set -x, set -e）
- 退出状态码与错误处理

## 模块七：软件包管理
- Debian 系：apt、dpkg
- Red Hat 系：yum/dnf、rpm
- 源码编译安装（./configure、make、make install）
- 依赖管理与冲突解决
- 仓库配置

## 模块八：网络配置与管理
- 网络基础概念（IP、子网、网关、DNS）
- ifconfig/ip 命令
- 网络配置文件
- SSH 远程连接、密钥认证
- SCP/SFTP 文件传输
- 网络诊断：ping、traceroute、netstat、ss、nslookup、curl
- 防火墙基础：iptables、firewalld

## 模块九：存储管理
- 磁盘分区：fdisk、parted
- 文件系统：ext4、xfs、创建与挂载
- /etc/fstab 自动挂载
- LVM 逻辑卷管理
- 磁盘配额（quota）
- RAID 基础

## 模块十：系统监控与日志
- 系统资源监控：free、df、du、iostat、vmstat
- 日志系统：rsyslog、journald
- 关键日志文件：/var/log/messages、/var/log/syslog
- logrotate 日志轮转
- 性能分析基础

## 模块十一：服务与启动管理
- systemd 基础：systemctl
- Unit 文件编写
- 服务状态管理（启动、停止、启用、禁用）
- target（运行级别）
- 定时任务：crontab、at、systemd timer

## 模块十二：安全基础
- Linux 安全模型回顾
- sudo 权限精细控制
- SSH 安全加固
- 文件完整性检查（md5sum、sha256sum）
- 基本审计（auditd）
- SELinux/AppArmor 概念
