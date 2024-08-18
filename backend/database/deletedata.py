import mysql.connector 
import config
import mysql.connector.cursor

def deleteBlogPost(id):
    try:
        cnx = mysql.connector.connect(user = config.USER, password = config.PASSWORD, host = config.HOST, database = config.DATABASE)
    except:
        return (False, "couldn't connect to database")
    
    query = f"DELETE FROM blog_posts WHERE post_id = {id}"
    cursor = mysql.connector.cursor()

    # delete data
    try:
        cursor.execute(query)
    except:
        return (False, "query couldn't be executed")
    
    return (True, f"blog post id {id} deleted")

