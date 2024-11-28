#!/bin/bash
mkdir -p uploads files good_files
uvicorn server:app --host 0.0.0.0 --port ${PORT:-5000}