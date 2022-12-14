import logging

from connexion.apps.flask_app import NumberConverter, IntegerConverter
from localstack.extensions.api import Extension
from localstack.extensions.api.http import RouteHandler, Router

from {{ cookiecutter.pkg_name }}.connexion.localstack_app import LocalStackApp

LOG = logging.getLogger(__name__)


class {{ cookiecutter.extension_class }}(Extension):
    name = "{{ cookiecutter.project_slug }}"

    def __init__(self):
        LOG.error("Initializing {{ cookiecutter.extension_class }}...")

    def update_gateway_routes(self, router: Router[RouteHandler]):
        LOG.debug("Updating gateway routes for {{ cookiecutter.extension_class }}...")
        router.url_map.converters["float"] = NumberConverter
        router.url_map.converters["int"] = IntegerConverter
        localstack_app = LocalStackApp(__name__, router=router, specification_dir="./openapi/")
        localstack_app.add_api('openapi.yaml', pythonic_params=True)