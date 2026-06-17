import http.server
import socketserver
import json
import base64
import os

PORT = 8080
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/save-config':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Validate JSON before saving
                config_data = json.loads(post_data.decode('utf-8'))
                with open('site-config.json', 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
                
        elif self.path == '/api/upload-image':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename')
                base64_data = data.get('image') # format: data:image/jpeg;base64,.....
                
                if not filename or not base64_data:
                    raise ValueError("Missing filename or image data")
                    
                # Extract the base64 part
                header, encoded = base64_data.split(",", 1)
                image_data = base64.b64decode(encoded)
                
                # Make sure images directory exists
                os.makedirs('images', exist_ok=True)
                filepath = os.path.join('images', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "url": filepath}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
