#!/usr/bin/python3
from datetime import datetime
from logging import INFO, info, error, basicConfig
from os import walk, path, getenv, remove, chdir, getcwd
from sys import stdout
from tarfile import open
from time import sleep

from mega import Mega
from schedule import every, run_pending


# Setup logger and global variables
basicConfig(stream=stdout, level=INFO)

now = datetime.now()
DATE_TIME = now.strftime('%m-%d-%Y_%H:%M')
FILE_NAME = f'backup-{DATE_TIME}.tar.gz'


# Create tar.gz file in target directory
def ball_dir(targ_dir, filename):
    with open(filename, 'w:gz') as tar_handle:
        for root, dirs, files in walk(targ_dir):
            for f in files:
                info(path.join(root, f) + ' added')
                tar_handle.add(path.join(root, f))


# Compress the files, return if the file can be uploaded
def can_upload():
    info(f'******* Log info for {DATE_TIME} *******')

    # Compress the files in the target directory
    ball_dir(target_dir, FILE_NAME)

    # Calculate if the tarball can be uploaded
    file_size = path.getsize('%s/%s' % (getcwd(), FILE_NAME))
    storage_space = m.get_storage_space()
    used_space = storage_space['used']
    total_space = storage_space['total'] - used_space
    return file_size < total_space

# Upload the tarball at specified time
def upload(m, file_name):
    info('Starting upload to mega.nz')
    m.upload(file_name)

    file_found = m.find(file_name, exclude_deleted=True)

    if file_found:
        if path.exists(file_name):
            info(f'Upload completed for {DATE_TIME}. Deleting file')
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
every().day.at(getenv('BACKUP_TIME')).do(upload(m, FILE_NAME))

# Run the pending tasks every 1s, making sure that there is enough space
while True:
    if can_upload():
        run_pending()
        sleep(1)
    else:
        # Wait an hour, then check if there is enough space
        sleep(3600)
        continue
