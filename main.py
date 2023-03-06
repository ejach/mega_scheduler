#!/usr/bin/python3
from datetime import datetime
from logging import INFO, info, error, basicConfig
from os import walk, path, getenv, remove, chdir, getcwd
from sys import stdout
from tarfile import open
from time import sleep

from mega import Mega
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

    info('Starting upload to mega.nz')

    m.upload(file_name)

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
