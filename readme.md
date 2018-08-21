
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
bash app_debugger.sh
```

To do list:
- [X] create endpoints for separate meta data JSONs
- [X] Design Question: Encoding and Decoding on the client side?
   - It kinda has to be to get the datetime objects through a stream.
- [X] create endpoint for constructing full meta data JSON
- [ ] Write tests for end points.
- [ ] Add CI
- [ ] move the json encoder from mock_usage to foolscap
- [ ] implement this in foolscap
- [ ] import from root instead of having relative imports
