FROM node:24-alpine@sha256:fb71d01345f11b708a3553c66e7c74074f2d506400ea81973343d915cb64eef0

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
