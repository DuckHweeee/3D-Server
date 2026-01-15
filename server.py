#!/usr/bin/env python3
"""
Simple HTTP Server for Unity WebGL builds.
Handles proper MIME types and headers required by Unity WebGL.
"""

import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = "Build"  # Default Unity WebGL build folder


class UnityWebGLHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with proper MIME types for Unity WebGL."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()
    
    def guess_type(self, path):
        """Return proper MIME types for Unity WebGL files."""
        # Unity WebGL specific MIME types
        unity_types = {
            '.unityweb': 'application/octet-stream',
            '.wasm': 'application/wasm',
            '.wasm.gz': 'application/wasm',
            '.wasm.br': 'application/wasm',
            '.js.gz': 'application/javascript',
            '.js.br': 'application/javascript',
            '.data': 'application/octet-stream',
            '.data.gz': 'application/octet-stream',
            '.data.br': 'application/octet-stream',
            '.symbols.json': 'application/json',
            '.symbols.json.gz': 'application/json',
            '.symbols.json.br': 'application/json',
        }
        
        path_lower = path.lower()
        for ext, mime_type in unity_types.items():
            if path_lower.endswith(ext):
                return mime_type
        
        return super().guess_type(path)
    
    def do_GET(self):
        """Handle GET requests with proper encoding headers."""
        path = self.translate_path(self.path)
        
        # Add Content-Encoding header for compressed files
        if path.endswith('.gz'):
            self.send_header_on_compressed = 'gzip'
        elif path.endswith('.br'):
            self.send_header_on_compressed = 'br'
        else:
            self.send_header_on_compressed = None
        
        super().do_GET()
    
    def send_head(self):
        """Send headers with proper encoding for compressed files."""
        path = self.translate_path(self.path)
        
        if os.path.exists(path):
            if path.endswith('.gz'):
                # Serve gzip compressed files
                self.send_response(200)
                self.send_header('Content-Encoding', 'gzip')
                self.send_header('Content-Type', self.guess_type(path))
                self.send_header('Content-Length', os.path.getsize(path))
                self.end_headers()
                return open(path, 'rb')
            elif path.endswith('.br'):
                # Serve brotli compressed files  
                self.send_response(200)
                self.send_header('Content-Encoding', 'br')
                self.send_header('Content-Type', self.guess_type(path))
                self.send_header('Content-Length', os.path.getsize(path))
                self.end_headers()
                return open(path, 'rb')
        
        return super().send_head()


