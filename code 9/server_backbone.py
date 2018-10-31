#coding=utf-8
'''Simple Web Server Impelmentation
1 - do request/response 
2 - create a page based on template and return server status
3 - handle static html request and error
4 - directory with/no index html based on cases, path vs file
5 - CGI Common Gateway Interface (CGI) support
4 - support file download including css, js, txt
6 - support streaming video
'''
import sys
from http.server import HTTPServer,BaseHTTPRequestHandler
import os
import subprocess

PORT = 8111

class ServerException(Exception):
    '''For internal error reporting.'''
    pass

class case_no_file(object):
    '''File or directory does not exist.'''

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

class case_cgi_file(object):
    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')

    def act(self, handler):
        # run python script
        cmd = 'python '+ handler.full_path
        p = subprocess.Popen(cmd, shell=True, 
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # get script result
        child_stdin, child_stdout = p.stdin, p.stdout
        child_stdin.close()
        data = child_stdout.read()
        child_stdout.close()
        #send
        handler.send_content(data)                                 
        
class case_existing_file(object):
    '''File exists.'''
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        handler.handle_file(handler.full_path)

class case_existing_downloadable_file(object):
    """docstring for ClassName"""
    def test(self, handler):
        if os.path.isfile(handler.full_path):
            file, ext  = handler.full_path.split('.')
            if ext in ('txt','pdf'):
                return True
        return False

    def act(self, handler):
        print(handler.full_path)
        handler.handle_file(handler.full_path,content_type='application/octet-stream')
        
class case_directory_index_html(object):
    def index_path(self,handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self,handler):
        return  os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))

    def act(self,handler):
        handler.handle_file(self.index_path(handler))
        

class case_existing_file(object):
    def test(self,handler):
        return os.path.isfile(handler.full_path)

    def act(self,handler):
        handler.handle_file(handler.full_path)


class case_always_fail(object):
    def test(self, handler):
        return True
    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.full_path))


class RequestHandler(BaseHTTPRequestHandler):
    '''Handle HTTP requests by returning a fixed 'page'.'''

    # How to display an error.
    # http://127.0.0.1:8111/josh           not found
    # http://127.0.0.1:8111/               index.html is displyed
    # http://127.0.0.1:8111/index.html     index.html is displyed
    # http://127.0.0.1:8111/subdir         display unkown
    # txt file, is not download
    # http://127.0.0.1:8111/simple.py  .py file 
    Cases =[
    case_no_file(),
    case_cgi_file(),
    case_existing_downloadable_file(),
    case_existing_file(),
    case_directory_index_html(),
    case_always_fail()]

    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
    # Handle a GET request.
    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path

            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)
    
    def handle_file(self, full_path, content_type="text/html"):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content, content_type=content_type)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def handle_error(self,msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(bytes(content,'utf-8'), 404)

    def send_content(self, content, status=200, content_type="text/html"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        server_address = ('', PORT)
        server = HTTPServer(server_address, RequestHandler)
        print('strating the web server...127.0.0.1:'+str(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server...')
        server.socket.close()    
