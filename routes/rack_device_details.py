from datetime import datetime, timedelta
from fastapi import APIRouter
from config.influx_connection import get_influx_client
from loguru import logger
from requests import get
import json
import os

router = APIRouter()


@router.get("/get_rack_list", tags=["Rack Device Details"])
def get_rack_list():
    r_map = []
    try:
        # Get mapping json file path
        json_file = f"{os.getcwd()}/config/device_mapping.json"
        with open(json_file, "r") as f:
            dev_mapping = json.load(f)
            r_map = dev_mapping.get("rack_mapping", [])
        
        return r_map
    except Exception as e:
        logger.error(f"Error occurred while fetching rack list - {e}")
        return r_map


@router.get("/get_rack_device_details", tags=["Rack Device Details"])
def get_rack_device_details(
    rack_name: str,
    start_time: str,
    end_time: str
):
    data = []
    try:
        # Here we convert the start_time and end_time into UTC format
        start_time = (datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=30)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        end_time = (datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=30)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        
        # Get mapping json file path
        json_file = f"{os.getcwd()}/config/device_mapping.json"
        with open(json_file, "r") as f:
            dev_mapping = json.load(f)
            rack_devices = dev_mapping.get(rack_name, [])
        for dev_map in rack_devices:
            panel_no = dev_map['panel_no']
            dev_code = dev_map['device_code']
            zone = dev_map['zone']
            ip = dev_map['ip']
            port = dev_map['port']
            dev_name = dev_map['device_name']
            measurement = dev_map['measurement']
            try:
                influx_client = get_influx_client(ip, port)
                if influx_client:
                    val = get_data_from_influx1(influx_client, panel_no, dev_code, measurement, start_time, end_time, zone)
                    data.append({
                        "ip": ip,
                        "port": port,
                        "panel_no": panel_no,
                        "device_name": dev_name,
                        "device_code": dev_code,
                        "zone": zone,
                        "value": val
                    })
            except Exception as e:
                logger.error(f"Error occurred while fetching data from influx for device {dev_code} - {e}")
                data.append({
                    "ip": ip,
                    "port": port,
                    "panel_no": panel_no,
                    "device_name": dev_name,
                    "device_code": dev_code,
                    "zone": zone,
                    "value": None
                })
            finally:
                if influx_client:
                    influx_client.close()
        
        return {"data": data}
    except Exception as e:
        logger.error(f"Error occurred while fetching rack device details - {e}")
        return {"data": data}
    
    
    
def get_data_from_influx1(client, panel_no, dev_code, measurement, start_time, end_time, zone):
    """
    This function is used to get PCM data from influx
    """
    val = None
    try:
        query = f'''
            SELECT LAST("value")
            FROM "{measurement}"
            WHERE "device_code" = '{dev_code}'
              AND "panel_no" = '{panel_no}'
              AND "zone" = '{zone}'
              AND time >= '{start_time}'
              AND time <= '{end_time}'
        '''
        data = client.query(query)
        if data:
            val = format_influx_data(data)
        return val
    except Exception as e:
        logger.error(f"Error occurred in Occupancy_AQI details get_data_from_influx1 {e}")
        return val


def format_influx_data(data):
    value = None
    try:
        for record in data:
            for rec in record:
                value = rec['last']
                return value
        return value
    except Exception as e:
        logger.error(f"Error occurred in Occupancy_AQI details format_influx_data {e}")
        return value