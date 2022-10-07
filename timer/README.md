# Timer

`timer` microservice is using `http://worldtimeapi.org` (thanks!) to get the current time at `continental/capital` in human time and in epoch time.

The service exposes three endpoints:

- `@app.route("/", methods=['GET'])`: for healthcheck usage

- `@app.route("/datetime/<continental>/<capital>", methods=['GET'])`: for human time

- `@app.route("/epochtime/<continental>/<capital>", methods=['GET'])`: for epoch time

This will be our `backend` microservice.

#### Run it locally

```bash
cd timer/
pip3 install -r requirements.txt
python3 ./app/app.py
```

##### Environment variables

- PORT: defaults to 8080

- LOG_LEVEL: one of "info" or "debug", defaults to "info"
