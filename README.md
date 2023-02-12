## Tasker

### Start the project

You can use docker or install python 3.10 on your local machine.

First you need to access to the container
```commandline
docker build -t tasker .
```

### Run the project in windows

```commandline
docker run --rm --env-file .env -p 80:80 -it -v ${PWD}:/app tasker bash
```

### Start testing

You need to install the test dependencies
```commandline
pip install .[test]
```
Then to run the tests you can execute
```commandline
coverage run -m pytest tests/ 
```

### FAQ

#### If fails to run the program you need to execute
```commandline
pip install .
```

#### If you want to see the report generated
```commandline
coverage report -m
```