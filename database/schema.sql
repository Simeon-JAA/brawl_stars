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
  player_id INT NOT NULL,
  player_tag VARCHAR(50) UNIQUE NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (player_id)
);

DROP TABLE IF EXISTS player_name;  
CREATE TABLE player_name (
  id INTEGER,
  player_id INT  NOT NULL,
  player_name TEXT NOT NULL,
  player_name_version INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (id),
  FOREIGN KEY (player_id) references player (player_id)
);

DROP TABLE IF EXISTS player_exp;
CREATE TABLE player_exp (
id INTEGER,
player_id INT  NOT NULL,
exp_level INTEGER NOT NULL,
exp_points INTEGER NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (player_id) references player (player_id)
);

DROP TABLE IF EXISTS player_tropies;
CREATE TABLE player_tropies (
  id INTEGER,
  player_id INT  NOT NULL,
  trophies INTEGER NOT NULL,
  highest_trophies INTEGER NOT NULL,
  last_updated TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (id),
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
  player_tag VARCHAR(50) NOT NULL,
  battle_time TIMESTAMPTZ,
  bs_event_id INT NOT NULL,
  battle_type_id SMALLINT NOT NULL,
  result TEXT NOT NULL,
  duration INTEGER NOT NULL,
  trophy_change INTEGER, 
  brawler_played_id INTGER NOT NULL,
  star_player boolean,
  PRIMARY KEY (id),
  FOREIGN KEY (bs_event_id) REFERENCES bs_event (bs_event_id),
  FOREIGN KEY (player_id) references player (player_id)
);

