import mysql.connector

# add user
def addAuthor(author_name, author_password):
    # connecting to database
    cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    cursor = cnx.cursor()
    query = f'INSERT INTO authors(user_name, user_password) VALUE ("{author_name}","{author_password}")'
    # doing query to databaseS
    try:
         cursor.execute(query)
         cnx.commit()
         cnx.close()
    except:
        return (False, "the addauthor query didnt run")
    return (True, "success")

# add blogpost
def addBlogPost(author_id, post_title, post_body, post_tag):
    # connecting to database
    try:
        cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database")
    cursor = cnx.cursor()
    query = f"INSERT INTO blog_posts(author_id, post_title, post_body, post_tag) VALUES ({author_id},'{post_title}', '{post_body}', '{post_tag}')"
    # doing query to database
    try:
         cursor.execute(query)
         cnx.commit()
    except:
        cnx.close()
        return (False, "the addblogpost query didnt run")
    cnx.close()
    return (True, "success")

# update user info
def updateAuthor(author_id, author_name, author_password):
    # connecting to database
    cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    cursor = cnx.cursor()
    query = f"UPDATE authors SET author_name = '{author_name}', author_password = '{author_password}' WHERE author_id = {author_id}"
    # doing query to database
    try:
         cursor.execute(query)
         cnx.commit()
    except:
        cnx.close()
        return (False, "the updateauthor query didnt run")
    cnx.close()
    return (True, "success")

# update blogpost
def updateBlogPost(post_id, post_title, post_body, post_tag):
    # connecting to database
    try:
       cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database")
    cursor = cnx.cursor()
    query = f"UPDATE blog_posts SET post_title = '{post_title}', post_body = '{post_body}', post_tag = '{post_tag}' WHERE post_id = {post_id} "
    # doing query to database
    try:
         cursor.execute(query)
         cnx.commit()
    except:
        cnx.close()
        return (False, "the udpateblogpost query didnt run")
    cnx.close()
    return (True, "success")
