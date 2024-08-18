from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import backend.hashit as hashit
import backend.database.getdata as db
import backend.database.editdata as edit_db
import backend.tokenit as tokenit
from jinja2 import Environment, FileSystemLoader
import json
import jwt
import backend.modifydata as modify
from http.cookies import SimpleCookie

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # set header to response
    def settingheader(self, status,title, content_type, token=None):
        self.send_response(status)
        self.send_header(title ,content_type)
        if token:
            self.send_header('Set-Cookie', f'token={token}; HttpOnly')
        self.end_headers()

    #  render html file
    def render_template(self, template_name, context):
        env = Environment(loader=FileSystemLoader('./backend/frontend'))
        template = env.get_template(template_name)
        return template.render(context)

       
    # Verify token from cookie
    def verify_token(self):

        if "Cookie" in self.headers:
            cookie = SimpleCookie(self.headers["Cookie"])
            if "token" in cookie:
                token = cookie["token"].value
                # Decode the token and verify it
                user_data = tokenit.decodetokenn(token)
                if user_data:
                    return user_data  # Returns user info if valid
                else: 
                    return None
        return None  # Returns None if token is invalid or absent



    #  all POST request handled here
    def do_POST(self):
        # check if token exists
        try:
            user_data = self.verify_token()
            print(user_data)
        except jwt.exceptions.ExpiredSignatureError:
            user_data = None
            print('token expired')
            self.settingheader(303, 'Location', '/login')


        #  ========== /LOGIN
        if self.path == '/login' and self.command == 'POST':
            # get POST data
            content_length = int(self.headers['Content-Length'])
            byte_data = self.rfile.read(content_length)
            print(byte_data)
            data = modify.separate_key_data(byte_data)

            # send POST data
            if data[0]['user_name'] and data[1]['user_password']:

                # authenticate returns [exists, user_id]
                user_exists = db.checkUser(data[0]['user_name'], data[1]['user_password'])
                print(user_exists)

                # send token
                if user_exists[0]:
                    token = tokenit.tokenit(user_exists[1],data[0]['user_name'])
                    print(token)
                    # set header
                    self.settingheader(303,'Location', '/profile', token)
                else:
                    self.wfile.write(json.dumps({'info': 'failed','token': ''}).encode('utf-8'))



        #  ========== /SIGNUP 
        if self.path == '/signup' and self.command == 'POST':
            # get POST data
            content_length = int(self.headers['Content-Length'])
            byte_data = self.rfile.read(content_length)
            data = modify.separate_key_data(byte_data)
            
            # hash password
            hashedpass = hashit.hashpassword(data[1]['user_password'])
            # add to database
            name = data[0]['user_name']
            passw = hashedpass.decode('utf-8')
            author_added = edit_db.addAuthor(name, passw)
            # client response
            if author_added[0]:
                self.settingheader(303,'Location', '/login')
            else:
                self.wfile.write(json.dumps({'info': author_added[1]}).encode('utf-8'))



        # =========== /CREATEPOST
        if self.path == '/createpost' and self.command == 'POST':

            if user_data:
                # get POST data
                content_length = int(self.headers['Content-Length'])
                byte_data = self.rfile.read(content_length)

                # add new post to database
                data = modify.separate_key_data(byte_data)
                print(data)
                post_added = edit_db.addBlogPost(user_data['user_id'], data[0]['post_title'], data[1]['post_body'], data[2]['post_tag'])
                
                if post_added[0]:
                    #  create new token
                    token = tokenit.tokenit(user_data['user_id'],user_data['user_name'])
                    # set header
                    self.settingheader(200,'Location', '/profile', token)



        # =========== /UPDATEPOST
        if self.path == '/updatepost/:id' and self.command == 'POST':

            if user_data:
                #  read POST data
                content_length = int(self.headers['Content-Length'])
                byte_data = self.rfile.read(content_length)
                data = modify.separate_key_data(byte_data)
                print(data)

                # update data in database
                post_id = self.path.split('/')[-1]
                updated = edit_db.updateBlogPost(post_id, data[0]['post_title'], data[1]['post_body'], data[2]['post_tag'] )
                if updated[0]:
                    token = tokenit.tokenit(user_data['user_id'], user_data['user_name'])
                    self.settingheader(303, 'Location', '/profile', token)



        # ============ /UPDATEPROFILE
        if self.path == '/updateprofile' and self.command == 'POST':

            if user_data:
                #  read POST data
                content_length = int(self.headers['Content-Length'])
                byte_data = self.rfile.read(content_length)
                data = modify.separate_key_data(byte_data)
                print(data)

                # updata profile in database
                updated = edit_db.updateAuthor(user_data['user_id'], data[0]['user_name'], data[1]['user_password'])

                if updated[0]:
                    token = tokenit.tokenit(user_data['user_id'], data[0]['user_name'])
                    self.settingheader(303, 'Location', '/profile', token)
    



    def do_GET(self):
        # check if token exists
        try:
            user_data = self.verify_token()
            print(user_data)
        except jwt.exceptions.ExpiredSignatureError:
            user_data = None
            print('token expired')


        if self.path == '/' and self.command == 'GET':

            if user_data:
                token = tokenit.tokenit(user_data['user_id'], user_data['user_name'])
                # setting header
                self.settingheader(200, 'Content-type','text/html', token)
            else:
                print('this has ran')
                # setting header
                self.settingheader(200, 'Content-type','text/html')
            # get all blogposts
            content = {'data': db.getBlogPosts()}
            # read html file
            html = self.render_template('index.html', content)
            # send html file 
            self.wfile.write(html.encode('utf-8'))



        elif self.path == '/login' and self.command == 'GET':

            if user_data:
                token = tokenit.tokenit(user_data['user_id'], user_data['user_name'])
                self.settingheader(303, 'Location', '/profile', token)
            else:
                # setting header
                self.settingheader(200,'Content-type','text/html')
                # read html file
                html = self.render_template('login.html',{})
                # send html file 
                self.wfile.write(html.encode('utf-8'))



        elif self.path == '/signup' and self.command == 'GET':

            if user_data:
                token = tokenit.tokenit(user_data['user_id'], user_data['user_name'])
                self.settingheader(303, 'Location', '/profile', token)
            else:
                # setting header
                self.settingheader(200,'Content-type','text/html')
                # read html file
                html = self.render_template('signup.html',{})
                # send html file 
                self.wfile.write(html.encode('utf-8'))



        elif self.path == '/profile' and self.command == 'GET':

            if user_data:
                # new token 
                token = tokenit.tokenit(user_data['user_id'],user_data['user_name'])
                # setting header
                self.settingheader(200,'Content-type','text/html', token)
                # get all blogposts
                content = {'data': db.getAuthor(user_data['user_id']), 'posts': db.getAuthorPosts(user_data['user_id'])}
                # read html file
                html = self.render_template('profile.html', content)
                # send html file 
                self.wfile.write(html.encode('utf-8'))
            else:
                self.settingheader(303,'Location', '/login')



        elif self.path == '/createpost' and self.command == 'GET':

            if user_data:
                # new token 
                token = tokenit.tokenit(user_data['user_id'],user_data['user_name'])
                # setting header
                self.settingheader(200,'Content-type','text/html', token)
                # read html file
                html = self.render_template('createpost.html', {})
                # send html file 
                self.wfile.write(html.encode('utf-8'))
            else:
                self.settingheader(303,'Location', '/login')



        elif self.path == '/updatepost/:id' and self.command == 'GET':

            if user_data:
                post_id = self.path.split('/')[-1]
                # new token 
                token = tokenit.tokenit(user_data['user_id'],user_data['user_name'])
                # setting header
                self.settingheader(200,'Content-type','text/html', token)
                postdata = db.getPost(post_id)
                # read html file
                html = self.render_template('updatepost.html', {"data": postdata})
                # send html file 
                self.wfile.write(html.encode('utf-8'))
            else:
                self.settingheader(303,'Location', '/login')



        elif self.path == '/updateprofile' and self.command == 'GET':

            if user_data:
                # new token 
                token = tokenit.tokenit(user_data['user_id'],user_data['user_name'])
                # setting header
                self.settingheader(200,'Content-type','text/html', token)
                # get author data
                authorinfo = db.getAuthor(user_data['user_id'])
                # read html file
                html = self.render_template('updateprofile.html', {'data': authorinfo})
                # send html file 
                self.wfile.write(html.encode('utf-8'))
            else:
                self.settingheader(303,'Location', '/login')



        else:
            # set header
            self.settingheader(200,'Content-type','text/html')
            # read html file
            html = self.render_template('404.html', {})
            # send html file 
            self.wfile.write(html.encode('utf-8'))


