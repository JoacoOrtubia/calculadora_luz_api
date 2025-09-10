#!/bin/bash
export PYTHONPATH=/opt/render/project/src:/opt/render/project/src/app
cd /opt/render/project/src
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "PYTHONPATH: $PYTHONPATH"
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT