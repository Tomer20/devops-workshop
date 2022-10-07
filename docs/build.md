# Build docker images

## TIMER

```bash
$ cd timer/
$ docker build -t <your_repo>/timer:0.0.1 -f Dockerfile ./timer
$ docker push <your_repo>/timer:0.0.1
```

## AUTH

```bash
$ cd auth/
$ docker build -t <your_repo>/auth:0.0.1 -f Dockerfile ./auth
$ docker push <your_repo>/auth:0.0.1
```
