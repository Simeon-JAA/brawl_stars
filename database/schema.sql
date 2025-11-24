DROP TABLE IF EXISTS brawler;
CREATE TABLE brawler (
  brawler_id INTEGER NOT NULL,
  brawler_version INTEGER NOT NULL,
  brawler_name TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS starpower;
CREATE TABLE starpower (
  starpower_id INTEGER NOT NULL,
  starpower_version INTEGER NOT NULL,
  starpower_name TEXT NOT NULL,
  brawler_id INTEGER NOT NULL,
  brawler_version INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (starpower_id, starpower_version),
  FOREIGN KEY (brawler_id, brawler_version) REFERENCES brawler (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS gadget;
CREATE TABLE gadget (
  gadget_id INTEGER NOT NULL,
  gadget_version INTEGER NOT NULL,
  gadget_name TEXT NOT NULL,
  brawler_id INTEGER NOT NULL,
  brawler_version INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (gadget_id, gadget_version),
  FOREIGN KEY (brawler_id, brawler_version) REFERENCES brawler (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS gear;
CREATE TABLE gear (
  gear_id INTEGER NOT NULL,
  gear_version INTEGER NOT NULL,
  gear_name TEXT NOT NULL,
  brawler_id INTEGER NOT NULL,
  brawler_version INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (gear_id, gear_version),
  FOREIGN KEY (brawler_id, brawler_version) REFERENCES brawler (brawler_id, brawler_version)
);

DROP TABLE IF EXISTS player;
CREATE TABLE player (
  player_id INTEGER NOT NULL,
  player_tag VARCHAR(50) UNIQUE NOT NULL,
  player_name TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  last_updated TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (player_id)
);

DROP TABLE IF EXISTS player_exp;
CREATE TABLE player_exp (
player_exp_id INTEGER,
player_id INTEGER NOT NULL,
exp_level INTEGER NOT NULL,
exp_points INTEGER NOT NULL,
created_at TEXT DEFAULT (datetime('now')),
PRIMARY KEY (player_exp_id),
FOREIGN KEY (player_id) references player (player_id)
);

DROP TABLE IF EXISTS player_trophies;
CREATE TABLE player_trophies (
  player_trophies_id INTEGER NOT NULL,
  player_id INTEGER NOT NULL,
  trophies INTEGER NOT NULL,
  highest_trophies INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (player_trophies_id),
  FOREIGN KEY (player_id) references player (player_id)
);

DROP TABLE IF EXISTS player_victories;
CREATE TABLE player_victories (
  player_victories_id INTEGER NOT NULL,
  player_id INTEGER NOT NULL,
  _3v3_victories INTEGER,
  solo_victories INTEGER,
  duo_victories INTEGER,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (player_victories_id),
  FOREIGN KEY (player_id) references player (player_id)
);

DROP TABLE IF EXISTS bs_event;
CREATE TABLE bs_event (
  bs_event_id INTEGER NOT NULL,
  bs_event_version INTEGER NOT NULL,
  mode TEXT NOT NULL,
  map TEXT NOT NULL, 
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (bs_event_id, bs_event_version)
);


DROP TABLE IF EXISTS process;
CREATE TABLE process (
  process_id INTEGER NOT NULL,
  process_name TEXT NOT NULL,
  PRIMARY KEY (process_id)
);

INSERT INTO process (process_id, process_name) VALUES
(1, 'Brawler ETL'),
(2, 'Player ETL');

DROP TABLE IF EXISTS process_log;
CREATE TABLE process_log (
  process_log_id INTEGER NOT NULL,
  process_id TEXT NOT NULL,
  process_status TEXT NOT NULL,
  last_updated TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (process_log_id),
  FOREIGN KEY (process_id) REFERENCES process (process_id)
);

-- DROP TABLE IF EXISTS battle_type;
-- CREATE TABLE battle_type (
--   battle_type_id SMALLINT GENERATED ALWAYS AS IDENTITY,
--   battle_type_name TEXT NOT NULL,
--   created_at TIMESTAMPTZ DEFAULT NOW(),
--   PRIMARY KEY (battle_type_id)
-- ); 

-- DROP TABLE IF EXISTS battle;
-- CREATE TABLE battle (
--   battle_id INT TEXT NOT NULL,
--   player_tag VARCHAR(50) NOT NULL,
--   battle_time TIMESTAMPTZ,
--   bs_event_id INT NOT NULL,
--   battle_type_id SMALLINT NOT NULL,
--   result TEXT NOT NULL,
--   duration INTEGER NOT NULL,
--   trophy_change INTEGER, 
--   brawler_id INTEGER NOT NULL,
--   star_player boolean,
--   PRIMARY KEY (id),
--   FOREIGN KEY (bs_event_id) REFERENCES bs_event (bs_event_id),
--   FOREIGN KEY (player_id) references player (player_id)
-- );

