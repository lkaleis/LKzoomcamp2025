# ran docker-compose up to spin up pgadmin + postgres db
# in future can include in yml file altogether

export URL1="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
export URL2="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
export URL3="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


docker build -t taxi_ingest:v003 .

docker run -it \
    --network=pg-network \
    taxi_ingest:v003 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name1=yellow_taxi_trips \
    --url1=${URL1} \
    --table_name2=green_taxi_trips \
    --url2=${URL2} \
    --table_name3=zones \
    --url3=${URL3}
