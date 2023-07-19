
#!/bin/bash

# Die E-Mail-Adresse, an die Benachrichtigungen gesendet werden sollen
EMAIL="kuhle.katherine@gmail.com"

# Der Pfad zu Ihrem Python-Skript
SCRIPT="/home/katherine/Development/Bachelorarbeit/main.py"

# Der Pfad zu Ihrer Protokolldatei
LOGFILE="/home/katherine/Development/Bachelorarbeit/logfile.log"

# Senden Sie eine E-Mail, um den Start des Skripts anzukündigen
echo "Der Cronjob startet jetzt das Skript $SCRIPT" | mail -s "Cronjob startet" $EMAIL

# Führen Sie das Python-Skript aus und leiten Sie etwaige Fehler an die Protokolldatei weiter
python3 $SCRIPT 2>> $LOGFILE

# Überprüfen Sie, ob das Skript erfolgreich war
if [ $? -eq 0 ]; then
    # Wenn das Skript erfolgreich war, senden Sie eine Erfolgsmeldung
    echo "Das Skript $SCRIPT wurde erfolgreich ausgeführt" | mail -s "Cronjob erfolgreich" $EMAIL
else
    # Wenn das Skript fehlschlug, senden Sie die Fehlermeldung und die Protokolldatei
    echo "Das Skript $SCRIPT ist auf einen Fehler gestoßen. Siehe angehängte Protokolldatei für Details." | mail -s "Cronjob Fehler" -A $LOGFILE $EMAIL
fi

