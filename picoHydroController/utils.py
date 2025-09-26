from time import sleep
import ujson as json
import network
import requests
from umqtt.simple import MQTTClient
import utime
from machine import RTC


def load_env(env_path=".env") -> dict:
    env_vars = {}
    try:
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    env_vars[key] = value.strip().strip("'").strip('"')
    except OSError:
        print("Could not open .env file.")
    return env_vars


def publish_mqtt_message(
    client_id: str,
    broker: str,
    port: int,
    user: str,
    password: str,
    topic: str,
    message: dict,
):
    client = MQTTClient(client_id, broker, port, user, password)
    try:
        client.connect()
        client.publish(topic, json.dumps(message))
        client.disconnect()
        print(f"Published message to {topic}: {message}")
    except Exception as e:
        print(f"Failed to publish message: {e}")


def connect_wifi(ssid: str, pwd: str) -> bool:
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            print("Waiting for connection...")
            sleep(1)
    return sta_if.isconnected()


def set_rtc(timezone: str):
    url = f"https://timeapi.io/api/time/current/zone?timeZone=America%2F{timezone}"
    days_of_week = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    # get current time from API
    try:
        initial_pico_time = utime.ticks_ms()
        api_response = requests.get(url)
        pico_time_delta_after_response = utime.ticks_diff(
            utime.ticks_ms(), initial_pico_time
        )
        if api_response.status_code == 200:
            time_data = api_response.json()
            # convert to milliseconds
            hours_ms, minutes_ms, seconds_ms = (
                int(time_data.get("hour")) * 3600000,
                int(time_data.get("minute")) * 60000,
                int(time_data.get("seconds")) * 1000,
            )
            adjusted_time = (
                hours_ms + minutes_ms + seconds_ms + pico_time_delta_after_response
            )
            dow = days_of_week.get(time_data.get("dayOfWeek"))
            new_rtc = (
                time_data.get("year"),
                time_data.get("month"),
                time_data.get("day"),
                dow,
                int(adjusted_time // 3600000) % 24,
                int((adjusted_time % 3600000) // 60000) % 60,
                int((adjusted_time % 60000) // 1000) % 60,
                int(adjusted_time % 1000),
            )
            rtc = RTC()
            rtc.datetime(new_rtc)
        else:
            pass
    except Exception as e:
        print(f"Error fetching time data: {e}")
        return

    import machine

    rtc = machine.RTC()
    rtc.datetime(time_tuple)
    
