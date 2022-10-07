# Timer

`timer` service is using `http://worldtimeapi.org` (thanks!) to get the current time at `continental/capital` in human time and in epoch time.

The service exposes three endpoints:

- `@app.route("/", methods=['GET'])`: for healthcheck usage

- `@app.route("/datetime/<continental>/<capital>", methods=['GET'])`: for human time

- `@app.route("/epochtime/<continental>/<capital>", methods=['GET'])`: for epoch time

This will be our `backend` service.

## Run it locally

```bash
$ cd timer/
$ pip3 install -r requirements.txt
$ python3 ./app/app.py

Server is starting
Serving on http://0.0.0.0:8080
```

### Testing the endpoint

Using curl:

```bash
$ # get human time
$ curl -X GET http://0.0.0.0:8080/datetime/asia/jerusalem
{"body": {"datetime": "2020-06-22T21:15:11.804696+03:00"}}

$ # get epochtime time
$ curl -X GET http://0.0.0.0:8080/epochtime/asia/jerusalem
{"body": {"epochtime": 1592849876}}
```

## Environment variables

| Variable  | Default | Options               |
|-----------|---------|-----------------------|
| PORT      | 8080    | Any valid port number |
| LOG_LEVEL | INFO    | INFO, DEBUG           |
