from playwright.sync_api import sync_playwright
from twilio.rest import Client
from datetime import datetime
from dataclasses import dataclass

import time
import random
import yaml

URL = "https://www.bestbuy.com/site/nvidia-geforce-rtx-4090-24gb-gddr6x-graphics-card-titanium-and-black/6521430.p?acampID=0&cmp=RMX&irclickid=zpS1Dd2x1xyPUIQ3CYXtKQK9UkFzABQbxxY9WQ0&irgwc=1&loc=PCPartPicker&mpid=79301&ref=198&refdomain=pcpartpicker.com&skuId=6521430"


@dataclass
class TwilioConfig:
    account_sid: str
    auth_token: str
    message_sender: str
    message_receiver: str


def read_config() -> TwilioConfig:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return TwilioConfig(
            account_sid=config["twilio"]["account_sid"],
            auth_token=config["twilio"]["auth_token"],
            message_sender=config["twilio"]["message_sender"],
            message_receiver=config["twilio"]["message_receiver"],
        )


def main():
    config = read_config()
    client = Client(config.account_sid, config.auth_token)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        found = False
        while not found:
            page.goto(URL)
            state = page.wait_for_selector("button.add-to-cart-button").get_attribute(
                "data-button-state"
            )
            match state:
                case "SOLD_OUT":
                    print("Out of stock at", datetime.now().strftime("%H:%M:%S"))
                    time.sleep(random.gauss(mu=10, sigma=2))
                case "ADD_TO_CART":
                    print(
                        "🎉 Found NVIDIA RTX 4090 Founder's Edition at",
                        datetime.now().strftime("%H:%M:%S"),
                        "!!!",
                    )
                    message = client.messages.create(
                        from_=config.message_sender,
                        to=config.message_reciever,
                        body="RTX 4090 is in stock!",
                    )
                    print(message.sid)
                    found = True
                case _:
                    raise Exception(
                        "Got unknown state " + state + " on page: " + page.content()
                    )
        browser.close()


if __name__ == "__main__":
    main()
