# --- Этап 1: сборка Vite-проекта ---
FROM node:20-alpine AS build

# Рабочая директория
WORKDIR /app

# Копируем манифесты зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем остальные файлы проекта
COPY . .

# Сборка production-версии (папка dist)
RUN npm run build

# --- Этап 2: лёгкий nginx для статики ---
FROM nginx:alpine

# Удалим дефолтный конфиг, если свой нужен (опционально)
# RUN rm /etc/nginx/conf.d/default.conf

# Копируем собранную статику
COPY --from=build /app/dist /usr/share/nginx/html

# (опционально) свой конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]