import os


def get_api_url() -> str:
    api_url = os.getenv("API_URL")
    if api_url:
        return api_url.rstrip("/")

    api_hostport = os.getenv("API_HOSTPORT")
    if api_hostport:
        if os.getenv("RENDER"):
            host = api_hostport.split(":", 1)[0]
            return f"https://{host}.onrender.com"
        return f"http://{api_hostport}".rstrip("/")

    return "http://localhost:8000"


API_URL = get_api_url()
