FROM node:16-alpine

WORKDIR /app

COPY /frontend ./frontend
COPY /docker ./docker

WORKDIR /app/frontend
RUN yarn install

WORKDIR /app

CMD ["sh", "./docker/scripts/frontend-entrypoint.sh"]