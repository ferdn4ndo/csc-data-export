# csc-data-export

A customized data export tool (for a legacy system) using Python+MySQL. It outputs *.json and *.xlsx files for the different database entities of the legacy system.

A database service is also created by the `docker-compose.yml` file, where the SQL files inside the `dump/` folder are automatically ingested when the container is started.

### Prepare the environment

Copy `.env.template` to `.env` and edit it accordingly.

### Run the Application

```sh
docker-compose up --build
```
