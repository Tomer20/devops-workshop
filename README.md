# DevOps Workshop: Helm

In this workshop we will simulate an operation of two-microservices environment using Kubernetes, Helm, and Docker, hosting an application composed of Flask.

## Prerequisites

- kubectl (tested on v1.14)

- helm cli (tested on v2.12)

- docker engine

- Kubernetes environment (local, cloud, managed, on-prem, whatever v1.14) with nginx ingress controller


## The microservices

A brief explanation of the deployed services.

### TIMER

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

### AUTH

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

## Create docker images

### TIMER

```bash
cd auth/
docker build . -t <your_repo>/timer:0.1
docker push <your_repo>/timer:0.1
```

### AUTH

```bash
cd auth/
docker build . -t <your_repo>/timer-auth:0.1
docker push <your_repo>/timer-auth:0.1
```

## Create helm charts

The helm charts under `./timer/helm/timer` and `./auth/helm/auth` are the final results of the following processes.

### TIMER

```bash
cd timer/helm
helm create timer
```

#### Edit values file `timer/values.yaml`:

Change the image repository and tag:

```yaml
.
.
image:
  repository: <your_repo>/timer
  tag: "0.1"
.
.
```

Add imagePullSecrets, it is the name of k8s dockerconfig secret with credentials to your docker repository (we will create it later):

```yaml
.
.
image:
  repository: <your_repo>/timer
  tag: "0.1"
  pullPolicy: IfNotPresent
  imagePullSecrets: docker
.
.
```

Add configmap values to be used as environment variables in the container:

```yaml
.
.
configMap:
  data:
    PORT: "8080"
    LOG_LEVEL: "info"
.
.
```

Make sure that the service port matches the environment variable `LOG_LEVEL`:

```yaml
.
.
service:
  type: ClusterIP
  port: 8080
.
.
```

#### Create configmap template `timer/templates/configmap.yaml`:

This will be a template configmap for environment variables.

The template will add all `configMap.data` entries from the values file `timer/values.yaml`.

```go
{{- if .Values.configMap.data -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "timer.fullname" . }}
data:
  {{- range $name, $value := .Values.configMap.data }}
    {{ $name }}: {{ $value | quote }}
  {{- end }}
{{- end -}}
```

#### Edit deployment template `auth/templates/deployment.yaml`:

Fix the `containerPort` to be templated, under `spec.template.spec.containers[0].ports`:

```yaml
.
.
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
.
.
```

Add `imagePullSecrets` under `spec.template.spec`:
    
```yaml
.
.
    spec:
      imagePullSecrets:
        - name: {{ .Values.image.imagePullSecrets }}
.
.
```

Add template for `envFrom`, to the attach environment variables from configmap to the container. under `spec.template.spec.containers[0]`:

```go
.
.
          {{- if .Values.configMap.data }}
          envFrom:
            {{- if .Values.configMap.data }}
            - configMapRef:
                name: {{ include "auth.fullname" . }}
            {{- end }}
          {{- end }}
.
.
```

### AUTH

```bash
cd auth/helm
helm create auth
```

#### Edit values file `auth/values.yaml`:

Change the image repository and tag:

```yaml
.
.
image:
  repository: <your_repo>/timer-auth
  tag: "0.1"
.
.
```

Add imagePullSecrets (as in `timer` service):

```yaml
.
.
image:
  repository: <your_repo>/timer-auth
  tag: "0.1"
  pullPolicy: IfNotPresent
  imagePullSecrets: docker
.
.
```

Add configmap values to be used as environment variables in the container:

```yaml
.
.
configMap:
  data:
    PORT: "8090"
    LOG_LEVEL: "info"
    TIMER_HOST: timer
    TIMER_PORT: "8080"
.
.
```

Make sure that the service port matches the environment variable `LOG_LEVEL`:

```yaml
.
.
service:
  type: ClusterIP
  port: 8090
.
.
```

