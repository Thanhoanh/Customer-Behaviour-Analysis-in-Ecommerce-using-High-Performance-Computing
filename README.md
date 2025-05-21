# Customer Behaviour Analysis in Ecommerce using High Performance Computing
Đây là repository của đồ án cuối kì mô học Tính toán hiệu suất cao (High Performance Computing), khóa 48, ngành Khoa học dữ liệu thuộc Khoa Công nghệ thông tin Kinh doanh, Đại học UEH. 

## Install
Clone this repository and navigate to Customer-Behaviour-Analysis-in-Ecommerce-using-High-Performance-Computing folder
```bash
git clone https://github.com/hllj/Vistral-V](https://github.com/Thanhoanh/Customer-Behaviour-Analysis-in-Ecommerce-using-High-Performance-Computing.git
cd Customer-Behaviour-Analysis-in-Ecommerce-using-High-Performance-Computing/docker
```
## Construct a Docker image by running Dockerfile 
```bash
docker build -t spark-image -f docker/Dockerfile .
```

## Testing
We run Spark cluster in a testing environment configured in docker-compose.yml
```bash
docker compose -f docker/docker-compose.yml up
```
Check the running containers by running this command: 
```bash
docker ps
```

Enter spark-master:
```bash
docker exec -it spark-master bash
```
Submit a job on spark-master: 
```bash
spark-submit ./scripts/ml.py
```

## Initialize Docker Swarm
After testing phase, we move on to deploy the production on a distributed systerm on Docker Swarm.
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
Next, we will deploy the production on Swarm, which was configured in spark-stack.yml, this is a modified version of docker-compose.yml, which makes the production compatible to run on Swarm distributed system.
```bash
docker stack deploy -c cluster/spark-stack.yml spark-cluster
```
