#!/bin/sh
chmod 777 /app/data
if [ ! -s /app/data/grid.geojson ] ; then
     cp -r /tmp/data /app
fi 
cd /app/data
jupyter notebook --allow-root --ip=0.0.0.0 --autoreload --no-browser --NotebookApp.token='notebook2023!'
