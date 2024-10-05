#!/usr/bin/python3
from datetime import datetime, timedelta
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
        for root, _, files in walk(targ_dir):
            for f in files:
                info('%s added' % path.join(root, f))
                tar_handle.add(path.join(root, f))


# Upload the tarball at specified time
def upload(mega_obj, targ_dir, files):
    day_retention(mega_obj, int(getenv('DAY_RETENTION')), files)
    now = datetime.now()
    date_time = now.strftime('%m-%d-%Y')
    info('******* Log info for %s *******' % date_time)
    file_name = 'backup-%s.tar.gz' % date_time
    ball_dir(targ_dir, file_name)
    info('Starting upload to mega.nz')

    mega_obj.upload(file_name)
    file_found = mega_obj.find(file_name, exclude_deleted=True)
    if file_found:
        if path.exists(file_name):
            info('Upload completed for %s. Deleting file' % date_time)
            remove(file_name)
        else:
            error('File not found.')
    else:
        error('File not uploaded, please try again.')


# Create an array of the past n days and delete files that aren't inside of it, then empty the Rubbish Bin
def day_retention(mega_obj, num, files):
    info('******* Deleting backups not from the last %s days *******' % num)
    date_arr = []
    for x in range(num):
      d = datetime.now() - timedelta(days=x)
      date_arr.append(d.strftime('%m-%d-%Y'))
    for y in files:
        filename = files[y]['a']['n']
        if filename not in ('Rubbish Bin', 'Cloud Drive', 'Inbox') and 'backup-' in filename:
            file = filename.strip('.tar.gz').strip('backup-')
            if file not in date_arr:
                mega_obj.delete(files[y]['h'])
                info('Deleted %s' % filename)
    info('Day retention cleanup complete')
    mega_obj.empty_trash()


if __name__ == '__main__':
    # Create the Mega object and log in using env variables
    info('Logging in')
    mega = Mega()
    email, password, target_dir = getenv('EMAIL'), getenv('PASSWORD'), getenv('TARGET_DIR')
    m = mega.login(email, password)
    files = m.get_files()


    # Change the working directory to the TARGET_DIR, and then go up a level so the tarball is not put in the TARGET_DIR
    info('Logged in. Changing current working directory.')
    chdir(target_dir)
    chdir('..')
    info('Current working directory is %s' % getcwd())

    if bool(getenv('SCRIPT_MODE', False)):
        # Run upload at the specified BACKUP_TIME
        every().day.at(getenv('BACKUP_TIME')).do(upload, m, target_dir, files)

        # Run the pending tasks every 1s
        while True:
            run_pending()
            sleep(1)
    else:
        upload(m, target_dir, files)
