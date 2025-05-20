# Customer Behaviour Analysis in Ecommerce using High Performance Computing
Đây là repository của đồ án cuối kì mô học Tính toán hiệu suất cao (High Performance Computing), khóa 48, ngành Khoa học dữ liệu thuộc Khoa Công nghệ thông tin Kinh doanh, Đại học UEH. 

## Install
Clone this repository and navigate to Customer-Behaviour-Analysis-in-Ecommerce-using-High-Performance-Computing folder
```bash
git clone https://github.com/hllj/Vistral-V](https://github.com/Thanhoanh/Customer-Behaviour-Analysis-in-Ecommerce-using-High-Performance-Computing.git
cd Customer-Behaviour-Analysis-in-Ecommerce-using-High-Performance-Computing
```
## Construct a Docker image by running Dockerfile 
```bash
docker build -t spark-behavior-analysis -f docker/Dockerfile .
```

## Test running Spark cluster locally 
```bash
docker compose -f docker/docker-compose.yml up
```

## Initialize Docker Swarm
We want to deploy Spark cluster on Docker Swarm, we use Virtual Machine and create a cluster with 3 nodes. 

1. On manager node, run: 
```bash
docker swarm init
```
2. Next, on each worker node, run:
```bash
docker swarm join --token SWMTKN-1-5pd8fcltjo0tjc8oqsxza91zwqt4wlerubtslu7at7e64ugc7l-dt9df86gxhg5hnmtr8bhz6djp 192.168.65.3:2377
```
3. Check the number of nodes:
```bash
docker node ls
```
## Deploy production on Swarm 
```bash
docker stack deploy -c cluster/spark-stack.yml spark-cluster
```
