#!/bin/bash
mkdir -p uploads good_files
uvicorn server:app --host 0.0.0.0 --port ${PORT:-5000}