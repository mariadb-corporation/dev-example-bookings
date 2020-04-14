#!/bin/bash
host=$1
port=$2
user=$3
pass=$4
target_year=$5
source_year=$6
month=$7

mariadb="mariadb --host ${host} --port ${port} --user ${user} -p${pass} --ssl-ca skysql_chain.pem -e"

${mariadb} "INSERT INTO travel.flights (year,month,day,fl_date,carrier,fl_num,origin,dest,dep_time,arr_time,distance) SELECT $target_year,month,day,(concat($target_year,'-',month,'-',day)),carrier,fl_num,origin,dest,dep_time,arr_time,distance from columnstore_schema.flights where (year=$source_year and month=$month);"

${mariadb} "DELETE FROM travel.tickets;"

${mariadb} "INSERT INTO travel.tickets (fl_date,fl_num,carrier,origin,dest,price) SELECT fl_date,fl_num,carrier,origin,dest,distance*((FLOOR(RAND()*(75-55+1))+55)/100) FROM travel.flights;"


