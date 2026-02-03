#!/bin/bash

sudo docker compose -f ./docker-compose.test.yml up --build --exit-code-from pytest --abort-on-container-exit
EXIT_CODE=$?

sudo docker compose -f ./docker-compose.test.yml down -v
exit $EXIT_CODE