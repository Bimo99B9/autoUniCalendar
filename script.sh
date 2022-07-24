#!/bin/bash
gunicorn run:app &
npm run start
