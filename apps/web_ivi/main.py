from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from uvicorn import run
import asyncio
import shutil

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

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

stop_server_side_event = threading.Event()
connected_clients = []

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
static_files_with_headers = StaticFiles(directory="static")
static_files_with_headers.headers = {"Cache-Control": "no-store"}
app.mount("/static", StaticFiles(directory="static"), name="static")

assets_with_headers = StaticFiles(directory="static/assets")
assets_with_headers.headers = {"Cache-Control": "no-store"}
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

@app.post("/execute-shell-script")
async def execute_shell_script():
    result = subprocess.run(["./static/helloworld.sh"], capture_output=True, text=True)
    logger.info(f"Script output: {result.stdout}")
    return JSONResponse(content={"message": "Shell script executed successfully", "output": result.stdout})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """웹소켓 연결 관리"""
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Keep the connection alive
    except:
        connected_clients.remove(websocket)


@app.post("/ota")
async def ota_update():
    """OTA 업데이트 실행"""
    # 1. 변경된 파일 복사/배포 (예: S3에서 다운로드 후 덮어쓰기)
    source_dir = "/web_ivi/updates/static"  # OTA에서 가져온 파일
    target_dir = "/web_ivi/static"  # 현재 GUI 파일이 있는 디렉토리
    if os.path.exists(source_dir):
        shutil.rmtree(target_dir)  # 기존 파일 삭제
        shutil.copytree(source_dir, target_dir)  # 새로운 파일 복사

    # 2. 클라이언트에 변경 사항 알림
    message = "OTA update applied!"
    for client in connected_clients:
        await client.send_text(message)

    return {"status": "success", "message": message}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5500)
