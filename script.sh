#!/bin/bash
gunicorn run:app &
npm run linux-start
