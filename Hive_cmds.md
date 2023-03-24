**-To start hive in power shell**

docker exec -it d2e715017c17e3a03a2dc745e56b1ac1c37a00cc1f117b5d310f4d2d963d4b48 /bin/bash


**-To start Hive**

Hive;

show databases;

create database hive_db;

use hive_db;

show tables;


**- To create internal table**

      create table department_data
      (dept_id int,
      dept_name string,
      manager_id int,
      salary int)
      row format delimited
      fields terminated by ',';
      
describe department_data;

describe formatted department_data;

set hive.cli.print.header=true;



**- To load data in table from local path file**

   load data local inpath 'file:///department_data.csv' into table department_data;
   
   
   
**- To load data in table from HDFS path file**

   load data inpath '/user/input/depart_data.csv' into table department_data;



**- To create external table**

           create external table Ex_department_data
           (dept_id int,
           dept_name string,
           manager_id int,
           salary int)
           row format delimited
           fields terminated by ','
           location '/user/input2/';
           
           

**- To create table for array based file**

     create table employee
     (
     emp_id int,
     name string,
     skills array<string>
     )
     row format delimited
     fields terminated by ','
     collection items terminated by ':';

     select name,skills[0] as primary_skill,size(skills) as total_skills,
     array_contains(skills,"HADOOP") as knows_hadoop,
     sort_array(skills) as sorted_skills
     from employee;
     
     

**- To create table for dictionary based file**

    create table employee_map_data
     (
     id int,
     name string,
     details map<string,string>
     )
     row format delimited
     fields terminated by ','
     collection items terminated by '|'
     map keys terminated by ':';

     select id,name,
     details["gender"] as gender,
     size(details) as map_size,
     map_keys(details) as dist_keys,
     map_values(details) as dist_values
     from employee_map_data;



**- To create a backup copy of a table**

    create table employee_backup as select * from employee;
    
    

**- To create a table based using sedre**

     create table csv_table
     (name string,
     location string)
     ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
     WITH SERDEPROPERTIES (
     "separatorChar" = ",",
     "quoteChar"="\"",
     "escapeChar"="\\"
     )
     stored as textfile
     tblproperties ("skip.header.line.count"="1");
     
     

**- To create a table based on json file**

    create table json_table
     ( name string,
     id int,
     skills array<string>)
     ROW FORMAT SERDE
     'org.apache.hive.hcatalog.data.JsonSerDe'
     stored as textfile;



**- To add a jar file in hive shell**

    add jar file:///config/workspace/hive-hcatalog-core-0.14.0.jar;
    
    

**- To create parquet table**

    create table sales_data_row_pq
     (
     prod string,
     total_sales int
     )
     stored as parquet;



**- To load data from csv table to parquet table**

    from sales_data_row insert overwrite table sales_data_row_pq select *;
    
    or
    
    insert overwrite table sales_data_row_pq select * from sales_data_row;
    
    
    

**- To create ORC table**

    create table sales_data_row_orc
     (
     prod string,
     total_sales int
     )
     stored as orc;



**- To load data from csv table to orc table**

    from sales_data_row insert overwrite table sales_data_row_orc select *;



**- To set reducer size in mapreduce**

    set mapreduce.job.reduces=3;



**- To set max reducer in mapreduce**

    set hive.exec.reducers.max=10;



**- To create a static partitioning table**

    create table sales_data_static_part
     (
     ORDERNUMBER int,
     QUANTITYORDERED int,
     SALES float,
     YEAR_ID int
     )
     partitioned by (COUNTRY string);

- To load data to static partitioned table from other table

    insert overwrite table sales_data_static_part partition(country='USA')
    select ordernumber,quantityordered,sales,year_id from sales_order_data_orc where country='USA';

- To select records from static partitioned table
    
    select * from sales_data_static_part where country='USA';



**- To create a dynamic partitioning table**

    create table sales_data_dynamic_part
     (
     ORDERNUMBER int,
     QUANTITYORDERED int,
     SALES float,
     YEAR_ID int
     )
     partitioned by (COUNTRY string);

 - To load data to dynamic partitioned table from other table
    
    insert overwrite table sales_data_dynamic_part partition(country)
    select ordernumber,quantityordered,sales,year_id,country from sales_order_data_orc;

  - To set partitioning property to nonstrict
    
    set hive.exec.dynamic.partition.mode=nonstrict



**- To create a multi level dynamic partitioning table**

    create table sales_data_dynamic_multi_part
     (
     ORDERNUMBER int,
     QUANTITYORDERED int,
     SALES float
     )
     partitioned by (COUNTRY string,YEAR_ID int);

- To load data to multi level dynamic partitioned table from other table
    
    insert overwrite table sales_data_dynamic_multi_part partition(country,year_id)
    select ordernumber,quantityordered,sales,country,year_id from sales_order_data_orc;



**- To create bucking table**

    create table buck_users
          (id int,
          name string,
          salary int,
          unit string
          )
     clustered by (id)
     sorted by (id)
     into 3 buckets;

- To load records to bucketing table from existing table
    
    insert overwrite table buck_users select * from users;



**- Map join (Broadcast join)**

    set hive.auto.convert.join=true;
    
    select * from buck_users u inner join buck_locations l on u.id=l.id;



**- Bucket map join**

    set hive.optimize.bucketmapjoin=true;
    
    select * from buck_users u inner join buck_locations l on u.id=l.id;



**- sorted merge bucket join**

    set hive.enforce.sortmergebucketmapjoin=false;
    
    set hive.auto.convert.sortmerge.join=true;
    
    set hive.optimize.bucketmapjoin = true;
    
    set hive.optimize.bucketmapjoin.sortedmerge = true;
    
    select * from buck_users u inner join buck_locations l on u.id=l.id;

**- To add udf file to Hive shell from hdfs**

    add file hdfs:/user/input/multiply_udf.py;

**- To add udf file to Hive shell from local**

    add file file:///home/hadoop/multiply_udf.py;

**- To transform data using udf**

    select transform(quantityordered) using 'python multiply_udf.py' as (quantityordered int) from sales_order_data_orc limit 5;

**- To transform multiple data using udf**

    select transform(country,ordernumber,quantityordered) using 'python many_column_udf.py' as (country string,ordernumber int,multiplied_qty int) from sales_order_data_orc limit 5;

**- exit;**


