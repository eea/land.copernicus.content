import logging


logger = logging.getLogger('land.copernicus.content')


def delete_unused_accounts():
    logger.info("Deleted unused accounts. WIP")


def run(_):
    delete_unused_accounts()
