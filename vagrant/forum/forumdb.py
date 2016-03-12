#
# Database access functions for the web forum.
# 

import time, psycopg2, bleach

## Database connection
#DB = []

## Get posts from database.
def GetAllPosts():
    DB = psycopg2.connect("dbname=forum")

    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    c = DB.cursor()
    c.execute("SELECT time, content from posts ORDER BY time DESC");
    posts = ({'content': str(row[1]), 'time': str(row[0])}
              for row in c.fetchall())
    DB.close()
    #posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    DB = psycopg2.connect("dbname=forum")
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    c = DB.cursor()
    c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
    bleach.clean('an <script>evil()</script> example')
u'an &lt;script&gt;evil()&lt;/script&gt; example'
    leach.linkify('an http://example.com url')
u'an <a href="http://example.com" rel="nofollow">http://example.com</a> url
    DB.commit()
    DB.close()
    #DB.append((t, content))
