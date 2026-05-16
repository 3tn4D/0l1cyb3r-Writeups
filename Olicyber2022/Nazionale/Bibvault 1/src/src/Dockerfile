FROM node:18-alpine
RUN apk add --no-cache wget

WORKDIR /app
COPY ["package.json", "package-lock.json", "./"]
RUN npm install
COPY . .

RUN mkdir /users

CMD [ "node", "app.js" ]
