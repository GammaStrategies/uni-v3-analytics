from fastapi import Response, status

from v3data.hypervisor import HypervisorInfo
from v3data.toplevel import TopLevelData


async def hypervisor_basic_stats(
    chain: str, hypervisor_address: str, response: Response
):
    hypervisor_info = HypervisorInfo(chain)
    basic_stats = await hypervisor_info.basic_stats(hypervisor_address)

    if basic_stats:
        return basic_stats
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Invalid hypervisor address or not enough data"


async def hypervisor_apy(chain: str, hypervisor_address, response: Response):
    hypervisor_info = HypervisorInfo(chain)
    returns = await hypervisor_info.calculate_returns(hypervisor_address)

    if returns:
        return {"hypervisor": hypervisor_address, "returns": returns}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Invalid hypervisor address or not enough data"


async def aggregate_stats(chain: str):
    top_level = TopLevelData(chain)
    top_level_data = await top_level.all_stats()

    return {
        "totalValueLockedUSD": top_level_data["tvl"],
        "pairCount": top_level_data["pool_count"],
        "totalFeesClaimedUSD": top_level_data["fees_claimed"],
    }


async def recent_fees(chain: str, hours: int = 24):
    top_level = TopLevelData(chain)
    recent_fees = await top_level.recent_fees(hours)

    return {"periodHours": hours, "fees": recent_fees}


async def hypervisors_return(chain: str):
    hypervisor_info = HypervisorInfo(chain)

    return await hypervisor_info.all_returns()


async def hypervisors_all(chain: str):
    hypervisor_info = HypervisorInfo(chain)

    return await hypervisor_info.all_data()