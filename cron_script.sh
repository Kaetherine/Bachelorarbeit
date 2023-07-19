#!/bin/bash

EMAIL_RECEIPIENT="kuhle.katherine@gmail.com"

# main file to be executed
SCRIPT="/home/katherine/Development/Bachelorarbeit/main.py"

# path to logfile
LOGFILE="/home/katherine/Development/Bachelorarbeit/logfile.log"

# send notificationmal to email receipient
echo -e "Subject: Cronjob for Bachelorarbeit/main.py started #1\n\nThe cronjob started the script now." | sendmail $EMAIL_RECEIPIENT

# execution of python script
python3 $SCRIPT 2>> $LOGFILE

# read last 50 lines of logfile
LOG_CONTENT=$(tail -n 50 "$LOGFILE")

# check if script failed or ran successfully
if [ $? -eq 0 ]; then
    # if successful
    echo -e "Subject: Bachelorarbeit/main.py successful! #1\n\nThe script Bachelorarbeit/main.py was executed successfully\n\nLogfile content:\n$LOG_CONTENT" | sendmail $EMAIL_RECEIPIENT
else
    # if failed
    echo -e "Subject: Bachelorarbeit/main.py failed! #1\n\nExecution of the script Bachelorarbeit/main.py FAILED!\n\nLogfile content:\n$LOG_CONTENT" | sendmail $EMAIL_RECEIPIENT
fi
