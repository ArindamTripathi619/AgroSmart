#!/bin/bash

# 🐳 AgroSmart Docker Quick Commands
# Quick reference for managing the Dockerized AgroSmart application

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       🌾 AgroSmart Docker Management Script 🌾            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to display menu
show_menu() {
    echo -e "${GREEN}Available Commands:${NC}"
    echo "  1) Start application"
    echo "  2) Stop application"
    echo "  3) Restart application"
    echo "  4) View logs (all)"
    echo "  5) View logs (backend)"
    echo "  6) View logs (frontend)"
    echo "  7) Check status"
    echo "  8) Check resource usage"
    echo "  9) Test backend API"
    echo " 10) Test frontend"
    echo " 11) Rebuild and restart"
    echo " 12) Clean rebuild (removes all cache)"
    echo " 13) Stop and remove everything"
    echo " 14) Show running containers"
    echo " 15) Enter backend shell"
    echo " 16) Enter frontend shell"
    echo " 17) View backend environment"
    echo " 18) Export logs to file"
    echo "  0) Exit"
    echo ""
}

# Function to start application
start_app() {
    echo -e "${YELLOW}Starting AgroSmart containers...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ Containers started!${NC}"
    echo -e "${BLUE}Frontend: http://localhost${NC}"
    echo -e "${BLUE}Backend:  http://localhost:8000${NC}"
    echo -e "${BLUE}API Docs: http://localhost:8000/docs${NC}"
}

# Function to stop application
stop_app() {
    echo -e "${YELLOW}Stopping AgroSmart containers...${NC}"
    docker-compose stop
    echo -e "${GREEN}✅ Containers stopped!${NC}"
}

# Function to restart application
restart_app() {
    echo -e "${YELLOW}Restarting AgroSmart containers...${NC}"
    docker-compose restart
    echo -e "${GREEN}✅ Containers restarted!${NC}"
}

# Function to view all logs
view_logs_all() {
    echo -e "${YELLOW}Viewing logs for all services (Ctrl+C to exit)...${NC}"
    docker-compose logs -f
}

# Function to view backend logs
view_logs_backend() {
    echo -e "${YELLOW}Viewing backend logs (Ctrl+C to exit)...${NC}"
    docker-compose logs -f backend
}

# Function to view frontend logs
view_logs_frontend() {
    echo -e "${YELLOW}Viewing frontend logs (Ctrl+C to exit)...${NC}"
    docker-compose logs -f frontend
}

# Function to check status
check_status() {
    echo -e "${YELLOW}Checking container status...${NC}"
    docker-compose ps
    echo ""
    echo -e "${YELLOW}Health checks:${NC}"
    echo -n "Backend:  "
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Healthy${NC}"
    else
        echo -e "${RED}❌ Unhealthy${NC}"
    fi
    echo -n "Frontend: "
    if curl -s http://localhost/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Healthy${NC}"
    else
        echo -e "${RED}❌ Unhealthy${NC}"
    fi
}

# Function to check resource usage
check_resources() {
    echo -e "${YELLOW}Container resource usage:${NC}"
    docker stats --no-stream
}

# Function to test backend API
test_backend() {
    echo -e "${YELLOW}Testing backend API...${NC}"
    echo ""
    
    echo -e "${BLUE}1. Health Check:${NC}"
    curl -s http://localhost:8000/api/health | python -m json.tool
    echo ""
    
    echo -e "${BLUE}2. Crop Prediction Test:${NC}"
    curl -s -X POST http://localhost:8000/api/predict-crop \
      -H "Content-Type: application/json" \
      -d '{
        "soil_type": "Alluvial Soil",
        "n_level": 90,
        "p_level": 42,
        "k_level": 43,
        "temperature": 20.87,
        "humidity": 82.0,
        "ph_level": 6.5,
        "rainfall": 202.0,
        "region": "North India"
      }' | python -m json.tool
    echo ""
    
    echo -e "${GREEN}✅ Backend API tests completed!${NC}"
}

# Function to test frontend
test_frontend() {
    echo -e "${YELLOW}Testing frontend...${NC}"
    echo ""
    
    echo -e "${BLUE}Frontend HTTP Status:${NC}"
    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost/
    echo ""
    
    echo -e "${BLUE}API Proxy Test:${NC}"
    curl -s http://localhost/api/health | python -m json.tool
    echo ""
    
    echo -e "${GREEN}✅ Frontend tests completed!${NC}"
}

# Function to rebuild and restart
rebuild_restart() {
    echo -e "${YELLOW}Rebuilding and restarting containers...${NC}"
    docker-compose up -d --build
    echo -e "${GREEN}✅ Rebuild complete!${NC}"
}

# Function to clean rebuild
clean_rebuild() {
    echo -e "${RED}⚠️  This will remove all containers, images, and cache!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        echo -e "${YELLOW}Stopping containers...${NC}"
        docker-compose down -v
        
        echo -e "${YELLOW}Cleaning Docker cache...${NC}"
        docker system prune -af --volumes
        
        echo -e "${YELLOW}Rebuilding from scratch...${NC}"
        docker-compose build --no-cache
        
        echo -e "${YELLOW}Starting containers...${NC}"
        docker-compose up -d
        
        echo -e "${GREEN}✅ Clean rebuild complete!${NC}"
    else
        echo -e "${BLUE}Operation cancelled.${NC}"
    fi
}

# Function to stop and remove everything
stop_remove_all() {
    echo -e "${RED}⚠️  This will stop and remove all containers and volumes!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        echo -e "${YELLOW}Stopping and removing containers...${NC}"
        docker-compose down -v
        echo -e "${GREEN}✅ All containers and volumes removed!${NC}"
    else
        echo -e "${BLUE}Operation cancelled.${NC}"
    fi
}

# Function to show running containers
show_containers() {
    echo -e "${YELLOW}Running Docker containers:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Function to enter backend shell
enter_backend_shell() {
    echo -e "${YELLOW}Entering backend container shell...${NC}"
    docker-compose exec backend bash
}

# Function to enter frontend shell
enter_frontend_shell() {
    echo -e "${YELLOW}Entering frontend container shell...${NC}"
    docker-compose exec frontend sh
}

# Function to view backend environment
view_backend_env() {
    echo -e "${YELLOW}Backend container environment:${NC}"
    docker-compose exec backend env | sort
}

# Function to export logs
export_logs() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    LOGFILE="agrosmart_logs_${TIMESTAMP}.txt"
    
    echo -e "${YELLOW}Exporting logs to ${LOGFILE}...${NC}"
    docker-compose logs > "$LOGFILE"
    echo -e "${GREEN}✅ Logs exported to ${LOGFILE}${NC}"
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter your choice [0-18]: " choice
    echo ""
    
    case $choice in
        1) start_app ;;
        2) stop_app ;;
        3) restart_app ;;
        4) view_logs_all ;;
        5) view_logs_backend ;;
        6) view_logs_frontend ;;
        7) check_status ;;
        8) check_resources ;;
        9) test_backend ;;
        10) test_frontend ;;
        11) rebuild_restart ;;
        12) clean_rebuild ;;
        13) stop_remove_all ;;
        14) show_containers ;;
        15) enter_backend_shell ;;
        16) enter_frontend_shell ;;
        17) view_backend_env ;;
        18) export_logs ;;
        0) 
            echo -e "${GREEN}Goodbye! 👋${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    clear
done
