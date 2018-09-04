# Face emotions (with Azure API)

Installation:

* Create `resources` folder in project root and in it a `config.yml` file with the following content:

```yaml
# Flask
FLASK_ENV:
  value: 'development'
FLASK_APP:
  value: 'viz_ai_image/app.py'
SECRET_KEY:
  value: '(\xec\x0cB\x0c\xa2\x1e\x7f\x00\xd8N\x9dk\xc5\x1e\xef\xdc\x0e\x18\x91K\x10\x96R'

# Face API
SUBSCRIPTION_KEY:
  value: AZURE_API_KEY

```

* Install `pyinvoke` with `pip install invoke`
* Run `inv build-venv`
* Run `inv run-app` to launch the app