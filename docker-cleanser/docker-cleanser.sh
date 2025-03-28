#!/bin/bash

# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi -f $(docker images -aq)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Remove all networks except default ones
docker network rm $(docker network ls --filter "type=custom" -q)

# Prune all remaining resources (cleanup)
docker system prune -a --volumes -f

# Optional WSL shutdown (temporary action to completely reset Docker's virtual environment)
read -p "Do you want to shut down WSL? This temporarily resets Docker's VM from scratch without any permanent effects. Docker Desktop will need to be restarted. (Y/N): " answer
case $answer in
    [Yy]* )
        wsl --shutdown
        echo "WSL has been shut down. Please restart Docker Desktop now."
        ;;
    * )
        echo "WSL shutdown skipped."
        ;;
esac

# Optional confirmation
echo "Docker environment reset completed."

echo -e "\nYou can also limit WSL memory usage by creating or editing the ~/.wslconfig file as follows:\n\n---\n[wsl2]\nmemory=4GB        # adjust this to your liking\nprocessors=4      # optional CPU limit\nswap=0            # optional, disables swap\n---\n\nThen run 'wsl --shutdown' and restart Docker Desktop."

read -n 1 -s -r -p "Press any key to close..."
