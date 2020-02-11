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
兄弟 两个CPU  两个CPU  两个CPU  两核心！！！！
Ok 介绍完以上要求以后，开始安装 准备3台虚拟机 构建 一个Master 两个Node
环境: Centos7.6  Cpu:2 Mem:2Gb Disk： 60Gb  三台 


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

更改主机名
vim /etc/hosts
在原有的后面位置进行追加以下内容                                  
192.168.232.20 kubernetes-master
192.168.232.21 kubernetes-node1
192.168.232.22 kubernetes-node2
scp /etc/hosts 192.168.232.21:/etc/hosts # 直接复制到另外两台主机上
scp /etc/hosts 192.168.232.22:/etc/hosts      

# 2.进行时间校对+安装Docker+设置相关系统设置修改    以下操作三台主机均进行操作                               
进行时间校时(用aliyun的NTP服务器)                                  
yum -y install ntp
ntpdate ntp1.aliyun.com # 三台全部校对时间
安装yum-utils
yum install -y yum-utils \
device-mapper-persistent-data \
lvm2
安装Docker
cd /etc/yum.repos.d/
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum -y install docker-ce
systemctl start docker.service                                  
设置开机自启动Docker
systemctl enable docker.service
                                  
关闭Selinux和禁用防火墙                                 
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config
systemctl disable firewalld                                  

关闭Swap分区                                  
swapoff -a  
cp /etc/fstab /etc/fstab_bak
vim /etc/fstab
对当前的swap分区进行注释,开机不自动挂载                                   
# /dev/mapper/centos-swap swap                    swap    defaults        0 0         # 对此内容进行注释
彻底关闭swap
echo "vm.swappiness =0" >> /etc/sysctl.conf
sysctl -p
查看你的swap选项是否关闭 使用free命令查看
             total        used        free      shared  buff/cache   available
Mem:         995896      232724      229736        7864      533436      591844
Swap:             0           0           0

三台全部激活bridge流量
echo "net.bridge.bridge-nf-call-iptables = 1" >> /etc/sysctl.conf 
echo "net.bridge.bridge-nf-call-ip6tables = 1" >> /etc/sysctl.conf 

安装kubelete
vim /etc/yum.repos.d/kubernets.repo                                  
[aliyun.k8s]
name=aliyun
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0                                  

scp /etc/yum.repos.d/kubernets.repo 192.168.232.21:/etc/yum.repos.d/
scp /etc/yum.repos.d/kubernets.repo 192.168.232.22:/etc/yum.repos.d/

yum -y install kubelet-1.16.2 kubeadm-1.16.2 kubectl-1.16.2 --disableexcludes=kubernetns  (三台全装)
--disableexcludes=kubernetns  表示禁用官网的kubernets安装 使用我们自己配置的安装                                  
systemctl start kubelet
设置kubelet开机自启
systemctl enable kubelet

reboot # 重启三台主机                                 
  
                                  
# 3.下载所需镜像+集群初始化
因为k8s.gcr.io访问不了，手动下载docker镜像                               
docker pull bluersw/kube-apiserver:v1.16.2 
docker pull bluersw/kube-controller-manager:v1.16.2
docker pull bluersw/kube-scheduler:v1.16.2
docker pull bluersw/kube-proxy:v1.16.2
docker pull bluersw/pause:3.1
docker pull bluersw/etcd:3.3.15-0
docker pull bluersw/coredns:1.6.2
docker pull bluersw/flannel:v0.11.0-amd64        
                                  
然后把镜像打上官网对应的标签(必须打标签,不然后果自负)   
docker tag bluersw/kube-apiserver:v1.16.2 k8s.gcr.io/kube-apiserver:v1.16.2
docker tag bluersw/kube-controller-manager:v1.16.2 k8s.gcr.io/kube-controller-manager:v1.16.2
docker tag bluersw/kube-scheduler:v1.16.2 k8s.gcr.io/kube-scheduler:v1.16.2
docker tag bluersw/kube-proxy:v1.16.2 k8s.gcr.io/kube-proxy:v1.16.2
docker tag bluersw/pause:3.1 k8s.gcr.io/pause:3.1
docker tag bluersw/etcd:3.3.15-0 k8s.gcr.io/etcd:3.3.15-0
docker tag bluersw/coredns:1.6.2 k8s.gcr.io/coredns:1.6.2
docker tag bluersw/flannel:v0.11.0-amd64 quay.io/coreos/flannel:v0.11.0-amd64                                  
                                  
如果你看别的bluersw的镜像碍眼 那么接下来把他删掉
docker images | grep bluersw | awk '{print "docker rmi ",$1":"$2}' | sh -x
                                  
Master节点初始化
执行kubeadm init初始化命令：
kubeadm init  --kubernetes-version=v1.16.2 --apiserver-advertise-address=192.168.232.20 --pod-network-cidr=10.244.0.0/16 --service-cidr=10.1.0.0/16
# --apiserver-advertise-address=192.168.232.20 IP 地址为MasterIP
# --kubernetes-version=v1.16.2 加上该参数后启动相关镜像（刚才下载的那一堆）
# --pod-network-cidr=10.244.0.0/16  （Pod 中间网络通讯我们用flannel，flannel要求是10.244.0.0/16，这个IP段就是Pod的IP段）
# --service-cidr=10.1.0.0/16 ： Service（服务）网段（和微服务架构有关）        
                                  
如果你初始化集群报错Master 
[ERROR NumCPU]: the number of available CPUs 1 is less than the required 2 # 你一定没看我最上面写道的要求内容                                  
[WARNING SystemVerification]: this Docker version is not on the list of validated versions: 19.03.5. Latest validated version: 18.09
# 第二个报错表示K8S支持的版本为1809 我用的是1903 版本太高了 不要在意 没有关系                                  
                                  
#每次启动自动加载$HOME/.kube/config下的密钥配置文件（K8S自动行为）                                  
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config 
                                  
                                  
                                  
在Master上安装flannel（在Master上执行） 
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml                                  
                                  
                                  
使用Master生成的密钥加入集群
# Then you can join any number of worker nodes by running the following on each as root:
以上表示如果你想要工作节点加入 请以root身份执行以下命令   
# kubeadm join 192.168.232.20:6443 --token lch6e5.s7qtnjlimq27t7wo \
#    --discovery-token-ca-cert-hash sha256:1347322df8595a24c44fe67c388f087f426971c4bddbe810fd81be821ecdece1    
                                                          
Node1节点操作--加入集群
kubeadm join 192.168.232.20:6443 --token lch6e5.s7qtnjlimq27t7wo \
    --discovery-token-ca-cert-hash sha256:1347322df8595a24c44fe67c388f087f426971c4bddbe810fd81be821ecdece1
Node2节点操作--加入集群
kubeadm join 192.168.232.20:6443 --token lch6e5.s7qtnjlimq27t7wo \
    --discovery-token-ca-cert-hash sha256:1347322df8595a24c44fe67c388f087f426971c4bddbe810fd81be821ecdece1        
                                                                    
                                  
                                  
查看节点
[root@kubernetes-master ~]# kubectl get nodes
NAME                STATUS   ROLES    AGE     VERSION
kubernetes-master   Ready    master   17m     v1.16.2
kubernetes-node1    Ready    <none>   2m26s   v1.16.2
kubernetes-node2    Ready    <none>   2m19s   v1.16.2 # 由于是1.16.2版本的原因可能会导致Roles角色为None  没关系                   
                         
