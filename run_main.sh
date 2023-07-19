#!/bin/bash

EMAIL_RECEIPIENT="kuhle.katherine@gmail.com"

# main file to be executed
SCRIPT="/home/katherine/Development/Bachelorarbeit/main.py"

# path to logfile
LOGFILE="/home/katherine/Development/Bachelorarbeit/logfile.log"

# send notificationmal to email receipient
echo -e "Subject: Cronjob for Bachelorarbeit/main.py started\n\nThe cronjob started the script now." | sendmail $EMAIL_RECEIPIENT

# get start time
START_TIME=$(date +%s)

# execution of python script
python3 $SCRIPT 2>> $LOGFILE

# get end time
END_TIME=$(date +%s)

# calculate duration
DURATION=$((END_TIME - START_TIME))

# read last 50 lines of logfile
LOG_CONTENT=$(tail -n 50 "$LOGFILE")

# check if script failed or ran successfully

# if successful send email and run transform_zara.py
echo -e "Subject: Execution completed for Bachelorarbeit/main.py\n\nThe script Bachelorarbeit/main.py was executed. See Logfile to verify it was successfully. It took $DURATION seconds.\n\nLogfile content:\n$LOG_CONTENT" | sendmail $EMAIL_RECEIPIENT

