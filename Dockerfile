FROM postgres:9.4

MAINTAINER Luke Smith

RUN apt-get update && apt-get install -y python-pip python-dev lzop pv daemontools rsyslog
RUN pip install -U pip setuptools
#RUN pip install wal-e
#hack until fxed upstream
RUN apt-get install -y git
RUN pip install -U pip setuptools six
RUN pip install -U 'requests!=2.9.0,>=2.8.1'
RUN pip install git+https://github.com/sebastianneubauer/wal-e.git
RUN pip install  --no-cache-dir --no-deps -U git+https://github.com/sebastianneubauer/wal-e.git

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD recovery.conf /tmp/
#RUN chown postgres:postgres /var/lib/postgresql/data/recovery.conf
ADD recover_db.py /usr/bin/
ADD fix-acl.sh /docker-entrypoint-initdb.d/
ADD setup-wale.sh /docker-entrypoint-initdb.d/