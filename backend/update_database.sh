#!/usr/bin/env bash

PATH_TO_UPLOAD_SCRIPT="upload.py"

FROM_DATE=`date -v-1w +%Y-%m-%d`
TO_DATE=`date +%Y-%m-%d`

mkdir .govpulse_download
cd .govpulse_download
python -m congressionalrecord.cli $FROM_DATE $TO_DATE json
cd ..

find .govpulse_download | grep "+*\.json" | xargs python $PATH_TO_UPLOAD_SCRIPT speeches

rm -rf .govpulse_download
