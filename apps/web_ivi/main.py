from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from uvicorn import run
import os
import sys
from asyncio import sleep
from queue import Queue
import threading
import logging
import signal
from contextlib import asynccontextmanager
import subprocess

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

stop_server_side_event = threading.Event()

# OTA
pub = None

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
    ecal_core.finalize()
    logger.info('Shutting down...')

# create a route that delivers the static/index.html file
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
    Serves the web IVI page by returning a FileResponse object pointing to "static/index.html".

    Returns:
        FileResponse: A response object that serves the "static/index.html" file.
    """
    return FileResponse("static/index.html")

@app.get("/vehicle-dynamics")
async def vehicle_dynamics():
    """
    Asynchronous function to handle vehicle dynamics data streaming to the client browser.
    """
    async def vehicle_dynamics_generator():
        vehicle_dynamics_queue = Queue()

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

        ecal_core.finalize()

    return StreamingResponse(vehicle_dynamics_generator(), media_type="text/event-stream")

@app.get("/hidden_danger_people")
async def hidden_danger_people():
    """
    Asynchronous function to handle vehicle dynamics data streaming to the client browser.

    This function initializes the eCAL API, subscribes to the "hidden_danger_people" topic,
    and sets a callback to handle incoming messages. It uses an asynchronous generator
    to yield vehicle dynamics data as server-sent events (SSE).

    Returns:
        StreamingResponse: A streaming response with vehicle dynamics data in SSE format.
    """
    async def hidden_danger_people_generator():
        hidden_danger_people_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_hidden_danger_people(_topic_name, msg, _time):
            hidden_danger_people_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "WebIVI HiddenDangerPeople")

        # Subscribe to the hidden_danger_people topic receiving json messages
        sub = StringSubscriber("hidden_danger_people")

        # Set the Callback
        sub.set_callback(callback_hidden_danger_people)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not hidden_danger_people_queue.empty():
                hidden_danger_people_data = hidden_danger_people_queue.get()
                logger.info(hidden_danger_people_data)
                hidden_danger_people_queue.task_done()
                hidden_danger_people_queue = Queue()
                yield f"event: hidden_danger_people\ndata: {hidden_danger_people_data}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(hidden_danger_people_generator(), media_type="text/event-stream")

@app.get("/calculated_angle")
async def calculated_angle():
    """
    Asynchronous function to handle vehicle dynamics data streaming to the client browser.

    This function initializes the eCAL API, subscribes to the "calculated_angle" topic,
    and sets a callback to handle incoming messages. It uses an asynchronous generator
    to yield vehicle dynamics data as server-sent events (SSE).

    Returns:
        StreamingResponse: A streaming response with vehicle dynamics data in SSE format.
    """
    async def calculated_angle_generator():
        calculated_angle_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_calculated_angle(_topic_name, msg, _time):
            calculated_angle_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "WebIVI CalculatedAngle")

        # Subscribe to the calculated_angle topic receiving json messages
        sub = StringSubscriber("calculated_angle")

        # Set the Callback
        sub.set_callback(callback_calculated_angle)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not calculated_angle_queue.empty():
                calculated_angle_data = calculated_angle_queue.get()
                logger.info(calculated_angle_data)
                calculated_angle_queue.task_done()
                calculated_angle_queue = Queue()
                yield f"event: calculated_angle\ndata: {calculated_angle_data}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(calculated_angle_generator(), media_type="text/event-stream")

@app.get("/version")
async def version():
    """
    Asynchronous function to handle vehicle dynamics data streaming to the client browser.

    This function initializes the eCAL API, subscribes to the "version" topic,
    and sets a callback to handle incoming messages. It uses an asynchronous generator
    to yield vehicle dynamics data as server-sent events (SSE).

    Returns:
        StreamingResponse: A streaming response with vehicle dynamics data in SSE format.
    """
    async def version_generator():
        version_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_version(_topic_name, msg, _time):
            version_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "WebIVI Version")

        # Subscribe to the version topic receiving json messages
        sub = StringSubscriber("version")

        # Set the Callback
        sub.set_callback(callback_version)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not version_queue.empty():
                version_data = version_queue.get()
                logger.info(version_data)
                version_queue.task_done()
                version_queue = Queue()
                yield f"event: version\ndata: {version_data}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(version_generator(), media_type="text/event-stream")

@app.post("/yorn")
async def yorn():
    global pub

    # Initialize ecal
    ecal_core.initialize(sys.argv, "WebIVI Version")

    if pub is None:
        pub = StringPublisher("yorn")
    pub.send("1")

    # Finalize eCAL API
    ecal_core.finalize()

@app.post("/execute-shell-script")
async def execute_shell_script():
    result = subprocess.run(["./static/helloworld.sh"], capture_output=True, text=True)
    logger.info(f"Script output: {result.stdout}")
    return JSONResponse(content={"message": "Shell script executed successfully", "output": result.stdout})

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5500)
