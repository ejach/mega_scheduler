#!/usr/bin/python3
from datetime import datetime
from logging import INFO, info, error, basicConfig
from os import walk, path, getenv, remove, chdir, getcwd
from math import floor, log
from sys import stdout
from tarfile import open
from time import sleep

from mega import Mega
from mega.errors import RequestError
from schedule import every, run_pending

# Setup logger
basicConfig(stream=stdout, level=INFO)


# Create tar.gz file in target directory
def ball_dir(targ_dir, filename):
    with open(filename, 'w:gz') as tar_handle:
        for root, dirs, files in walk(targ_dir):
            for f in files:
                info(path.join(root, f) + ' added')
                tar_handle.add(path.join(root, f))


# Upload the tarball at specified time
def upload():
    now = datetime.now()
    date_time = now.strftime('%m-%d-%Y_%H:%M')

    info(f'******* Log info for {date_time} *******')

    file_name = f'backup-{date_time}.tar.gz'

    ball_dir(target_dir, file_name)
    
    file_size = path.getsize('%s/%s' % (getcwd(), file_name))

    storage_space = m.get_storage_space()

    used_space = storage_space['used']

    total_space = storage_space['total'] - used_space

    info('Starting upload to mega.nz')

    try:
        if file_size < total_space:
            m.upload(file_name)
        else:
            # Throw Quota error, catch it and wait until the next day and try again
            raise RequestError(-17)
    except RequestError:
        error('File cannot be uploaded, quota needs to be freed up.')

    file_found = m.find(file_name, exclude_deleted=True)

    if file_found:
        if path.exists(file_name):
            info(f'Upload completed for {date_time}. Deleting file')
            remove(file_name)
        else:
            error('File not found.')
    else:
        error('File not uploaded, please try again.')


# Create the Mega object and log in using env variables
info('Logging in')
mega = Mega()
email, password, target_dir = getenv('EMAIL'), getenv('PASSWORD'), getenv('TARGET_DIR')
m = mega.login(email, password)

# Change the working directory to the TARGET_DIR, and then go up a level so the tarball is not put in the TARGET_DIR
info('Logged in. Changing current working directory.')
chdir(target_dir)
chdir('..')
info('Current working directory is ' + getcwd())

# Run upload at the specified BACKUP_TIME
every().day.at(getenv('BACKUP_TIME')).do(upload)

# Run the pending tasks every 1s
while True:
    run_pending()
    sleep(1)
