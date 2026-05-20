import os


def get_api_url() -> str:
    api_url = os.getenv("API_URL")
    if api_url:
        return api_url.rstrip("/")

    api_hostport = os.getenv("API_HOSTPORT")
    if api_hostport:
        return f"http://{api_hostport}".rstrip("/")

    return "http://localhost:8000"


API_URL = get_api_url()
