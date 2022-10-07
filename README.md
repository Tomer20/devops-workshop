# DevOps Workshop: Helm

In this workshop we will simulate an operation of two python services, on Kubernetes, using Helm and Docker.

## Prerequisites

- kubectl (tested on v1.14)

- helm cli (tested on v2.12)

- docker engine

- Kubernetes environment (local, cloud, managed, on-prem, whatever v1.14) with nginx ingress controller


## Docs:

- [Timer](./timer/README.md)

- [Auth](./auth/README.md)

- [Docker build](./docs/build.md)

- [About the helm charts](./docs/helm.md)

- [Deploy](./docs/deploy.md)

## Accessing the endpoint

After deployed, curl the ingress host you configured in `auth` helm chart (devops-ws.example.io):

```bash
$ # get human time
$ curl -X GET http://devops-ws.example.io/datetime/asia/jerusalem -H "k8s-ws: user_a"
{"body": {"datetime": "2020-06-22T21:15:11.804696+03:00"}}

$ # get epochtime time
$ curl -X GET http://devops-ws.example.io/epochtime/asia/jerusalem -H "k8s-ws: user_a"
{"body": {"epochtime": 1592849876}}
```
