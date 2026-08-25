# external requests library that makes http calls
import os
import requests

# constants
# i made this an env since it shouldn't be hardcoded
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "lifeagent-rin")
NTFY_URL = "https://ntfy.sh/" + NTFY_TOPIC

# default LifeAgent param
def notify(message: str, title: str = "LifeAgent"):
    # turned into a try block in case ntfy.sh is down, so we don't have a forever running attempt
    try: 
        response = requests.post(
    # http post, convert to what http needs [bytes] w header for title on phone
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={"Title": title},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"if ntfy down? ntfy delivery failed: {e}")


# only demo if someone runs it by itself
if __name__ == "__main__":
    notify("lifeagent ntfy module working!", title="test")