#!/usr/bin/python
import logging
from subprocess import check_call
import time
import grp
import pwd
import os

logger = logging.getLogger(__file__)


def pg_get_configuration():
    configuration = {}
    # Get the initialization flag.
    value = os.getenv('PGDATA', 'True')
    configuration.update({'data_directory': value})
    # Get the AWS secret key.
    value = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    configuration.update({'aws_secret_access_key': value})
    # Get the AWS access key.
    value = os.getenv('AWS_ACCESS_KEY_ID', None)
    configuration.update({'aws_access_key_id': value})
    # Get the wal-e S3 prefix.
    value = os.getenv('WALE_S3_PREFIX', None)
    configuration.update({'wale_s3_prefix': value})
    # Get the wal-e S3 hostname.
    value = os.getenv('WALE_S3_ENDPOINT', None)
    configuration.update({'wale_s3_endpoint': value})

    return configuration


def chown(path, user, group):
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(group).gr_gid
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chown(os.path.join(root, dir), uid, gid)
        for file in files:
            os.chown(os.path.join(root, file), uid, gid)
    os.chown(path, uid, gid)


def run(app, *args):
    check_call([app] + list(args))


def pg_change_data_directory(data_directory):
    run('gosu', 'postgres', 'pg_ctl', '-D', data_directory, '-m', 'fast', '-w', 'stop')
    run('gosu', 'postgres', 'pg_ctl', '-D', data_directory, '-m', 'fast', '-w', 'start')
    chown(data_directory, 'postgres', 'postgres')


def wait_for_file(file_path):
    while not os.path.exists(file_path):
        logger.info("file {} does not yet exist".format(file_path))
        time.sleep(1)
    logger.info("file {} does exist".format(file_path))


def check_recovery_exists():
    try:
        run('gosu', 'postgres', '/usr/bin/envdir', '/etc/wal-e.d/env', '/usr/local/bin/wal-e', 'backup-list')
    except:
        logger.info("recovery backup does not exist")
        return False
    return True

def pg_fetch_initial_backup(data_directory):
    if check_recovery_exists():
        run('gosu', 'postgres', 'pg_ctl', '-D', data_directory, '-m', 'fast', '-w', 'stop')
        run('gosu', 'postgres', '/usr/bin/envdir', '/etc/wal-e.d/env', '/usr/local/bin/wal-e', 'backup-fetch', data_directory, 'LATEST')
        run('gosu', 'postgres', 'cp', '/tmp/recovery.conf', data_directory)
        run('gosu', 'postgres', 'pg_ctl', '-D', data_directory, '-m', 'fast', '-w', 'start')
        wait_for_file(data_directory + '/recovery.done')

if __name__ == "__main__":
    # Load the configuration into a dictionary.
    configuration = pg_get_configuration()
    pg_change_data_directory(configuration['data_directory'])
    logging.basicConfig(level=logging.DEBUG)
    logger.info("starting postgres recovery")
    pg_fetch_initial_backup(configuration['data_directory'])
    logger.info("recovery finished")