# external requests library that makes http calls
import requests

# constants
NTFY_TOPIC = "lifeagent-rin"
NTFY_URL = "https://ntfy.sh/" + NTFY_TOPIC

# default LifeAgent param
def notify(message: str, title: str = "LifeAgent"):
    # http post, convert to what http needs [bytes] w header for title on phone
    requests.post(
        NTFY_URL,
        data=message.encode("utf-8"),
        headers={"Title": title}
    )

# only demo if someone runs it by itself
if __name__ == "__main__":
    notify("lifeagent ntfy module working!", title="test")