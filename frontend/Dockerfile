# React Dockerfile
FROM node:18-slim

WORKDIR /client
COPY client/package.json client/package-lock.json ./
RUN npm install

COPY client ./

# Build the React app
RUN npm run build

# Serve the app using a lightweight HTTP server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
