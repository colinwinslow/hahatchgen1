import asyncio
import json
import paho.mqtt.client as mqtt
from pyhatchbabyrest import PyHatchBabyRestAsync

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_COMMAND_TOPIC = "hatch/command"
MQTT_STATE_TOPIC = "hatch/state"

rest = None

async def setup_device():
    global rest
    rest = PyHatchBabyRestAsync()
    await rest.connect()
    await publish_state()

async def handle_command(payload):
    command = json.loads(payload)
    if 'power' in command:
        if command['power'] == 'on':
            await rest.power_on()
        elif command['power'] == 'off':
            await rest.power_off()
    if 'volume' in command:
        await rest.set_volume(command['volume'])
    if 'color' in command:
        await rest.set_color(*command['color'])  # expects [r, g, b]
    if 'brightness' in command:
        await rest.set_brightness(command['brightness'])
    if 'sound' in command:
        await rest.set_sound(command['sound'])
    await publish_state()

async def publish_state():
    client.publish(MQTT_STATE_TOPIC, json.dumps({"status": "updated"}), retain=True)

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_COMMAND_TOPIC)

def on_message(client, userdata, msg):
    asyncio.run(handle_command(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

asyncio.run(setup_device())

# Keep the script alive
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
