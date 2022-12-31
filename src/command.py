import logging
from argparse import ArgumentParser

from pymongo import MongoClient

from model import Work, Search
from repository import WorkRepository
from settings import Settings

settings = Settings()
client: MongoClient = MongoClient(settings.database_uri)
repository = WorkRepository(client.task)
logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    insert = subparser.add_parser("insert")
    insert.add_argument("details", metavar="Details", type=str, help="details of the task")
    insert.add_argument("-d", "--date")
    insert.add_argument("-t", "--tag", required=True)

    find = subparser.add_parser("find")
    find.add_argument("-t", "--tag")
    find.add_argument("-d", "--date")

    args = parser.parse_args()
    if args.command == "insert":
        result = repository.insert(Work(date=args.date, tag=args.tag, details=args.details))
        logger.warning(result)
    elif args.command == "find":
        result = repository.find(Search(tag=args.tag, date=args.date))
        logger.warning([Work(**item).json() for item in result])
    else:
        logger.error("Invalid command.")


if __name__ == "__main__":
    main()
