import logging
from argparse import ArgumentParser
from datetime import datetime, timezone

from pymongo import MongoClient

from model import TaskInput, Search, Query, TaskOutput
from repository import TaskRepository
from settings import Settings

settings = Settings()
client: MongoClient = MongoClient(settings.database_uri)
repository = TaskRepository(client.work)
logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    insert = subparser.add_parser("insert")
    insert.add_argument("details", metavar="Details", help="details of the task")
    insert.add_argument("-t", "--tag", required=True)
    insert.add_argument(
        "-d",
        "--date",
        default=datetime.utcnow().replace(tzinfo=timezone.utc, hour=0, minute=0, second=0, microsecond=0),
    )

    find = subparser.add_parser("find")
    find.add_argument("-t", "--tag")
    find.add_argument("-d", "--date")
    find.add_argument("-s", "--sort", default="newest")
    find.add_argument("-l", "--limit", type=int, default=10)

    args = parser.parse_args()
    if args.command == "insert":
        result = repository.insert(TaskInput(date=args.date, tag=args.tag, details=args.details))
        logger.warning(result)
    elif args.command == "find":
        result = repository.find(Search(tag=args.tag, date=args.date), Query(limit=args.limit, sort=args.sort))
        for item in result:
            item["id"] = str(item["_id"])
            logger.warning(TaskOutput(**item).json())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
