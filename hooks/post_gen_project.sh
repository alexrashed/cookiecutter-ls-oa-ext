#!/bin/bash
set -euo pipefail
echo "Installing openapi-generator-cli..."
source ~/.nvm/nvm.sh
npm install @openapitools/openapi-generator-cli -g
echo "Generating Python API code based on {{ cookiecutter.openapi_url }}..."
openapi-generator-cli generate -i {{ cookiecutter.openapi_url }} -g python-flask -o ./target/openapi --additional-properties=packageName={{ cookiecutter.pkg_name }}
echo "Post-processing generated code..."
rm -rf target/openapi/{{ cookiecutter.pkg_name }}/__main__.py
rm -rf target/openapi/{{ cookiecutter.pkg_name }}/__init__.py
rm -rf target/openapi/{{ cookiecutter.pkg_name }}/test
mv target/openapi/{{ cookiecutter.pkg_name }}/* {{ cookiecutter.pkg_name }}/
rm -rf target
echo "Setting up python project..."
make clean clean-dist install dist