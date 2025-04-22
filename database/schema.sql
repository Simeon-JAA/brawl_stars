DROP DATABASE IF EXISTS brawl; 

CREATE DATABASE brawl;

\c brawl;
DROP TABLE IF EXISTS brawler CASCADE;
CREATE TABLE brawler (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  brawler_id INT NOT NULL,
  brawler_version SMALLINT NOT NULL,
  brawler_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS starpower CASCADE;
CREATE TABLE starpower (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  starpower_id INT NOT NULL,
  starpower_version SMALLINT NOT NULL,
  brawler_id INT NOT NULL,
  brawler_version SMALLINT NOT NULL,
  starpower_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (starpower_id, starpower_version),
  FOREIGN KEY (brawler_id, brawler_version) REFERENCES brawler (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS gadget CASCADE;
CREATE TABLE gadget (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  gadget_id INT NOT NULL,
  gadget_version SMALLINT NOT NULL,
  brawler_id INT NOT NULL,
  brawler_version SMALLINT NOT NULL,
  gadget_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (gadget_id, gadget_version),
  FOREIGN KEY (brawler_id, brawler_version) REFERENCES brawler (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS gear CASCADE;
CREATE TABLE gear (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  gear_id INT NOT NULL,
  gear_version SMALLINT NOT NULL,
  brawler_id INT NOT NULL,
  brawler_version SMALLINT NOT NULL,
  gear_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (gear_id, gear_version),
  FOREIGN KEY (brawler_id, brawler_version) REFERENCES brawler (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS player CASCADE;
CREATE TABLE player (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  player_tag VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (player_tag)
);

DROP TABLE IF EXISTS player_name CASCADE;  
CREATE TABLE player_name (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  player_tag VARCHAR(50) NOT NULL,
  player_name TEXT NOT NULL,
  player_name_version SMALLINT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (id),
  FOREIGN KEY (player_tag) REFERENCES player (player_tag)
);

DROP TABLE IF EXISTS player_exp CASCADE;
CREATE TABLE player_exp (
id SMALLINT GENERATED ALWAYS AS IDENTITY,
player_tag VARCHAR(50) NOT NULL,
exp_level SMALLINT NOT NULL,
exp_points INT NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (player_tag) REFERENCES player (player_tag)
);

DROP TABLE IF EXISTS player_tropies CASCADE;
CREATE TABLE player_tropies (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  player_tag VARCHAR(50) NOT NULL,
  trophies SMALLINT NOT NULL,
  highest_trophies SMALLINT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (id),
  FOREIGN KEY (player_tag) REFERENCES player (player_tag)
);

DROP TABLE IF EXISTS bs_event CASCADE;
CREATE TABLE bs_event (
  id SMALLINT GENERATED ALWAYS AS IDENTITY,
  bs_event_id INT UNIQUE NOT NULL,
  bs_event_version SMALLINT NOT NULL,
  mode TEXT NOT NULL,
  map TEXT NOT NULL, 
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ,
  PRIMARY KEY (bs_event_id)
);

DROP TABLE IF EXISTS battle_type CASCADE;
CREATE TABLE battle_type (
  battle_type_id SMALLINT GENERATED ALWAYS AS IDENTITY,
  battle_type_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (battle_type_id)
); 

DROP TABLE IF EXISTS battle CASCADE;
CREATE TABLE battle (
  id INT GENERATED ALWAYS AS IDENTITY,
  player_tag VARCHAR(50),
  battle_time TIMESTAMPTZ,
  bs_event_id INT NOT NULL,
  battle_type_id SMALLINT NOT NULL,
  result TEXT NOT NULL,
  duration SMALLINT NOT NULL,
  trophy_change SMALLINT, 
  brawler_played_id INT NOT NULL,
  star_player boolean,
  PRIMARY KEY (id),
  FOREIGN KEY (bs_event_id) REFERENCES bs_event (bs_event_id),
  FOREIGN KEY (player_tag) REFERENCES player (player_tag),
  FOREIGN KEY (battle_type_id) REFERENCES battle_type (battle_type_id)
);

