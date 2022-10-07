# Auth

`auth` microservice will handle the request and forward it to `timer` microservice.

In order for the `auth` microservice to forward the request to `timer`:

- The request should contain an authentication header `{k8s-ws: <user>}`

- The provided `<user>` should be part of the `config.json` file

The `config.json` should be located outside `app` directory, the file's structure:

```json
{
    "auth_users": [
        "user_a",
        "user_b"
    ]
}
```

*Yes, our authentication service will be based on a config file.*

*Notice that this is just a sample service, authentication shouldn't be handled this way and it is not recommended to use this service for real authentication.*

The service exposes two endpoints:

- `@app.route("/", methods=['GET'])`: for healthcheck usage

- `@app.route("/<timetype>/<continental>/<capital>", methods=['GET'])`: the main endpoint

## Run it locally

```bash
$ cd auth/
$ pip3 install -r requirements.txt
$ python3 ./app/app.py

Server is starting
Serving on http://0.0.0.0:8090
```

## Environment variables

| Variable   | Default | Options                     |
|------------|---------|-----------------------------|
| PORT       | 8090    | Any valid port number       |
| LOG_LEVEL  | INFO    | INFO, DEBUG                 |
| TIMER_HOST | 0.0.0.0 | Hostname of `timer` service |
| TIMER_PORT | 8080    | Port of `timer` service     |
