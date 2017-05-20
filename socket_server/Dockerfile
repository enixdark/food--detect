FROM node:argon

RUN mkdir -p /app
WORKDIR /app

COPY . /app/
RUN npm i -g babel-cli
RUN npm install
# RUN npm install -g http-server
EXPOSE 1333
CMD [ "babel-node", "start" ]
