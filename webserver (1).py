import http.server
import http.client
import urllib.parse
import base64
	
a=""

f = True
def keep_running():
        return f
        
class WebServer:        
        def __init__(self, port):
                self.port = port;
        
        def listen(self):
                server_address = ("", self.port)
                httpd = http.server.HTTPServer(server_address, WebServerRequestHandler)
                print("Web server started on port %s" % self.port)
                while keep_running():
                        httpd.handle_request()                
                                          
class WebClient:
        def myencode(self, str):
                bRes = base64.b64encode(str.encode('utf-8'))
                sRes = bRes.decode("utf-8")
                print("%s: %s" % (str, sRes))

        def mydecode(self, str):
                bRes = base64.b64decode(str.encode('utf-8'))
                sRes = bRes.decode("utf-8")
                print("%s: %s" % (str, sRes))	

        def get(self, host, path):
                conn = http.client.HTTPSConnection(host)
                conn.request('GET', path)
                resp = conn.getresponse()
                data = resp.read()
                conn.close()
                return data

class WebServerRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
                if self.path == '/':
                        self.send_response(302)
                        self.send_header("Location", "https://oauth.vk.com/authorize?client_id=5341594&display=page&redirect_uri=http://localhost:12346/verify&scope=friends,audio,notes&response_type=code&v=5.45")
                        self.end_headers()
                        self.wfile.write(("<h1>hello, %s %s!</h1>" % (self.path, self.client_address[0])).encode('utf-8'))
                        return
                if self.path.startswith("/verify"):
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(("<h1>hello, %s %s!</h1>" % (self.path, self.client_address[0])).encode('utf-8'))
                        global a
                        a = self.path.split('=')[1]
                        #print("https://oauth.vk.com/access_token?client_id=5341594&client_secret=BxRhBC146ZPHD7owDgCQ&redirect_uri=http://localhost:12346/verify&code=%s" % a)
                       
                        global f
                        f = False
                        
                       
if __name__ == "__main__":
                
        print("Start our web server...")
        ws = WebServer(12346)
        ws.listen()
        print(a)
        print("Test our web client...")
        wc = WebClient()
        spath =  "/access_token?client_id=5341594&client_secret=BxRhBC146ZPHD7owDgCQ&redirect_uri=http://localhost:12346/verify&code=%s" % a
        #print(spath)
        result = wc.get("oauth.vk.com", spath)
        print(result)
        at = result.decode('utf-8').split(',')[0].split(':')[1][1:-1]
        print("access_token = " + at)
        print("___________________________________________")
        print(wc.get("api.vk.com","/method/audio.get?owner_id=17345074&need_user=1&count=7&v=5.45&access_token=%s" % at))
        print("___________________________________________")
        print(wc.get("api.vk.com","/method/notes.get?user_id=49504326&count=3&count=1&sort=1&access_token=%s" % at))
        print("___________________________________________")
        
        wc.myencode("Elza")
        wc.myencode("Lesha")
        wc.mydecode("QW50b24=")




        
