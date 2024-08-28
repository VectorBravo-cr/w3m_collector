from app.schemas.schemas_validator import CustomValidation


class DeviceDataSchema(CustomValidation):
    """ default device schemas calc_profit"""
    device_id: str
    mac_address: str
    is_active: bool
    pool_name: str
    kw_per_hour: int
    hostname: str
    miner_name: str
    subaccount: str


class Device(CustomValidation):
    """ def device link"""
    guid: str # device_uuid
    ip: str #all_data.ip
    mac: str # mac_adress
    last_data: DeviceDataSchema #schema_to_calc_profit

