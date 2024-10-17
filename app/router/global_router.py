import datetime
import json

import redis as redis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from app.api.asics import scan_miners, get_miner_data, get_all_miners_data, get_all_miners_scan, mac_returner, \
    get_uniq_macs
from app.config import BASIC_LOGIN, BASIC_PASS, MINERS_CONFIGURATION, REDIS_CONN
from app.methods.default import miner_data_by_all_data, miner_data_by_all_data_id, miner_data_new

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
    # tags=["device_methods"],
    responses={404: {"description": "Not found"}},
)

calc_router = APIRouter(
    # tags=["calc_profit_device"],
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
    if miner_data is not None:
        return miner_data.as_json()
    else:
        return []


@router.get('/device/get_device/hashrate/{device_ip}', dependencies=[Depends(check_creds)])
async def hasrate_info_sel_device_by_ip(device_ip: str):
    miner_data = await get_miner_data(device_ip)
    if miner_data is not None:
        return miner_data.hashrate
    else:
        return []


@router.get('/device/get_device/config/{device_ip}', dependencies=[Depends(check_creds)])
async def confing_info_sel_device_by_ip(device_ip: str):
    miner_data = await get_miner_data(device_ip)
    if miner_data is not None:
        return miner_data.config
    else:
        return []


@router.get('/device/get_device/all_mac/', dependencies=[Depends(check_creds)])
async def all_miners_mac():
    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = red.get('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d'))
    if cache is not None:
        return json.loads(cache)

    all_miners_data = await get_all_miners_data()
    macs = mac_returner(all_miners_data)

    macs_yesterday = json.loads(
        red.get('macs_cache_' + (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')))
    new_macs_today = await get_uniq_macs(macs_yesterday, macs)
    print(new_macs_today)

    red.set('new_macs_cache_' + datetime.date.today().strftime('%Y-%m-%d'), json.dumps(new_macs_today))
    red.set('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d'), json.dumps(macs))

    return macs


# @router.get('/device/get_device/old_devices/', dependencies=[Depends(check_creds)])
# async def all_miners_old():
#


# @router.post('/device/config/{device_ip}', dependencies=[Depends(check_creds)])
# async def provisioning_service(device_ip: str):
#     print("configuration device by ip")
#     return 200


@router.get('/device/macs/', dependencies=[Depends(check_creds)])
async def get_all_macs():
    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = json.loads(red.get('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d')))
    # cache_2 = json.loads(red.get('macs_cache_' + (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')))
    return {"today": cache}


@router.get('/device/set_old_info/', dependencies=[Depends(check_creds)])
async def set_old_devices():
    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    # cache = json.loads(red.get('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d')))

    with open('app/device_info_old_service.json') as f:
        d = json.load(f)
        f.close()

    all_miners_data = await get_all_miners_data()
    format_data = await miner_data_by_all_data_id(all_miners_data, d)

    for device_old in format_data:
        red.set(device_old['mac_address'], json.dumps(device_old))

    return format_data


@router.get('/device/set_new_devices/', dependencies=[Depends(check_creds)])
async def set_new_devices():
    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    # cache = json.loads(red.get('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d')))
    all_miners_data = await get_all_miners_data()
    news = []
    print(all_miners_data)
    cache_all = red.get('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d'))

    if cache_all is None:
        cache_all = []
    else:
        cache_all = json.loads(cache_all)

    for miner in all_miners_data:
        print(miner['mac'])
        cache = red.get(miner['mac'])

        if cache is not None:
            print('exist')
            cache_all.append(miner['mac'])
        else:
            new_mine_data = await miner_data_new(miner)
            red.set(new_mine_data['mac_address'], json.dumps(new_mine_data))
            news.append(new_mine_data['mac_address'])
            cache_all.append(new_mine_data['mac_address'])

    red.set('macs_cache_' + datetime.date.today().strftime('%Y-%m-%d'), json.dumps(cache_all))

    return news



@calc_router.get('/device/all_data_info/realtime/', dependencies=[Depends(check_creds)])
async def get_all_data_realtime():
    """get all miner information realtime"""
    all_miners_data = await get_all_miners_scan()

    return all_miners_data


@calc_router.get('/device/all_data_info/cache/', description='', dependencies=[Depends(check_creds)])
async def get_all_data():
    """get all data by cache today"""

    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = red.get(datetime.date.today().strftime('%Y-%m-%d'))
    if cache is not None:
        return json.loads(cache)

    all_miners_data, miners_info = await get_all_miners_data()

    return all_miners_data


@calc_router.get('/device/all_data_info/', description='get by db macs old with news', dependencies=[Depends(check_creds)])
async def get_all_data_by_list():
    """get all data by cache today"""

    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = red.get("macs_cache_"+datetime.date.today().strftime('%Y-%m-%d'))

    if cache is not None:
        device_all_data = []
        macs = json.loads(red.get("macs_cache_"+datetime.date.today().strftime('%Y-%m-%d')))

        for mac in macs:
            print(mac)
            device = red.get(mac)
            if device is not None:
                device_all_data.append(json.loads(device))

        return device_all_data

    # all_miners_data, miners_info = await get_all_miners_data()

    return 200


# @calc_router.post('/device/all_data_info/old_devices/', dependencies=[Depends(check_creds)])
# async def get_all_data_to_calc_profit_old_devices():
#     with open('app/device_info_old_service.json') as f:
#         d = json.load(f)
#         f.close()


@calc_router.post('/device/all_data_info/create_cache/', dependencies=[Depends(check_creds)])
async def get_all_data_to_calc_profit():
    """default research method"""

    red = redis.Redis(host=REDIS_CONN, max_connections=10, decode_responses=True)
    cache = red.get(datetime.date.today().strftime('%Y-%m-%d'))
    if cache is not None:
        return json.loads(cache)

    # all_miners_data, miners_info = await get_all_miners_data()
    all_miners_data = await get_all_miners_data()

    with open('app/device_info_old_service.json') as f:
        d = json.load(f)
        f.close()

    format_data = await miner_data_by_all_data_id(all_miners_data, d)

    print("all_mine_data_get = ", len(all_miners_data))

    red.set(datetime.date.today().strftime('%Y-%m-%d'), json.dumps(format_data))

    return HTTP_200_OK

