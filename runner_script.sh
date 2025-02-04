#!/bin/bash


echo "ОК"
HOME_DIR="$HOME"
REPORT_FILE="$HOME_DIR/report.txt"
echo "ОК" > "$REPORT_FILE"
echo "Файл отчета создан: $REPORT_FILE"
chmod 644 "$REPORT_FILE"
exit 0