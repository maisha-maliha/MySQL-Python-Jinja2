import mysql.connector
import backend.hashit as hashit

# get all authors
def getAuthors():
    # connecting to database
    try:
       cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database authors")
    # cursor for querying in database
    cursor = cnx.cursor()
    query = "SELECT * FROM authors"
    try:
        cursor.execute(query)
    except:
        cnx.close()
        return (False, "the query didn't work")
    dataset = [ i for i in cursor]
    cnx.close()
    return dataset

# get all blogposts
def getBlogPosts():
    # connecting to database
    try:
        cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database blog_post")
    # cursor for querying in database
    cursor = cnx.cursor()
    query = "SELECT * FROM blog_posts"
    try:
        cursor.execute(query)
    except:
        cnx.close()
        return (False, "the query didn't work")
    dataset = [ {'post_id': i[0], 'post_author': getAuthor(i[1])[0][1], 'post_title': i[2], 'post_body': i[3], 'post_tag': i[4] } for i in cursor]
    cnx.close()
    return dataset

def getAuthorPosts(id):
        # connecting to database
    try:
        cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database blog_post")
    # cursor for querying in database
    cursor = cnx.cursor()
    query = f"SELECT * FROM blog_posts WHERE author_id = {id}"
    try:
        cursor.execute(query)
    except:
        cnx.close()
        return (False, "the query didn't work")
    dataset = [ {'post_id': i[0], 'post_author': getAuthor(id)[0][1], 'post_title': i[2], 'post_body': i[3], 'post_tag': i[4] } for i in cursor]
    cnx.close()
    return dataset

#  get blogpost with id
def getPost(id):
    # connecting to database
    try:
        cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database blog_post")
    # cursor for querying in database
    cursor = cnx.cursor()
    query = f"SELECT * FROM blog_posts WHERE post_id = {id}"
    try:
        cursor.execute(query)
    except:
        cnx.close()
        return (False, "the query didn't work")
    dataset = [ i for i in cursor] 
    cnx.close()
    return dataset 

# get author with id
def getAuthor(id):
    # connecting to database
    try:
        cnx = mysql.connector.connect(user='root', password='test30',host='127.0.0.1',database='blog')
    except:
        return (False, "couldn't connect to database author")
    # cursor for querying in database
    cursor = cnx.cursor()
    query = f"SELECT * FROM authors WHERE author_id = {id}"
    try:
        cursor.execute(query)
    except:
        cnx.close()
        return (False, "the query didn't work")
    dataset = [ i for i in cursor] 
    cnx.close()
    return dataset

# get user id if exists
def checkUser(user_name, user_password):
    print(user_name, user_password)
    dataset = getAuthors()
    for user in dataset:

        if user_name == user[1] and hashit.comparehashedpassword(user_password, user[2]):
            return [True, user[0]]
    return [False, 0]