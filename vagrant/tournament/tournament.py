#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM result;")
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players;")
    conn.commit()
    conn.close()

def deleteTournaments():
    """Remove all the tournament records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from tournaments;")
    conn.commit()
    conn.close()


def countPlayers(tid):
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(players) as num from players;")
    players = c.fetchone()[0]
    conn.close()
    return players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = name
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) values (%s);", (bleach.clean(name),))
    conn.commit()
    conn.close()

def playerStandings(tid):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tid = tournament id
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select players_id, players_name, matches, wins from standings where tournament_id=%s", (bleach.clean(tid),))
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(tid, id1, id2, w):
    """Records the outcome of a single match between two players.

    Args:
        tid = tournament id
        id1:  player1
        id2:  player2
        w: id of the player who won
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into matches(tournament_id, player1, player2) VALUES(%(tid)s, %(player1)s, %(player2)s) returning id;",
        {'tid': bleach.clean(tid), 'player1': bleach.clean(id1), 'player2': bleach.clean(id2)})
    match_id = c.fetchone()[0]
    if w:
        c.execute("insert into result(match_id, winner) VALUES(%(match_id)s, %(winner)s);",
                  {'match_id': bleach.clean(match_id), 'winner': bleach.clean(w)})
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


def createTournament(name):
    """Create a new tournament.
    Args:
        Name of tournament
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO tournaments (name) values (%s) returning id;", (bleach.clean(name),))
    tournament_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return tournament_id

