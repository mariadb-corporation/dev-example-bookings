#!/bin/bash

host=$1
port=$2
user=$3
pass=$4

# use the arguments to connect to MariaDB SkySQl
mariadb="mariadb --host ${host} --port ${port} --user ${user} -p${pass} --ssl-ca skysql_chain.pem"

# non-SkySQL connection
#mariadb="mariadb --host ${host} --port ${port} --user ${user} -p${pass}"

# create travel database and airlines, airports, flights, trips, tickets tables
echo "Creating InnoDB schema..."
${mariadb} < schema/idb_schema.sql
echo "InnoDB schema created."

# create travel_history database and flights table
echo "Creating ColumnStore schema..."
${mariadb} < schema/cs_schema.sql
echo "ColumnStore schema created."

echo "Loading data..."

# Load airlines into flights.airlines
${mariadb} -e "LOAD DATA LOCAL INFILE 'schema/airlines.csv' INTO TABLE airlines FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'" travel

echo "- airlines.csv loaded into travel.airlines"

# Load airports into flights.airlines
${mariadb} -e "LOAD DATA LOCAL INFILE 'schema/airports.csv' INTO TABLE airports FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'" travel
echo "- airports.csv loaded into travel.airports"

echo "- travel_history.flights"
#!/bin/bash
# check for argument, if so use as wildcard for file load match, otherwise load everything
filematch="*"
if [ $# -eq 1 ]
then
  filematch="*$1*"
fi
# load the specified files under the data directory with the file pattern match
for f in data/$filematch.csv; do
  echo "  - $f"
  # /usr/bin/cpimport -m2 -s ',' -E '"' columnstore_schema flights -l $f
  ${mariadb} -e "LOAD DATA LOCAL INFILE '"$f"' INTO TABLE flights FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'" travel_history
done
echo "Done!"