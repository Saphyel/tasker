import contextlib

from litestar import Controller, get, post, Router, Request
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.exceptions import NotAuthorizedException
from litestar.params import Body
from litestar.response import Template, Redirect

from tasker.config import app_settings
from tasker.model import TaskInput, Search, Pagination, SortEnum
from tasker.repository import TaskRepository, task_repository


class TasksViewController(Controller):
    tags = ["View"]

    @get()
    async def index(
        self,
        repository: TaskRepository,
        token: str,
        tag: str | None,
        limit: int = 10,
        page: int = 1,
        sort: str = SortEnum.newest,
    ) -> Template:
        if not app_settings.token == token:
            raise NotAuthorizedException()

        return Template(
            template_name="index.html",
            context={
                "token": token,
                "data": repository.find(Search(tag=tag), Pagination(limit=limit, page=page, sort=sort)),
            },
        )

    @get(path="/add")
    async def add(self, token: str) -> Template:
        if not app_settings.token == token:
            raise NotAuthorizedException()

        return Template(template_name="task.html", context={"token": token})

    @post(path="/add")
    async def new(
        self,
        repository: TaskRepository,
        token: str,
        request: Request,
        form: TaskInput | None = Body(media_type=RequestEncodingType.URL_ENCODED),
    ) -> Redirect:
        if not app_settings.token == token:
            raise NotAuthorizedException()

        if not form:
            request.logger.info(request.headers.dict()["content-type"])
            form = TaskInput(**await request.form())
        repository.insert(form)
        return Redirect(path=f"/?token={token}")


@get(path="healthcheck", cache=False, tags=["Misc"])
async def health_check(repository: TaskRepository) -> str:
    with contextlib.suppress(Exception):
        if repository.check_health():
            return "OK"
    raise ConnectionError("DB not ready.")


view_router = Router(
    path="",
    route_handlers=[TasksViewController, health_check],
    dependencies={"repository": Provide(task_repository, sync_to_thread=False)},
)
