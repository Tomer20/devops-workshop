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

#### Run it locally

```bash
cd auth/
pip3 install -r requirements.txt
python3 ./app/app.py
```

##### Environment variables

- PORT: defaults to 8090

- LOG_LEVEL: one of "info" or "debug", defaults to "info"

- TIMER_HOST: hostname of `timer` service, defaults to "0.0.0.0"

- TIMER_PORT: port of `timer` service, defaults to "8080"
