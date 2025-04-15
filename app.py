from ZeroTier import config
from ZeroTier.api import ZeroTierAPI
from ZeroTier.device import DeviceResult
from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

import asyncio
from contextlib import asynccontextmanager

global_state: Dict[str, DeviceResult] = {}
CONFIG: config.Config = config.getConfig("config.yaml")
ZT = ZeroTierAPI(CONFIG.token)
INTERVAL = CONFIG.interval
DEVICES = CONFIG.devices


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background task
    task = asyncio.create_task(update_state_forever())
    yield  # Application runs while this block is open
    task.cancel()  # Cleanup
    try:
        await task
    except asyncio.CancelledError:
        pass
app = FastAPI(lifespan=lifespan)


# -- Background task --

def fetch_device_info(device: config.Device) -> Optional[DeviceResult]:
    try:
        data = ZT.get_node(device.network_id, device.node_id)
        enriched = {
            "name": device.name,
            "network_id": device.network_id,
            "node_id": device.node_id,
            "last_online": data.get("lastOnline"),
            "clock": data.get("clock")
        }
        return DeviceResult.from_dict(enriched)
    except Exception as e:
        print(f"[ERROR] {device.name}: {e}")
        return None


async def update_state_forever():
    while True:
        results = await asyncio.gather(*[
            asyncio.to_thread(fetch_device_info, device)
            for device in DEVICES
        ])
        for res in results:
            if res:
                global_state[res.name] = res
        await asyncio.sleep(INTERVAL)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    html_path = Path("static/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)


@app.get("/status", response_model=Dict[str, DeviceResult])
async def get_status():
    return global_state
