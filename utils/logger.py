import logging
import os

LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()

logging.basicConfig(level=LOGLEVEL,
                    format='%(asctime)s:%(levelname)s: %(message)s',
                    datefmt='%m-%d-%YT%H:%M:%S%z')

if __name__ == '__main__':
    logging.debug("hello")
