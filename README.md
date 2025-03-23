# Brawl Stars Project

## Introduction

Project built around **Brawl Stars**!

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
