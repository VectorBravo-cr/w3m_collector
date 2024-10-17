import asyncio

from pyasic import get_miner
from pyasic.network import MinerNetwork

from app.config import MINERS_NETWORK


async def scan_miners():
    # default scan for subnet
    network = MinerNetwork.from_subnet(MINERS_NETWORK)
    miners = await network.scan()
    print("ip scan realtime devices = ", len(miners))

    return miners


async def get_miner_data(miner_net):
    # default info by miner
    miner = await get_miner(miner_net)
    if miner is not None:
        miner_data = await miner.get_data()
        print(miner_data)
        print(miner_data.hashrate)

        return miner_data
    return None


async def get_config_miner(miner_net):
    # default get config device
    miner = await get_miner(miner_net)
    if miner is not None:
        cfg = await miner.get_config()
        print(cfg)

        return cfg
    return None


async def get_all_miners_scan():
    net = MinerNetwork.from_subnet(MINERS_NETWORK)
    miners = await net.scan()
    all_miner_data = await asyncio.gather(*[miner.get_data() for miner in miners])
    print("data = ", len(all_miner_data))

    return all_miner_data


def mac_returner(data):
    macs = []
    if data:
        for asic in data:
            macs.append(asic['mac'])

    print(macs)
    return macs


async def get_all_miners_data():
    net = MinerNetwork.from_subnet(MINERS_NETWORK)
    miners = await net.scan()

    # miners_info = []
    # for miner in miners:
    #     miner_data = await miner.get_data()
    #     miners_info.append(miner_data)

    all_miner_data = await asyncio.gather(*[miner.get_data() for miner in miners])

    print("net = ", len(net))
    print("mine = ", len(miners))
    print("data = ", len(all_miner_data))
    # print("cycle = ", miners_info)

    # return all_miner_data, miners_info
    return all_miner_data


async def get_uniq_macs(list_old, list_new):
    uniq = []
    for new in list_new:
        if new not in list_old:
            uniq.append(new)

    return uniq