# Brawl Stars Project

## Introduction

I play **Brawl Stars** <ins> A LOT </ins>!

The main branch of this reposiory is always in an operational state and can run on a machine providing you have a brawl stars api token. Setup instructions can be found below.

## Setup

| Step | Title                | Command                                                                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---- | -------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Repository location  | `cd ~/Desktop*`                                                        | Navigate to the location on your machine you wish to set the repository up in.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 2    | Clone repository     | `git clone https://github.com/Simeon-JAA/brawl_stars.git`              | Clone repository onto the machine you wish to set up on.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 3    | Venv                 | `python -m venv .venv`                                                 | Create a virtual environment to install all repository requirementsand packages locally. (This step requires your machine to have python installed).                                                                                                                                                                                                                                                                                                                                                     |
| 4    | Activate Venv        | `.\.venv\Scripts\activate`                                             | Activte the virtual environemnt (command written is for windows, your command may vary depending on OS).                                                                                                                                                                                                                                                                                                                                                                                                 |
| 5    | Install requirements | `pip install -r ./requiremets.txt`                                     | Install repository requirements.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 6    | .env file            | `New-file ".env"`                                                      | A .env file is required to securely hold required data make api/database calls. The command creates an empty environment file (command wrttten for windows).                                                                                                                                                                                                                                                                                                                                             |
| 7    | populate .env        |                                                                        | Populate the .env file (text in **bold** should be updated with your own values):<br><br>- db_name = **"DATABASE NAME"**<br>- user = **"DATABASE USERNAME"**<br>- password = **"DATABASE PASSWORD"**<br>- host = **"DATABASE HOSTNAME - (localhost)"**<br>- port = **"DATABASE PORT - (5432)"**<br>- api_token = **"YOUR API TOKEN"**<br>- player_tag = **"BRAWLSTARS PLAYER TAG - or use mine (#2POLV8PV)"**<br><br> You will require a brawl stars api token and access to an external/local database. |
| 8    | create database      | `psql -h <host_name> -p <port> -U <username> -f .\database\schema.sql` | This command uses postgreSQL to create the database and tables in the host location required for this repository.                                                                                                                                                                                                                                                                                                                                                                                        |
| 9    | run main.py          | `python ./etl/main.py`                                                 | Run the etl pipeline.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |


## Database

The `"database"` folder contains the schema for the database that sits behind the API (not created yet). All data stored within the database is unlikely to change (e.g., brawler names, star power names, etc.). It is more efficient for the API to retrieve this data from the database rather than making a call to the **Brawl Stars API** each time.

### Database - Improvements

- Currently does not accommodate brawler stats (e.g., health, damage, etc.). Plans to check if this information is available and incorporate it.
- Create additional tables for more brawler data (e.g., pick rates, win rates, ban rates, etc.).

## ETL

The **ETL pipeline** will retrieve data from the **Brawl Stars API** and update the database.

`main.py` runs on a **cron job** to detect changes every morning and update the database.

### ETL - Improvements

- Currently using the **requests** library, which is not asynchronous. Plans to replace this with **aiohttp** for better efficiency.
