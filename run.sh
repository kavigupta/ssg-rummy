#!/usr/bin/env bash

set -e
cd assets; npm run dev; cd ..
flask --app ssg_rummy_server.server run