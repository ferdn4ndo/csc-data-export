#!/bin/sh

if [ $DAEMON -eq 1 ]; then
    echo "Running as a daemon."
    echo "To export the data, execute:"
    echo "docker exec -it csc-data-export sh -c ./start_export.sh"
    tail -f /dev/null
else
    ./start_export.sh
fi
