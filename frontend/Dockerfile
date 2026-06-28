# Usar Node 18 en imagen ligera
FROM node:18-alpine

WORKDIR /app

# Copiar package.json primero para aprovechar la caché de capas de Docker
COPY package*.json ./
RUN npm install

# Copiar el resto del código fuente
COPY . .

EXPOSE 5173

# Arrancar Vite con --host para que sea accesible desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host"]
