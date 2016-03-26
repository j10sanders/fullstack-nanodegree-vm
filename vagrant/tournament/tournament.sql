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

CREATE TABLE players(id serial primary key, name text);

CREATE TABLE tournaments (id serial primary key, name text NOT NULL);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    tournament_id integer REFERENCES tournaments(id) NOT NULL,
    player1 integer REFERENCES players(id) NOT NULL,
    player2 integer REFERENCES players(id) NOT NULL,
    CONSTRAINT not_same CHECK (player1!=player2)
);

CREATE TABLE result (
    match_id integer REFERENCES matches(id),
    winner integer REFERENCES players(id),
    loser integer REFERENCES players(id)
);

CREATE VIEW standings AS
    select t.id as tournament_id,
        p.id as players_id,
        p.name as players_name,
        count(m.*) AS matches,
        count(w.*) AS wins,
        count(l.*) as losses
    FROM tournaments AS t
        CROSS JOIN players AS p
        LEFT JOIN matches AS m ON m.tournament_id=t.id AND p.id IN (m.player1, m.player2)
        LEFT JOIN result AS w ON w.match_id=m.id AND w.winner=p.id
        LEFT JOIN result as l on l.match_id=m.id AND l.winner!=p.id
    GROUP BY t.id, p.id;
