## About the helm charts

The helm charts are under `chart/timer` and `charts/auth` are the final results of the following processes.

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
