import mysql.connector 
import config
import mysql.connector.cursor

def deleteBlogPost(id):
    # connecting to database
    try:
        cnx = mysql.connector.connect(user = config.DATABASE_USER, password = config.DATABASE_PASSWORD,host = config.DATABASE_HOST,database = config.DATABASE)
    except:
        return (False, "couldn't connect to database")
    # query database
    cursor = cnx.cursor()
    query = f"DELETE FROM blog_posts WHERE post_id={int(id)}"
    try:
         cursor.execute(query)
         cnx.commit()
    except:
        cnx.close()
        return (False, "the updateauthor query didnt run")
    cnx.close()
    return (True, "success")

