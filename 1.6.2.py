# This is kubernetes 1.6.2 install Document
Welecome to Waidinsamkeit Home  study leader 
今天我们以安装kubernetes 1. 6 2 举例
关于安装kubernetes的系统要求
`Ubuntu 16.04+
Debian 9+
CentOS 7
Red Hat Enterprise Linux (RHEL) 7
Fedora 25+
HypriotOS v1.0.1+
Container Linux (tested with 1800.6.0)` >>>> 以上是关于系统的要求

关于kubernetes的配置要求
·2 GB or more of RAM per machine (any less will leave little room for your apps 2 CPUs or more·
·Swap disabled. You MUST disable swap in order for the kubelet to work properly.

Ok 介绍完以上要求以后，开始安装 准备3台虚拟机 构建 一个Master 两个Node
环境: Centos7.6  Cpu:2 Mem:2Gb Disk： 60Gb


--------------------------------**********************------------------------------
# 1. 所有主机操作  配置SSH免密钥登陆+更改主机名
第一台主机
ssh-keygen 
ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.232.21
ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.232.22
第二台主机
ssh-keygen 
ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.232.20
ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.232.22
第三台主机
ssh-keygen 
ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.232.20
ssh-copy-id -i /root/.ssh/id_rsa.pub 192.168.232.21
