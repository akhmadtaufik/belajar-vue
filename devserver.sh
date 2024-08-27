#!/bin/sh
source .venv/bin/activate
python -m flask run --debug
cd vue-frontend
npm run dev