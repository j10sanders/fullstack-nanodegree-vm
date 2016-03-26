-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
\i tournament.sql
CREATE DATABASE tournament;
\c tournament

DROP TABLE IF EXISTS MATCHES;

CREATE TABLE players(id serial primary key, name text);

CREATE TABLE tournaments (id serial primary key, name text NOT NULL);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    tournament_id integer REFERENCES tournaments(id) NOT NULL,
    player1 integer REFERENCES players(id) NOT NULL,
    player2 integer REFERENCES players(id) NOT NULL,
    CONSTRAINT not_same CHECK (player1!=player2)
);




-- CREATE TABLE scoreboard(player integer references players(id), score integer, matches(id) integer);

--CREATE VIEW standings as select splayers.id, players.name, wins, matches from players, matches;