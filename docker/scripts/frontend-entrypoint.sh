#!/bin/sh

cd /app/frontend
yarn install
yarn start

exec "$@"