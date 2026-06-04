from influxdb import InfluxDBClient
from loguru import logger


def get_influx_client(host, port):
    try:
        influx_client = InfluxDBClient(
            host=host,
            port=port,
            username="admin",
            password="admin123",
            database="data"
        )
        if influx_client.ping():
            return influx_client
        else:
            logger.debug("could not connect to influxDB")
            return None
    except ConnectionError as e:
        logger.debug(f"{e}")
        return None
    except Exception as e:
        logger.error(f"{e}")
        return None
