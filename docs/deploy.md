# Deploy

## Setup k8s namespace

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

## Deploy `timer` service:

You can use `helm upgrade --install` to upgrade and install if chart doesn't exist.

```bash
cd timer
helm upgrade --install timer ./helm/timer  --namespace <name_it>
```

## Deploy `auth` service:

```bash
cd timer
helm upgrade --install auth ./helm/auth  --namespace <name_it>
```
