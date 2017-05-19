FROM node:argon

RUN mkdir -p /app
WORKDIR /app

COPY . /app/
RUN npm i -g babel-cli
RUN npm install

EXPOSE 3000
CMD [ "babel-node", "start" ]
