
BASE_URL = 'https://www.pentairthermalwifi.com/api'

def login(username, password):
    return f"{BASE_URL}/authenticate?email={username}&password={password}"

def get_groups(session):
    return f"{BASE_URL}/groups?sessionId={session}"

def get_devices(session):
    return f"{BASE_URL}/thermostats?sessionId={session}"

def get_device(session, serial):
    return f"{BASE_URL}/thermostat?sessionId={session}&serialnumber={serial}"