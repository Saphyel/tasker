import logging
from argparse import ArgumentParser
from datetime import datetime

from pymongo import MongoClient

from model import TaskInput, Search, Pagination
from repository import TaskRepository
from settings import app_settings

client: MongoClient = MongoClient(app_settings.database_uri)
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
        default=datetime.utcnow(),
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
        data = repository.find(Search(tag=args.tag, date=args.date), Pagination(limit=args.limit, sort=args.sort))
        [logger.warning(item.json()) for item in data.result]

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
