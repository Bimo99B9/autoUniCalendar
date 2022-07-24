#!/bin/bash
exec gunicorn run:app
exec npm run linux-start
