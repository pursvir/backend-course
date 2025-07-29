#!/usr/bin/env bash

docker run --name booking_db \
  -p 6432:5432 \
  -e POSTGRES_DB=booking_db \
  -e POSTGRES_USER=super_puper_user \
  -e POSTGRES_PASSWORD=dNg5d2fcbwHWPb23SVxb3DCZPM5UffRc \
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
