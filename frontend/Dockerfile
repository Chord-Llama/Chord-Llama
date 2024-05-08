FROM node:16

WORKDIR /usr/frontend/src/app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000