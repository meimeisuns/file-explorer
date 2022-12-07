# Install

## Run for Manual Testing

1. Build image

   tags image as file-explorer

   ```
   docker build -t file-explorer --target base .
   ```

2. Run image

   binds to port 8000 on container, can use port 8000 locally to curl access for manual testing. Defaults to home directory in container.

   ```
   docker run --publish 8000:8000 file-explorer
   ```

   Or use environment variable to specify directory in container to start from:

   ```
   docker run --publish 8000:8000 -e DIR=/tests/sample_dir/ file-explorer
   ```

3. Curl command from outside container

   See [API guide](#how-to-use-api) for more details.

   ```
   curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/
   ```

   creating a new directory:

   ```
   curl -i -H "Content-Type: application/json" -X POST -d '{"type": "dir","name":"hello"}' http://localhost:8000/
   ```

   creating a new file:

   ```
   curl -i -H "Content-Type: application/json" -X POST -d '{"type": "file","name":"hello.txt","contents":"new text file"}' http://localhost:8000/hello/
   ```

## Run Tests

1. Build image

   to build for test image, add target:

   ```
   docker build -t file-explorer --target test .
   ```

2. Run image

   run image with correct directory passed in:

   ```
   docker run -e DIR=/tests/sample_dir/ file-explorer
   ```

# How to use API

# Suggestions for Future Work

Improvements:

- mock testing directory to not depend on container environment variable
