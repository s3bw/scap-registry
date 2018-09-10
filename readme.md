
<h1 align="center">
  Scap Registry
</h1>

<h4 align="center">
  Server side application for note storage.
</h4>

## Environments

| Name | Purpose |
| ---- | ------- |
| prod | production (runs with s3) |
| test | Running in ci |
| dev | For running locally |

## Setup local debugger for development

```bash
bash start_debugger.sh
```

## Running tests


```cmd
pip install setup.py dev
tox
```

## Running the Container

```bash
docker build -t scap-registry .

# Running development container
docker container run -d \
  -e APP_ENV=dev \
  -p 5000:5000 \
  --name cloud_dev scap-registry

# Running Production container
docker container run -d \
  -e APP_ENV=prod \
  -e S3_ACCESS_KEY=$S3_ACCESS_KEY \
  -e S3_SECRET_KEY=$S3_SECRET_KEY \
  -e S3_BUCKET=$S3_BUCKET \
  -p 5000:5000 \
  --name cloud_prod scap-registry
```

Stop container process

```
docker container rm cloud -f
```
