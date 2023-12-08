#!/bin/sh

remoteFile="/mnt/usb_share/main_pi.py"
tempFile="/home/sparky/temp_main.py"
localFile="/home/sparky/main_pi.py"

# delect local file and replace it with an empty file
rm $localFile
touch $localFile

while true
do
    # unmount and remount usb_share to refresh the files on it
    sudo umount /mnt/usb_share
    sudo mount -o ro /piusb.bin /mnt/usb_share

    # copy the Main.py off the usb share for comparing
    sudo \cp -r $remoteFile $tempFile

    if cmp -s "$tempFile" "$localFile"; then
        echo "they match"
    else
        echo "they're different"
        # kill the python script if it's already running
        sudo killall python3
        # copy temp file over the local file
        sudo \cp -r $tempFile $localFile
        # run local file
        sudo python3 $localFile
    fi

    # wait a bit before checking again
    sleep 10
done