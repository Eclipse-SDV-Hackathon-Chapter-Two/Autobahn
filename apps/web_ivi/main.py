from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn import run
import os
import requests
import sys
from asyncio import sleep
from queue import Queue
import threading
import logging
import signal
from contextlib import asynccontextmanager

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

# OTA 관련 변수
LATEST_VERSION_URL = "http://example.com/updates/latest_version.txt"
BASE_UPDATE_URL = "http://example.com/updates"
LOCAL_VERSION_FILE = "updates/current_version.txt"
UPDATE_DIR = "updates"
DOWNLOAD_FILE = "/tmp/update.tar.gz"

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

stop_server_side_event = threading.Event()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Manages the lifespan of the FastAPI application.

    This function is a generator that performs actions at the startup and shutdown of the application.
    At startup, it sets up a signal handler for SIGINT to trigger a server-side event.
    At shutdown, it finalizes the eCAL core and logs the shutdown process.

    Args:
        _app (FastAPI): The FastAPI application instance.
    """
    # Run at startup
    signal.signal(signal.SIGINT, lambda: stop_server_side_event.set())

    yield
    # Run on shutdown
    # Finalize eCAL API
    ecal_core.finalize()
    logger.info('Shutting down...')

# create a route that delivers the statc/index.html file
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    """
    Serves the web ivi page by returning a FileResponse object pointing to "static/index.html".

    Returns:
        FileResponse: A response object that serves the "static/index.html" file.
    """
    return FileResponse("static/index.html")

@app.get("/vehicle-dynamics")
async def vehicle_dynamics():
    """
    Asynchronous function to handle vehicle dynamics data streaming to the client browser.

    This function initializes the eCAL API, subscribes to the "vehicle_dynamics" topic,
    and sets a callback to handle incoming messages. It uses an asynchronous generator
    to yield vehicle dynamics data as server-sent events (SSE).

    Returns:
        StreamingResponse: A streaming response with vehicle dynamics data in SSE format.
    """
    async def vehicle_dynamics_generator():
        vehicle_dynamics_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_vehicle_dynamics(_topic_name, msg, _time):
            vehicle_dynamics_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "WebIVI VehicleDynamics")

        # Subscribe to the vehicle_dynamics topic receiving json messages
        sub = StringSubscriber("vehicle_dynamics")

        # Set the Callback
        sub.set_callback(callback_vehicle_dynamics)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not vehicle_dynamics_queue.empty():
                vehicle_dynamics_data = vehicle_dynamics_queue.get()
                logger.info(vehicle_dynamics_data)
                vehicle_dynamics_queue.task_done()
                vehicle_dynamics_queue = Queue()
                yield f"event: vehicle-dynamics\ndata: {vehicle_dynamics_data}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(vehicle_dynamics_generator(), media_type="text/event-stream")

@app.post("/update/")
def update():
    """
    Checks for the latest version and applies updates if necessary.
    """
    try:
        # Step 1: Fetch current version
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                local_version = f.read().strip()
        else:
            local_version = "0.0.0"
        logger.info(f"Current version: {local_version}")

        # Step 2: Fetch latest version
        response = requests.get(LATEST_VERSION_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch the latest version information")
        latest_version = response.text.strip()
        logger.info(f"Latest version: {latest_version}")

        # Step 3: Check if an update is needed
        if local_version == latest_version:
            return JSONResponse(content={"status": "no_update", "message": "Already up-to-date"})

        # Step 4: Download the latest update
        update_url = f"{BASE_UPDATE_URL}/{latest_version}/update.tar.gz"
        logger.info(f"Downloading update from {update_url}")
        response = requests.get(update_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to download the update file")
        os.makedirs(os.path.dirname(DOWNLOAD_FILE), exist_ok=True)
        with open(DOWNLOAD_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Step 5: Apply the update
        logger.info("Applying update...")
        os.makedirs(UPDATE_DIR, exist_ok=True)
        os.system(f"tar -xzf {DOWNLOAD_FILE} -C {UPDATE_DIR}")

        # Step 6: Update the current version file
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(latest_version)

        logger.info("Update applied successfully")
        return JSONResponse(content={"status": "success", "message": f"Updated to version {latest_version}"})

    except Exception as e:
        logger.error(f"Update failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5500)

