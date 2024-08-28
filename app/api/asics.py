import asyncio

from pyasic import get_miner
from pyasic.network import MinerNetwork

from app.config import MINERS_NETWORK


async def scan_miners():
    # default scan for subnet
    network = MinerNetwork.from_subnet(MINERS_NETWORK)
    # print(network.hosts)
    miners = await network.scan()
    print(len(miners))
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


async def get_all_miners_data(miners):
    all_miner_data = await asyncio.gather(*[miner.get_data() for miner in miners])

    return all_miner_data
