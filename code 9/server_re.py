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

#-------------------------------------------------------------------------------

class ServerException(Exception):
    '''For internal error reporting.'''
    pass

#-------------------------------------------------------------------------------

class base_case(object):
    '''Parent for case handlers.'''

    def handle_file(self, handler, full_path, status = 200, content_type="text/html"):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content, status = status, content_type=content_type)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'

#-------------------------------------------------------------------------------

class case_no_file(base_case):
    '''File or directory does not exist.'''

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

#-------------------------------------------------------------------------------

class case_cgi_file(base_case):
    '''Something runnable.'''

    def run_cgi(self, handler):
        cmd = "python " + handler.full_path
        p = subprocess.Popen(cmd, shell=True, 
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        child_stdin, child_stdout = p.stdin, p.stdout
        child_stdin.close()
        data = child_stdout.read()
        child_stdout.close()
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
               handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)

#-------------------------------------------------------------------------------

class case_existing_file(base_case):
    '''File exists.'''

    def test(self, handler):
        if os.path.isfile(handler.full_path):
            file, ext  = handler.full_path.split('.')
            if ext not in ('mp4','mp3','txt'):
                return True
        return False

    def act(self, handler):
        #text/css application/x-javascript
        file, ext  = handler.full_path.split('.')
        if ext == 'css':        
            self.handle_file(handler, handler.full_path,content_type='text/css')
        elif ext == 'js':
            self.handle_file(handler, handler.full_path,content_type='application/x-javascript')
        else:
            self.handle_file(handler, handler.full_path)

class case_existing_download_file(base_case):
    '''File exists.'''

    def test(self, handler):
        if os.path.isfile(handler.full_path):
            file, ext  = handler.full_path.split('.') #os.path.splitext(handler.full_path)
            if ext in ('txt'):
                return True
        return False

    def act(self, handler): #application/octet-stream
        self.handle_file(handler, handler.full_path,content_type='application/octet-stream')

class case_stream_file(base_case):
    '''File exists.'''

    def test(self, handler):
        if os.path.isfile(handler.full_path):
            file, ext  = handler.full_path.split('.') #os.path.splitext(handler.full_path)
            if ext in ('mp4'):
                return True
        return False

    def act(self, handler): #application/octet-stream

        f = open(handler.full_path, 'rb')
        fs = os.fstat(f.fileno())
        size = int(fs[6])        
        start_range = 0
        end_range = size
        if "Range" in handler.headers:
           
            s, e = handler.headers['range'][6:].split('-', 1)
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
                if el > 0:
                    end_range = int(e) + 1
            elif el > 0:
                ei = int(e)
                if ei < size:
                    start_range = size - ei
            handler.send_response(206)            
        else:
            handler.send_response(200)
        handler.send_header("Content-type", "video/mp4")
        handler.send_header("Content-Range", 'bytes ' + str(start_range) + '-' + str(end_range - 1) + '/' + str(size))
        handler.send_header("Content-Length", end_range - start_range)
        handler.send_header("Last-Modified", handler.date_time_string(fs.st_mtime))               
        handler.send_header("Accept-Ranges", "bytes")            
        handler.end_headers()

        print("Got values of ", start_range, " and ", end_range, "...\n")
        if f:
            f.seek(start_range, 0)
            chunk = 0x1000
            total = 0
            while chunk > 0:
                if start_range + chunk > end_range:
                    chunk = end_range - start_range
                try:
                    handler.wfile.write(f.read(chunk))
                except:
                    break
                total += chunk
                start_range += chunk
            f.close()
#-------------------------------------------------------------------------------

class case_directory_index_file(base_case):
    '''Serve index.html page for a directory.'''

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

#-------------------------------------------------------------------------------

class case_directory_no_index_file(base_case):
    '''Serve listing for a directory without an index.html page.'''

    # How to display a directory listing.
    Listing_Page = '''\
        <html>
        <body>
        <ul>
        {0}
        </ul>
        </body>
        </html>
        '''

    def list_dir(self, handler, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(e) for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            handler.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            handler.handle_error(msg)

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.list_dir(handler, handler.full_path)

#-------------------------------------------------------------------------------

class case_always_fail(base_case):
    '''Base case if nothing else worked.'''

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))

#-------------------------------------------------------------------------------

class RequestHandler(BaseHTTPRequestHandler):
    '''
    If the requested path maps to a file, that file is served.
    If anything goes wrong, an error page is constructed.
    '''

    Cases = [case_no_file(),
             case_cgi_file(),
             case_existing_download_file(),
             case_existing_file(),
             case_stream_file(),
             case_directory_index_file(),
             case_directory_no_index_file(),
             case_always_fail()]

    # How to display an error.
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    # Classify and handle request.
    def do_GET(self):
        try:

            # Figure out what exactly is being requested.
            self.full_path = os.getcwd() + self.path

            # Figure out how to handle it.
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        # Handle errors.
        except Exception as msg:
            self.handle_error(msg)

    # Handle unknown objects.
    def handle_error(self, msg):
        content = bytes(self.Error_Page.format(path=self.path, msg=msg),'utf8')
        self.send_content(content, 404)

    # Send actual content.
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
