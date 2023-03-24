**-To copy .csv(any file) from local to namenode(Linux path)**

docker cp D:\Hive\depart_data.csv namenode:depart_data.csv

**-To go to namenode path**

docker exec -it namenode bash

**1) To check root directories**

 hadoop fs -ls /user/hive/warehouse/hive_db.db
 
 hdfs dfs -ls /user/hive/warehouse/hive_db.db

**2) To create a directory in HDFS**

 hadoop fs -mkdir /user/input
 
 hdfs dfs -mkdir -p /user/input2

**3) To copy file from namenode to HDFS**

 hdfs dfs -put depart_data.csv /user/input/depart_data.csv

**4) To read file in hadoop**

   hadoop fs -cat /user/hive/warehouse/hive_db.db/sales_order_data_orc/000000_0
