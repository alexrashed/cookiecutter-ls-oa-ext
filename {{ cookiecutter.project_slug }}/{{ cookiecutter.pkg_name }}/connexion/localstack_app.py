import logging

from connexion.apps.abstract import AbstractApp
from flask.helpers import get_root_path
from localstack.extensions.api.http import RouteHandler, Router

from {{ cookiecutter.pkg_name }}.connexion.localstack_api import LocalStackApi

LOG = logging.getLogger(__name__)


class LocalStackApp(AbstractApp):
    def __init__(self, import_name, router: Router[RouteHandler], **kwargs):
        self.router = router
        super().__init__(import_name, LocalStackApi, **kwargs)

    def create_app(self):
        pass

    def get_root_path(self):
        return get_root_path(self.import_name)

    def set_errors_handlers(self):
        pass

    def add_api(self, specification, **kwargs):
        LOG.info("Adding API: %s", specification)
        api = super().add_api(specification, **kwargs)
        for rule in api.rules:
            LOG.error("Adding route rule: %s", rule)
            self.router.add_rule(rule)
        return api

    def run(self, port=None, server=None, debug=None, host=None, **options):
        pass
