
<h1 align="center">
  Scap Registry
</h1>

<h4 align="center">
  Server side application for note storage.
</h4>

## Requirements

```bash
pip install flask
pip install requests
```

## Setup debugger for development

```bash
export FLASK_APP=scap_registry/app.py
export FLASK_DEBUG=1
python -m flask run
```

To do list:
[X] create endpoints for separate meta data JSONs
[ ] create endpoint for constructing full meta data JSON
[ ] move the json encoder from mock_usage to utils
[ ] implement this in foolscap
[ ] import from root instead of having relative imports
