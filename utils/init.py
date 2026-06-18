from utils.logger import *
import shutil


def initialize(log_path):
    # For log
    if os.path.exists(log_path):
        logging.info("log path exists {}".format(log_path))
    else:
        logging.error("log path does not exists - {}".format(log_path))
        logging.info("creating log path")
        os.mkdir(log_path)
        logging.info("log path created")

    logging.info("initialization done")


if __name__ == '__main__':
    initialize(os.getcwd() + '/log')