#!/bin/sh

remoteFile="/mnt/usb_share/main_pi.py"
tempFile="/home/sparky/temp_main.py"
localFile="/home/sparky/main_pi.py"
logFile="/home/sparky/startup_log.txt"

# Redirect all output to the log file
exec >> $logFile 2>&1

# Delete local file and replace it with an empty file
rm $localFile
touch $localFile

while true
do
    # Unmount and remount usb_share to refresh the files on it
    sudo umount /mnt/usb_share
    sudo mount -o ro /piusb.bin /mnt/usb_share

    # Copy the Main.py off the usb share for comparing
    sudo \cp -r $remoteFile $tempFile

    if cmp -s "$tempFile" "$localFile"; then
        echo "They match"
    else
        echo "They're different"
        # Kill the python script if it's already running
        sudo killall python3
        # Copy temp file over the local file
        sudo \cp -r $tempFile $localFile
        # Run local file
        sudo python3 $localFile &
    fi

    # Wait a bit before checking again
    sleep 10
done
