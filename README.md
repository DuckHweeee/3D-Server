# Unity WebGL 3D Building Server

A simple Python HTTP server configured to properly serve Unity WebGL builds.

## Quick Start

1. **Run the server:**
   ```bash
   python server.py
   ```

2. **Open in browser:**
   ```
   http://localhost:8000
   ```

## Usage

### Default (serves from `Build` folder on port 8000):
```bash
python server.py
```

### Custom port:
```bash
python server.py 3000
```

### Custom directory:
```bash
python server.py 8000 /path/to/your/webgl/build
```

## Unity WebGL Build Setup

1. In Unity, go to **File → Build Settings**
2. Select **WebGL** platform
3. Click **Build** and choose an output folder
4. Copy the build contents to the `Build` folder (or specify custom path)

### Expected folder structure:
```
3D-Server/
├── server.py
├── README.md
└── Build/
    ├── index.html
    ├── Build/
    │   ├── YourGame.loader.js
    │   ├── YourGame.framework.js(.gz/.br)
    │   ├── YourGame.data(.gz/.br)
    │   └── YourGame.wasm(.gz/.br)
    └── TemplateData/
        └── (style files, icons, etc.)
```

## Features

- ✅ Proper MIME types for Unity WebGL files (.wasm, .data, .unityweb)
- ✅ Support for gzip (.gz) and brotli (.br) compressed builds
- ✅ CORS headers enabled for development
- ✅ Cross-Origin isolation headers (required for SharedArrayBuffer/Threading)
- ✅ No external dependencies (uses Python standard library)

## Troubleshooting

### "Unable to load file" error
- Make sure the build files are in the correct directory
- Check browser console for specific file paths

### SharedArrayBuffer/Threading not working
- The server includes `Cross-Origin-Opener-Policy` and `Cross-Origin-Embedder-Policy` headers
- Use Chrome, Firefox, or Edge (Safari has limited support)

### Slow loading
- Use Unity's compression options (gzip or brotli) in Build Settings
- Enable "Decompression Fallback" if serving from servers without compression support

## Requirements

- Python 3.7 or higher
- No additional packages required
