# Install and Testing

1. Build image

   tags image as file-explorer

   ```
   docker build -t file-explorer .
   ```

2. Run image

   binds to port 8000 on container, can use port 8000 locally to curl access for manual testing. Defaults to home directory in container.

   ```
   docker run --publish 8000:8000 file-explorer
   ```

   Or use environment variable to specify directory in container to start from:

   ```
   docker run --publish 8000:8000 -e DIR=/explorer/ file-explorer
   ```

3. Curl command from outside container

   ```
   curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/
   ```
