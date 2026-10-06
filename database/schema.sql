USE manga_collection;



CREATE TABLE creator(
creator_id CHAR(12) PRIMARY KEY,
name VARCHAR(255) NOT NULL
);

CREATE TABLE series_creators(
series_id CHAR(12),
creator_id CHAR(12),
PRIMARY KEY (series_id, creator_id),
FOREIGN KEY (series_id) REFERENCES series(series_id),
FOREIGN KEY (creator_id) REFERENCES  creator(creator_id)
);

CREATE TABLE edition(
edition_id CHAR(12) PRIMARY KEY,
series_id CHAR(12),
name VARCHAR(255) NOT NULL,
publisher VARCHAR(255),
volume_count INT NOT NULL,
FOREIGN KEY (series_id) REFERENCES series(series_id)

);

CREATE TABLE volume(
volume_id CHAR(12) PRIMARY KEY,
edition_id CHAR(12),
volume_number VARCHAR(255) NOT NULL,
FOREIGN KEY (edition_id) REFERENCES edition(edition_id),
UNIQUE (edition_id, volume_number)

);

CREATE TABLE ownership(
ownership_id CHAR(12) primary key,
volume_id CHAR(12),
FOREIGN KEY (volume_id) REFERENCES volume(volume_id),
UNIQUE (volume_id)

);

