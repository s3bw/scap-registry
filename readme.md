
<h1 align="center">
  Scap Registry
</h1>

<h4 align="center">
  Server side application for note storage.
</h4>

## Setup local debugger for development

```bash
bash start_debugger.sh
```

## Running tests

requirements:
- tox
- pytest
- flake8

```
tox
```

## Running the Docker Container

```
docker build -t scap-registry .
docker container run -d -p 5000:5000 --name cloud scap-registry
```

Stop container process

```
docker container rm cloud -f
```
