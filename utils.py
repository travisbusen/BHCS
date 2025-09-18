import umqtt.simple as mqtt
import ujson as json


def load_env(env_path='.env') -> dict:
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value.strip().strip("'").strip('"')
    except OSError:
        print("Could not open .env file.")
    return env_vars


def publish_mqtt_message(client_id:str, broker:str, port:int, user:str, password:str, topic:str, message:dict):
    client = mqtt.MQTTClient(client_id, broker, port, user, password)
    try:
        client.connect()
        client.publish(topic, json.dumps(message))
        client.disconnect()
        print(f"Published message to {topic}: {message}")
    except Exception as e:
        print(f"Failed to publish message: {e}")
