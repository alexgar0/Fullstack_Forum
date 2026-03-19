#!/bin/bash

sudo docker compose -f ./docker-compose.test.yml up \
  --build \
  --exit-code-from pytest \
  --abort-on-container-exit \
  --attach pytest

EXIT_CODE=$?

echo ""
sudo docker compose -f ./docker-compose.test.yml down -v --rmi local --remove-orphans
echo "Test containers, volumes and local images removed."

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\033[0;32mTEST PASSED\033[0m"
else
    echo -e "\033[0;31mTESTS FAILED\033[0m"
fi

exit $EXIT_CODE