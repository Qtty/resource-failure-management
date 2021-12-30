FROM node:16.13.1 as frontend_build

WORKDIR /frontend

COPY . .

RUN npm install
RUN npm run build


FROM nginx

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend_build /frontend/dist /usr/share/nginx/html
