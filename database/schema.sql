
USE manga_collection;

CREATE TABLE series (
    series_id CHAR(12) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    status ENUM(
        'Ongoing',
        'Completed',
        'Cancelled',
        'Unknown',
        'On Hold'
    ) NOT NULL DEFAULT 'Unknown'
);

CREATE TABLE creator (
    creator_id CHAR(12) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE series_creators (
    series_id CHAR(12) NOT NULL,
    creator_id CHAR(12) NOT NULL,
    PRIMARY KEY (series_id, creator_id),
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (creator_id) REFERENCES creator(creator_id)
);

CREATE TABLE edition (
    edition_id CHAR(12) PRIMARY KEY,
    series_id CHAR(12) NOT NULL,
    name VARCHAR(255) NOT NULL,
    publisher VARCHAR(255),
    volume_count INT NOT NULL,
    format_label VARCHAR(100),
    notes TEXT,
    FOREIGN KEY (series_id) REFERENCES series(series_id)
);

CREATE TABLE volume (
    volume_id CHAR(12) PRIMARY KEY,
    edition_id CHAR(12) NOT NULL,
    volume_number VARCHAR(255) NOT NULL,
    notes TEXT,
    FOREIGN KEY (edition_id) REFERENCES edition(edition_id),
    UNIQUE (edition_id, volume_number)
);

CREATE TABLE ownership (
    ownership_id CHAR(12) PRIMARY KEY,
    volume_id CHAR(12) NOT NULL UNIQUE,
    FOREIGN KEY (volume_id) REFERENCES volume(volume_id)
);