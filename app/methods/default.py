from app.schemas.calc_profit import Device, DeviceDataSchema


def miner_data_by_all_data(miner_data):
    ms = []
    print(miner_data)
    for miner in miner_data:
        device_info = DeviceDataSchema(
            device_id='0001',
            mac_address=miner['mac'],
            is_active=miner['is_mining'],
            pool_name=miner['config']['pools']['groups'][0]['pools'][0]['url'],
            kw_per_hour=miner['wattage'],
            hostname=miner['hostname'],
            miner_name=miner['hostname'],
            subaccount=miner['config']['pools']['groups'][0]['pools'][0]['user']
        )
        ms.append(device_info)

    return ms


async def miner_data_by_all_data_id(miner_data, old_miners_list):
    ms = []
    for miner in miner_data:
        for device_old in old_miners_list:
            if miner['mac'] == device_old['mac_address']:
                # device_info = DeviceDataSchema(
                #     device_id=device_old['device_uuid'],
                #     mac_address=miner['mac'],
                #     is_active=miner['is_mining'],
                #     pool_name=device_old['pool_name'],
                #     kw_per_hour=miner['wattage'],
                #     hostname=miner['hostname'],
                #     miner_name=miner['hostname'],
                #     subaccount=miner['config']['pools']['groups'][0]['pools'][0]['user']
                # )
                device_info = {
                    "device_id" : device_old['device_uuid'],
                    "mac_address" : miner['mac'],
                    "is_active" : miner['is_mining'],
                    "pool_name" : device_old['pool_name'],
                    "kw_per_hour" : miner['wattage'],
                    "hostname" : miner['hostname'],
                    "miner_name" : miner['hostname'],
                    "subaccount" : miner['config']['pools']['groups'][0]['pools'][0]['user']
                }
                ms.append(device_info)

    return ms
