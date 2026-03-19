#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_NAME="forum-dev"
COMPOSE_FILE="./docker-compose.dev.yml"
BUILD=false
DETACHED=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --build|-b)
            BUILD=true
            shift
            ;;
        --attach|-a)
            DETACHED=false
            shift
            ;;
        --help|-h)
            echo -e "${BLUE}Usage:${NC} $0 [options]"
            echo -e "Options:"
            echo -e "  -b, --build     Force rebuild images"
            echo -e "  -a, --attach    Run in attached mode (show logs)"
            echo -e "  -h, --help      Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done


echo -e "${BLUE} Starting development environment: ${PROJECT_NAME}${NC}"

DC="sudo docker compose -p ${PROJECT_NAME} -f ${COMPOSE_FILE}"

if [ "$BUILD" = true ]; then
    echo -e "${YELLOW}Building images...${NC}"
    $DC build
fi

echo -e "${YELLOW}Starting services in attached mode (Ctrl+C to stop)...${NC}"
$DC up
