
BASE_URL = 'https://www.pentairthermalwifi.com/api'

def login(username, password):
    return f"{BASE_URL}/authenticate?email={username}&password={password}"

def get_groups(session):
    return f"{BASE_URL}/groups?sessionId={session}"