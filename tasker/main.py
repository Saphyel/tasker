from pathlib import Path

from starlite import Starlite, CompressionConfig, LoggingConfig, TemplateConfig, Provide
from starlite.contrib.jinja import JinjaTemplateEngine
from starlite.middleware import LoggingMiddlewareConfig

from tasker.controllers import view_router

logging_middleware_config = LoggingMiddlewareConfig()

app = Starlite(
    route_handlers=[view_router],
    openapi_config=None,
    logging_config=LoggingConfig(),
    compression_config=CompressionConfig(backend="gzip", gzip_compress_level=6),
    middleware=[logging_middleware_config.middleware],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