Since the `auth` service will serve as our entrypoint to the app, we need to create an ingress.

To enable it we will use nginx ingress class (passed as an annotation), enable it, add route path and dns name:

```yaml
.
.
ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
  paths: ["/"]
  hosts:
    - devops-ws.your-domain.io
.
.
```

*I'm using [ExternalDNS](https://github.com/helm/charts/tree/master/stable/external-dns) for automatically creating records on Route53.*

#### Create configmap template `auth/templates/configmap.yaml`:

This will be a template configmap for environment variables.

The template will add all `configMap.data` entries from the values file `auth/values.yaml`.

```go
{{- if .Values.configMap.data -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "auth.fullname" . }}
data:
  {{- range $name, $value := .Values.configMap.data }}
    {{ $name }}: {{ $value | quote }}
  {{- end }}
{{- end -}}
```

#### Create configmap template `auth/templates/auth-cm.yaml`:

This template is a configmap composed of the `config.json` file.

```go
apiVersion: v1
kind: ConfigMap
metadata:
  name: jsonconfig
data:
  config.json: |-
{{ .Files.Get "files/config.json" | indent 4}}
```

#### Create `auth/files/config.json`:

This is our "authentication" file.

It contains a list of users which can recieve data from the app.

```bash
mkdir auth/files
cat << EOF > auth/files/config.json
{
    "auth_users": [
        "user_a",
        "user_b"
    ]
}
EOF
```

#### Edit deployment template `auth/templates/deployment.yaml`:

Fix the `containerPort` to be templated, under `spec.template.spec.containers[0].ports`:

```yaml
.
.
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
.
.
```

Add `imagePullSecrets` under `spec.template.spec`:
    
```yaml
.
.
    spec:
      imagePullSecrets:
        - name: {{ .Values.image.imagePullSecrets }}
.
.
```

Add template for `envFrom`, to the attach environment variables from configmap to the container. under `spec.template.spec.containers[0]`:

```go
.
.
          {{- if .Values.configMap.data }}
          envFrom:
            {{- if .Values.configMap.data }}
            - configMapRef:
                name: {{ include "auth.fullname" . }}
            {{- end }}
          {{- end }}
.
.
```

Add `volumeMount` to the container, under `spec.template.spec.containers[0]`:

```yaml
.
.
          volumeMounts:
          - name: config-volume
            mountPath: /config.json
            subPath: config.json
.
.
```

Add `volumes` to the deployment, under `spec.template.spec`:

```yaml
.
.
      volumes:
      - name: config-volume
        configMap:
          name: jsonconfig
          items:
          - key: config.json
            path: config.json
.
.
```

## Deploy

### Setup k8s namespace

Create the namespace:

```bash
kubectl create namespace <name_it>
```

Create dockerconfig secret:

```bash
kubectl create secret docker-registry regcred \
  --namespace <name_it> \
  --docker-server=<your-registry-server> \
  --docker-username=<your-name> \
  --docker-password=<your-pword> \
  --docker-email=<your-email>
```

### Deploy `timer` service:

You can use `helm upgrade --install` to upgrade and install if chart doesn't exist.

```bash
cd timer
helm upgrade --install timer ./helm/timer  --namespace <name_it>
```

### Deploy `auth` service:

```bash
cd timer
helm upgrade --install auth ./helm/auth  --namespace <name_it>
```

## Testing the service

The service is now available on the host you configured in `auth` helm chart (devops-ws.your-domain.io).

Try curl it:

```bash
$ curl -X GET http://devops-ws.your-domain.io/datetime/asia/jerusalem -H "k8s-ws: user_a" # get human time
{"body": {"datetime": "2020-06-22T21:15:11.804696+03:00"}}

$ curl -X GET http://devops-ws.your-domain.io/epochtime/asia/jerusalem -H "k8s-ws: user_a" # get epochtime time
{"body": {"epochtime": 1592849876}}
```