def main():
    global PORT, DIRECTORY
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            DIRECTORY = sys.argv[1]
    
    if len(sys.argv) > 2:
        DIRECTORY = sys.argv[2]
    
    # Check if directory exists
    if not os.path.exists(DIRECTORY):
        print(f"Warning: Directory '{DIRECTORY}' does not exist.")
        print("Creating directory structure...")
        os.makedirs(DIRECTORY, exist_ok=True)
        
        # Create a placeholder index.html
        placeholder_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unity WebGL Server</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0d0d1a 100%);
            color: #e4e4e7;
            overflow-x: hidden;
        }
        
        /* Animated background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        
        .bg-animation::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(74, 222, 222, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(168, 85, 247, 0.08) 0%, transparent 40%);
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, -30px) rotate(5deg); }
            66% { transform: translate(-20px, 20px) rotate(-5deg); }
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 24px;
        }
        
        /* Header */
        .header {
            text-align: center;
            margin-bottom: 60px;
        }
        
        .logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            border-radius: 28px;
            margin-bottom: 32px;
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3),
                        0 0 80px rgba(139, 92, 246, 0.2);
            animation: pulse 3s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3), 0 0 80px rgba(139, 92, 246, 0.2); }
            50% { transform: scale(1.02); box-shadow: 0 25px 50px rgba(99, 102, 241, 0.4), 0 0 100px rgba(139, 92, 246, 0.3); }
        }
        
        .logo svg {
            width: 50px;
            height: 50px;
            fill: white;
        }
        
        h1 {
            font-size: 2.75rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #a1a1aa;
            font-weight: 400;
        }
        
        /* Status Card */
        .status-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 32px;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .status-indicator {
            width: 56px;
            height: 56px;
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(34, 197, 94, 0.3);
        }
        
        .status-indicator svg {
            width: 28px;
            height: 28px;
            fill: white;
        }
        
        .status-text h3 {
            font-size: 1.25rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 4px;
        }
        
        .status-text p {
            color: #71717a;
            font-size: 0.95rem;
        }
        
        /* Instructions */
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #a1a1aa;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 20px;
        }
        
        .steps {
            display: grid;
            gap: 16px;
            margin-bottom: 40px;
        }
        
        .step {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            align-items: flex-start;
            gap: 20px;
            transition: all 0.3s ease;
        }
        
        .step:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateX(8px);
        }
        
        .step-number {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            color: #a78bfa;
            flex-shrink: 0;
        }
        
        .step-content h4 {
            font-size: 1.05rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 6px;
        }
        
        .step-content p {
            color: #71717a;
            font-size: 0.9rem;
            line-height: 1.6;
        }
        
        /* Files Card */
        .files-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            padding: 32px;
        }
        
        .files-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .files-header svg {
            width: 24px;
            height: 24px;
            fill: #6366f1;
        }
        
        .files-header h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: #ffffff;
        }
        
        .file-tree {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
            padding: 20px 24px;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            font-size: 0.85rem;
            line-height: 1.8;
        }
        
        .file-tree .folder {
            color: #6366f1;
        }
        
        .file-tree .file {
            color: #a1a1aa;
        }
        
        .file-tree .required {
            color: #22c55e;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 32px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .footer p {
            color: #52525b;
            font-size: 0.85rem;
        }
        
        .footer a {
            color: #6366f1;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .footer a:hover {
            color: #818cf8;
        }
        
        /* Responsive */
        @media (max-width: 640px) {
            .container {
                padding: 40px 16px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .status-card {
                flex-direction: column;
                text-align: center;
            }
            
            .step {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="container">
        <header class="header">
            <div class="logo">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
            </div>
            <h1>Unity WebGL Server</h1>
            <p class="subtitle">Ready to serve your 3D experience</p>
        </header>
        
        <div class="status-card">
            <div class="status-indicator">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
            </div>
            <div class="status-text">
                <h3>Server Running</h3>
                <p>Waiting for Unity WebGL build files in the Build folder</p>
            </div>
        </div>
        
        <h2 class="section-title">Getting Started</h2>
        
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>Build Your Unity Project</h4>
                    <p>In Unity, go to File → Build Settings, select WebGL platform, configure your settings, and click Build.</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>Copy Build Files</h4>
                    <p>Move the entire contents of your Unity WebGL build output into the <strong>Build</strong> folder.</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>Refresh This Page</h4>
                    <p>Once your files are in place, refresh this page to launch your 3D application.</p>
                </div>
            </div>
        </div>
        
        <div class="files-card">
            <div class="files-header">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
                </svg>
                <h3>Expected File Structure</h3>
            </div>
            <div class="file-tree">
                <span class="folder">Build/</span><br>
                &nbsp;&nbsp;├── <span class="required">index.html</span><br>
                &nbsp;&nbsp;├── <span class="folder">Build/</span><br>
                &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="file">YourGame.loader.js</span><br>
                &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="file">YourGame.framework.js</span><br>
                &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="file">YourGame.data</span><br>
                &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="file">YourGame.wasm</span><br>
                &nbsp;&nbsp;└── <span class="folder">TemplateData/</span><br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── <span class="file">(styles, icons...)</span>
            </div>
        </div>
        
        <footer class="footer">
            <p>Python Unity WebGL Server • <a href="https://docs.unity3d.com/Manual/webgl-building.html" target="_blank">Unity WebGL Documentation</a></p>
        </footer>
    </div>
</body>
</html>"""
        with open(os.path.join(DIRECTORY, 'index.html'), 'w') as f:
            f.write(placeholder_html)
    
    # Start server
    with socketserver.TCPServer(("", PORT), UnityWebGLHandler) as httpd:
        print(f"╔══════════════════════════════════════════════════╗")
        print(f"║       Unity WebGL Server                         ║")
        print(f"╠══════════════════════════════════════════════════╣")
        print(f"║  Serving from: {DIRECTORY:<33} ║")
        print(f"║  URL: http://localhost:{PORT:<25} ║")
        print(f"╠══════════════════════════════════════════════════╣")
        print(f"║  Press Ctrl+C to stop the server                 ║")
        print(f"╚══════════════════════════════════════════════════╝")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
            sys.exit(0)


if __name__ == "__main__":
    main()
