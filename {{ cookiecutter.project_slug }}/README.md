# LocalStack {{ cookiecutter.api_name }} Extension

{{ cookiecutter.project_short_description }}


## Run this extension in Dev Mode
```sh
# Login
localstack login
# Initialize the extensions
localstack extensions init
# Enable the dev mode for this extension
localstack extensions dev enable ./
# Run LocalStack in Extensions Dev Mode
DEBUG=1 EXTENSION_DEV_MODE=1 LOCALSTACK_API_KEY=... localstack start
```