# Installation

## Install and run (without docker)

1. Install dependencies

   ```
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

2. Run server

   ```
   python3 run.py
   ```

## Install and run (with docker)

1. Build image

   tags image as file-explorer

   ```
   docker build -t file-explorer .
   ```

2. Run image

   binds to port 8000 on container

   ```
   docker run --publish 8000:8000 file-explorer
   ```

3. Curl command from outside container

   ```
   curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/
   ```
