#!/bin/bash

EMAIL="kuhle.katherine@gmail.com"

# main file to be executed
SCRIPT="/home/ubuntu/Bachelorarbeit/main.py"

# path to logfile
LOGFILE="/home/ubuntu/Bachelorarbeit/logfile.log"

# send notificationmal to email
echo "The cronjob on you VM BA has started the script $SCRIPT" | mail -s "VM BA: Cronjob started" $EMAIL

# get start time
START_TIME=$(date +%s)

# execution of python script
# python3 $SCRIPT 2>> $LOGFILE

# get end time
END_TIME=$(date +%s)

# calculate duration
DURATION=$((END_TIME - START_TIME))

# read last 50 lines of logfile
LOG_CONTENT=$(tail -n 100 "$LOGFILE")

# send notificationmal to email
echo "Execution completed for $SCRIPT. The script $SCRIPT was executed. It took $DURATION seconds. Logfile content:$LOG_CONTENT"| mail -s "VM BA: Execution completed" $EMAIL

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