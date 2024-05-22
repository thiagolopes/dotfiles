#!/bin/sh
set -e

echo "
NAME
    backup.sh - Perform backup and restore operations using rsync
OPTIONS
    -b BACKUP_DIR   Specify the directory where the backup will be stored.
    -r BACKUP_DIR   Specify the directory from which the backup will be restored.
EXAMPLES
    1. To perform a backup:
        ./backup.sh -b /path/to/backup

    2. To restore from a backup:
        ./backup.sh -r /path/to/backup
SEE ALSO
    rsync(1)
"

backup(){
    echo "Backup to $BACKUP ..."
    mkdir -p "$BACKUP/rsync/backup-home"
    rsync -a -h -c -b -v --progress \
	  --max-size='2G'\
	  --include='.ssh'\
	  --include='.local/share/gnome-shell'\
	  --exclude='.[!.]*'\
	  --exclude='Dropbox'\
	  --exclude='Larian Studios'\
	  --exclude='vm'\
	  --exclude='tmp'\
	  --exclude='dev'\
	  --exclude='*ROMS*'\
	  "$HOME/"\
	  "$BACKUP/rsync/backup-home/"
}

restore(){
    echo "Restore to home/$USER ..."
    rsync -a -h -c -b -v --progress \
	  "$BACKUP/rsync/backup-home/"\
	  "$HOME/"
}

while getopts b:r:h: flag
do
    case "${flag}" in
	b) BACKUP=${OPTARG}; backup;;
	r) BACKUP=${OPTARG}; restore;;
    esac
done
exit
