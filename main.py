from ph4_walkingpad.pad import WalkingPad, Controller
import yaml
import asyncio

minimal_cmd_space = 0.69

ctler = Controller()

def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def save_config(config):
    with open('config.yaml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

async def connect():
    address = load_config()['address']
    print("Connecting to {0}".format(address))
    await ctler.run(address)
    await asyncio.sleep(minimal_cmd_space)


async def disconnect():
    await ctler.disconnect()
    await asyncio.sleep(minimal_cmd_space)

async def get_status():
    try:
        await connect()

        await ctler.ask_stats()
        await asyncio.sleep(minimal_cmd_space)
        stats = ctler.last_status
        mode = stats.manual_mode
        belt_state = stats.belt_state

        if (mode == WalkingPad.MODE_STANDBY):
            mode = "standby"
        elif (mode == WalkingPad.MODE_MANUAL):
            mode = "manual"
        elif (mode == WalkingPad.MODE_AUTOMAT):
            mode = "auto"

        if (belt_state == 5):
            belt_state = "standby"
        elif (belt_state == 0):
            belt_state = "idle"
        elif (belt_state == 1):
            belt_state = "running"
        elif (belt_state >=7):
            belt_state = "starting"

        dist = stats.dist / 100
        time = stats.time
        steps = stats.steps
        speed = stats.speed / 10

        return { "dist": dist, "time": time, "steps": steps, "speed": speed, "belt_state": belt_state }
    finally:
        await disconnect()