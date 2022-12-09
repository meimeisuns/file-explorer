# Introduction

This is a simple file explorer app that allows you to:

1. `GET` a file or directory's contents

2. `POST` a new file or directory

# Install and Run

## Run for Manual Testing

1. Install Docker

   Make sure you have [docker](https://docs.docker.com/get-docker/) installed.

2. Build image

   Run the following command in the root of this repository to build and tag the image as `file-explorer`. We will be using the base image for manual testing.

   ```
   docker build -t file-explorer --target base .
   ```

3. Run container

   Run the following command to bind port 8000 on the container to your local port 8000 to curl access the flask server for manual testing. You can either specify a starting directory through an environment variable, OR let it default to the home directory in the container.

   Run this command to use the container's home directory:

   ```
   docker run --publish 8000:8000 file-explorer
   ```

   **OR** run this command to specify a starting directory.

   ```
   docker run --publish 8000:8000 -e DIR=/tests/sample_dir/ file-explorer
   ```

4. Run curl from outside the container

   Here are some sample curl commands you can use from the root directory of this repository to browse the file system in the container.

   This command will list contents of the starting directory:

   ```
   curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/
   ```

   This command will create a new directory named `hello` in the starting directory:

   ```
   curl -i -H "Content-Type: application/json" -X POST -d '{"type": "dir","name":"hello"}' http://localhost:8000/
   ```

   This will create a new file in the `hello` directory created in the above command:

   ```
   curl -i -H "Content-Type: application/json" -X POST -d '{"type": "file","name":"hello.txt","contents":"new text file"}' http://localhost:8000/hello/
   ```

   See [API guide](#how-to-use-api) for more details on querying.

## Run Tests

1. Build image

   Run the following command to build the test image. This will use the base image and simply run `pytest` instead of starting the flask server.

   ```
   docker build -t file-explorer --target test .
   ```

2. Run container

   Run the tests in the test container with testing directory passed in as a starting directory:

   ```
   docker run -e DIR=/tests/sample_dir/ file-explorer
   ```

   You should see a pytest session that shows you the progress of running all the tests.

# How to use API

This API supports two methods: `GET`, and `POST`.

## `GET` Requests

Query with the subpath of the file or directory you want to inspect relative to the starting directory. `GET` requests don't require any additional data.

There are two possible results you can receive from a `GET` request:

1. **Directory**

   Returns a list of files and directories, with the following attributes:

   - Name
   - Owner
   - Permissions (octal representation)
   - Size (in bytes)

   For example, to list the starting directory `/tests/sample_dir/`, query with curl using `http://localhost:8000/`:

   Sample curl command:

   ```
   curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/
   ```

   Sample result:

   ```
   [
      {
         "name": "baz.py",
         "owner": "root",
         "permissions": 33188,
         "size_bytes": 22
      },
      {
         "name": ".foo",
         "owner": "root",
         "permissions": 33188,
         "size_bytes": 35
      },
      {
         "name": "another_dir/",
         "owner": "root",
         "permissions": 16877,
         "size_bytes": 4096
      }
   ]
   ```

2. **File**

   Returns a single result of the file with the following attributes, all of which are the same attributes seen when listing the directory except for the added text attribute:

   - Name
   - Owner
   - Permissions (octal representation)
   - Size (in bytes)
   - Text

   For example, to inspect the contents of `baz.py` in the starting directory `/tests/sample_dir/`, query with curl using `http://localhost:8000/baz.py`:

   Sample curl command:

   ```
   curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/baz.py
   ```

   Sample result:

   ```
   {
      "name": "baz.py",
      "owner": "root",
      "permissions": 33188,
      "size_bytes": 22,
      "text": "print(\"hello world!\")\n"
   }
   ```

## `POST` Requests

Query with the subpath (relative to the starting directory of the directory where you want to create a new file or directory. Include JSON data with the following attributes:

- `type`: Required. Should be `dir` or `file`, depending on what you want to create.
- `name`: Required.
- `contents`: Required, only if `type` is `file`. This can be an empty string.

Make sure the subpath points to a valid directory. If the request is successful, you should see a confirmation like the below:

```
File hello.txt successfully created in /tests/sample_dir/.
```

# Discussion of Technologies

Here is the summary of the technologies used here:

- **Language**: Python
- **Framework**: Flask
- **Testing**: `pytest` and `unittest`
- **File exploring**: `pathlib`

The Flask framework was chosen as a lightweight and easy framework that is easy to get started in. It's great for smaller applications such as this one, but for applications that need to scale, Django REST framework is a much better choice as it comes with more powerful built in functionalities like serializers and input validation.

Two options were considered for file browsing: Python's `os` library, or the `pathlib` library. They largely have the same functionality, and `pathlib` even makes use of the `os` library. However, `pathlib`'s functionality is centered around their `Path` object, which is more readable and intuitive.

The tests are largely integration style tests that simply query a test client and checks if the results line up with what is expected. These tests are less dependent on the internal implementation of the API itself than unit tests would be. These tests run within the docker container.

# Suggestions for Future Work

This work is very simple application that could use a lot of improvement, including:

- Mocking a testing directory so as to not depend on the container environment variable for tests.

  Eliminating the environment variable would possibly require a combination of Python command line arguments and an `ARG` in the Dockerfile.

- Isolation of the testing environment between tests.

  This is most likely linked to the solution for test directory mocking.

- Handling files with no read permission.

  Attempting to list a directory where there aren't read permissions for a certain file could result in an error. This path needs more thorough testing a way to fail gracefully.
