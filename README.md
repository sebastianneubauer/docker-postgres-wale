# Postgres docker container with wale

Based on https://github.com/docker-library/postgres with [WAL-E](https://github.com/wal-e/wal-e) installed.

Environment variables to pass to the container for WAL-E, all of these must be present or WAL-E is not configured.

`AWS_ACCESS_KEY_ID`

`AWS_SECRET_ACCESS_KEY`

`WALE_S3_PREFIX=\"s3://<bucketname>/<path>\"`

# Build the image

    cd postgres
    docker build .

#Testing

install the requirements:
    
    pip install -r requirements.txt
    pip install -r requirements_dev.txt

Then execute the tests (be patient, this may take a while):

    cd tests
    py.test -s
    
The tests are using docker-compose to set up a s3proxy container and the postgres container with wal-e support.

You can start orchestrated containers (postgres+s3proxy) with docker-compose:
 
    docker-compose -f test-docker-compose.yml up -d
    
Now you have a running postgres container which is backuped in the s3proxy container