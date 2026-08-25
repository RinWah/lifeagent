# external requests library that makes http calls
import os
import requests

# constants
# i made this an env since it shouldn't be hardcoded
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "lifeagent-rin")
NTFY_URL = "https://ntfy.sh/" + NTFY_TOPIC

# default LifeAgent param
def notify(message: str, title: str = "LifeAgent"):
    # new logic to strip title if it contains emojis
    headers = {}
    try: 
        title.encode("latin-1")
        headers["Title"] = title
    except UnicodeEncodeError:
        pass # omit title if it cant be encoded safely

    try:
        response = requests.post(
    # http post, convert to what http needs [bytes] w header for title on phone
            NTFY_URL,
            data=message.encode("utf-8"),
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    # went back to original way of catching and displaying errors w/o exposing secrets
    except requests.exceptions.RequestException as e:
        print(f"ntfy delivery failed: {type(e).__name__}")


# only demo if someone runs it by itself
if __name__ == "__main__":
    notify("lifeagent ntfy module working!", title="test")