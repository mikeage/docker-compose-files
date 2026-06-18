FROM node:24-alpine@sha256:156b55f92e98ccd5ef49578a8cea0df4679826564bad1c9d4ef04462b9f0ded6

WORKDIR /app

# vips-tools provides `vips dzsave`, `vips thumbnail`, `vipsheader`
RUN apk add --no-cache libc6-compat vips vips-tools

COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY server.js ./
COPY public ./public

ENV PORT=8080
EXPOSE 8080

CMD ["node", "server.js"]
