import contextlib

from starlite import (
    Controller,
    get,
    post,
    Router,
    NotAuthorizedException,
    Template,
    Redirect,
    Body,
    RequestEncodingType,
    Provide,
    Request,
)

from tasker.model import TaskInput, Search, Pagination, SortEnum
from tasker.repository import TaskRepository, task_repository
from tasker.settings import app_settings


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
            raise NotAuthorizedException

        return Template(
            name="index.html",
            context={
                "token": token,
                "data": repository.find(Search(tag=tag), Pagination(limit=limit, page=page, sort=sort)),
            },
        )

    @get(path="/add")
    async def add(self, token: str) -> Template:
        if not app_settings.token == token:
            raise NotAuthorizedException

        return Template(name="task.html", context={"token": token})

    @post(path="/add", status_code=301)
    async def new(
        self,
        repository: TaskRepository,
        token: str,
        request: Request,
        form: TaskInput | None = Body(media_type=RequestEncodingType.URL_ENCODED),
    ) -> Redirect:
        if not app_settings.token == token:
            raise NotAuthorizedException

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
    dependencies={"repository": Provide(task_repository)},
)
