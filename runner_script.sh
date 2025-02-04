#!/bin/bash


echo "ОК"
HOME_DIR="$HOME"
REPORT_FILE="$HOME_DIR/report.txt"
CURRENT_DATE=$(date '+%d-%m-%Y %H:%M:%S')
echo "ОК - $CURRENT_DATE" >> "$REPORT_FILE"
echo "Файл отчета создан: $REPORT_FILE"
chmod 644 "$REPORT_FILE"
exit 0