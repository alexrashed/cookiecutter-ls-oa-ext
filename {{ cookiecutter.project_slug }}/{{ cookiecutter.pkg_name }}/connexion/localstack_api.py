from connexion.apis.abstract import AbstractAPI
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.apis.flask_api import FlaskSecurityHandlerFactory
from connexion.apis import flask_utils
from connexion.jsonifier import Jsonifier
from localstack.extensions.api.http import Request, Response
from werkzeug.routing import Rule
from {{ cookiecutter.pkg_name }}.encoder import JSONEncoder
import logging

LOG = logging.getLogger(__name__)


class LocalStackApi(AbstractAPI):
    rules = list()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_openapi_json(self):
        # TODO not implemented
        pass

    def add_openapi_yaml(self):
        # TODO not implemented
        pass

    def add_swagger_ui(self):
        # TODO not implemented
        pass

    def add_auth_on_not_found(self, security, security_definitions):
        # TODO not implemented
        pass

    @staticmethod
    def make_security_handler_factory(pass_context_arg_name):
        # TODO not implemented, just using flask implementation?
        return FlaskSecurityHandlerFactory(pass_context_arg_name)

    @classmethod
    def get_request(self, req: Request, **params):
        context_dict = {}
        request = ConnexionRequest(
            req.url,
            req.method,
            headers=req.headers,
            form=req.form,
            query=req.args,
            body=req.get_data(),
            json_getter=lambda: req.get_json(silent=True),
            files=req.files,
            path_params=params,
            context=context_dict,
            cookies=req.cookies,
        )
        LOG.debug('Getting data and status code',
                     extra={
                         'data': request.body,
                         'data_type': type(request.body),
                         'url': request.url
                     })
        return request

    @classmethod
    def get_response(cls, response, mimetype=None, request=None):
        return cls._get_response(response, mimetype=mimetype, extra_context={"url": request.url})

    @classmethod
    def _is_framework_response(cls, response):
        return isinstance(response, Response)

    @classmethod
    def _framework_to_connexion_response(cls, response: Response, mimetype):
        return ConnexionResponse(
            status_code=response.status_code,
            mimetype=response.mimetype,
            content_type=response.content_type,
            headers=response.headers,
            body=response.get_data() if not response.direct_passthrough else None,
            is_streamed=response.is_streamed
        )

    @classmethod
    def _connexion_to_framework_response(cls, response, mimetype, extra_context=None):
        framework_response = cls._build_response(
            mimetype=response.mimetype or mimetype,
            content_type=response.content_type,
            headers=response.headers,
            status_code=response.status_code,
            data=response.body,
            extra_context=extra_context,
        )

        return framework_response

    @classmethod
    def _build_response(cls, data, mimetype, content_type=None, status_code=None, headers=None, extra_context=None):
        if cls._is_framework_response(data):
            # TODO this is weird?
            return data

        data, status_code, serialized_mimetype = cls._prepare_body_and_status_code(data=data,
                                                                                   mimetype=mimetype,
                                                                                   status_code=status_code,
                                                                                   extra_context=extra_context)
        framework_response = Response()
        framework_response.status_code = status_code
        framework_response.data = data
        framework_response.mimetype = mimetype or serialized_mimetype
        framework_response.headers = headers or {}
        # TODO doesn't work?!
        # framework_response.content_type = content_type
        return framework_response

    def _add_operation_internal(self, method, path, operation):
        # TODO this doesn't add the prefix yet (f.e. v1)
        operation_id = operation.operation_id

        flask_path = flask_utils.flaskify_path(path, operation.get_path_parameter_types())

        LOG.error('... Adding %s %s -> %s', method.upper(), flask_path, operation_id,
                     extra=vars(operation))

        function = operation.function

        # create a "match any" host url?
        host = "<__host__>"
        self.rules.append(Rule(string=flask_path, endpoint=function, methods=[method], host=host))

    @classmethod
    def _set_jsonifier(cls):
        cls.jsonifier = Jsonifier(cls=JSONEncoder)