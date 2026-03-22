FROM node:18

WORKDIR /app

COPY package* ./
RUN npm install

COPY ./ ./

RUN useradd appuser
USER appuser

ENTRYPOINT [ "node", "server.js" ]
