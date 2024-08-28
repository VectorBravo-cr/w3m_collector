import datetime
import json

import redis as redis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from app.api.asics import scan_miners, get_miner_data, get_all_miners_data
from app.config import BASIC_LOGIN, BASIC_PASS, MINERS_CONFIGURATION, REDIS_CONN
from app.methods.default import miner_data_by_all_data, miner_data_by_all_data_id

security = HTTPBasic()


async def check_creds(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != BASIC_LOGIN or credentials.password != BASIC_PASS:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect authorization credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


router = APIRouter(
    tags=["device_methods"],
    responses={404: {"description": "Not found"}},
)

calc_router = APIRouter(
    tags=["calc_profit_device"],
    responses={404: {"description": "Not found"}},
)


# @router.get('/test/', description="tester", dependencies=[Depends(check_creds)])
# async def hello():
#     return BASIC_LOGIN, BASIC_PASS, MINERS_CONFIGURATION


@router.post('/device/searching/', dependencies=[Depends(check_creds)])
async def default_search_devices():
    try:
        asics_network = await scan_miners()
        return asics_network

    except:
        raise HTTPException(status_code=400, detail="Service error, see the log")


@router.get('/device/get_device/{device_ip}', dependencies=[Depends(check_creds)])
async def all_info_selected_device_by_ip(device_ip: str):
    miner_data = await get_miner_data(device_ip)
    return miner_data.as_json()


@router.get('/device/get_device/hashrate/{device_ip}', dependencies=[Depends(check_creds)])
async def hasrate_info_sel_device_by_ip(device_ip: str):
    miner_data = await get_miner_data(device_ip)
    return miner_data.hashrate


@router.get('/device/get_device/config/{device_ip}', dependencies=[Depends(check_creds)])
async def confing_info_sel_device_by_ip(device_ip: str):
    miner_data = await get_miner_data(device_ip)
    return miner_data.config


# @router.post('/device/config/{device_ip}', dependencies=[Depends(check_creds)])
# async def provisioning_service(device_ip: str):
#     print("configuration device by ip")
#     return 200


@calc_router.get('/device/all_data_info/realtime/', dependencies=[Depends(check_creds)])
async def get_all_data_realtime():
    """get all miner information realtime"""
    miners = await scan_miners()
    all_miners_data = await get_all_miners_data(miners)

    return all_miners_data


@calc_router.get('/device/all_data_info/cache/', description='')
async def get_all_data(dependencies=Depends(check_creds)):
    """get all data by cache today"""
    print(dependencies)
    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = red.get(datetime.date.today().strftime('%Y-%m-%d'))
    if cache is not None:
        return json.loads(cache)

    miners = await scan_miners()
    all_miners_data = await get_all_miners_data(miners)

    return all_miners_data


@calc_router.post('/device/all_data_info/create_cache/', dependencies=[Depends(check_creds)])
async def get_all_data_to_calc_profit():
    """default research method"""
    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = red.get(datetime.date.today().strftime('%Y-%m-%d'))
    if cache is not None:
        return json.loads(cache)

    miners = await scan_miners()
    all_miners_data = await get_all_miners_data(miners)
    with open('app/device_info_old_service.json') as f:
        d = json.load(f)
        f.close()
    format_data = await miner_data_by_all_data_id(all_miners_data, d)
    red.set(datetime.date.today().strftime('%Y-%m-%d'), json.dumps(format_data))

    return HTTP_200_OK
