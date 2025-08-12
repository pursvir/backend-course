#!/usr/bin/env bash

docker run --name booking_db \
  -p 5432:5432 \
  -e POSTGRES_USER=bookingman \
  -e POSTGRES_PASSWORD=vZwrMZ33dnQqdU5T5TmWAmsZgfKwDnKY \
  -e POSTGRES_DB=booking \
  --network=myNetwork \
  --volume pg-booking-data:/var/lib/postgresql/data \
  -d postgres:16

docker run --name booking_cache \
  -p 7379:6379 \
  --network=myNetwork \
  -d redis:7.4

docker run --name booking_celery_worker \
  --network=myNetwork \
  -d booking_image \
  celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
  --network=myNetwork \
  -d booking_image \
  celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking_back \
  -p 7777:8000 \
  --network=myNetwork \
  -d booking_image

  docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=myNetwork \
    -p 80:80 \
    -p 443:443 \
    -d \
    --rm nginx
