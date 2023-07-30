#!/bin/bash

EMAIL="kuhle.katherine@gmail.com"

# main file to be executed
SCRIPT="/home/ubuntu/Bachelorarbeit/main.py"

# path to logfile
LOGFILE="/home/ubuntu/Bachelorarbeit/logfile.log"

# send notificationmal to email
echo "The cronjob has started the script $SCRIPT" | mail -s "Cronjob started" $EMAIL

# get start time
START_TIME=$(date +%s)

# execution of python script
python3 $SCRIPT 2>> $LOGFILE

# get end time
END_TIME=$(date +%s)

# calculate duration
DURATION=$((END_TIME - START_TIME))

# read last 50 lines of logfile
# LOG_CONTENT=$(tail -n 50 "$LOGFILE")

# whole logfile
LOG_CONTENT=$LOGFILE

# send notificationmal to email
echo "Execution completed for $SCRIPT\n\nThe script $SCRIPT was executed. See Logfile to verify it was successfully. It took $DURATION seconds.\n\nLogfile content:\n$LOG_CONTENT"| mail -s "Cronjob: execution completed" -A $LOGFILE $EMAIL

# rm "/home/ubuntu/Bachelorarbeit/logfile.log"
rm "/home/ubuntu/Bachelorarbeit/categories.csv"
rm "/home/ubuntu/Bachelorarbeit/categories_by_target_groups.csv"
rm "/home/ubuntu/Bachelorarbeit/materials.csv"
rm "/home/ubuntu/Bachelorarbeit/origins.csv"
rm "/home/ubuntu/Bachelorarbeit/product_availability.csv"
rm "/home/ubuntu/Bachelorarbeit/products.csv"
rm "/home/ubuntu/Bachelorarbeit/products_by_categories.csv"
rm "/home/ubuntu/Bachelorarbeit/related_products.csv"
rm "/home/ubuntu/Bachelorarbeit/target_groups.csv"