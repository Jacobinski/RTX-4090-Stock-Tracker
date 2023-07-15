from playwright.sync_api import sync_playwright
import time

rtx4090 = "https://www.bestbuy.com/site/nvidia-geforce-rtx-4090-24gb-gddr6x-graphics-card-titanium-and-black/6521430.p?acampID=0&cmp=RMX&irclickid=zpS1Dd2x1xyPUIQ3CYXtKQK9UkFzABQbxxY9WQ0&irgwc=1&loc=PCPartPicker&mpid=79301&ref=198&refdomain=pcpartpicker.com&skuId=6521430"
inStockGPU = "https://www.bestbuy.com/site/asus-nvidia-geforce-rtx-4070-ti-tuf-overclock-12gb-gddr6x-pci-express-4-0-graphics-card-black/6529351.p?skuId=6529351"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    found = False
    while not found:
        page.goto(inStockGPU)
        state = page.wait_for_selector("button.add-to-cart-button").get_attribute("data-button-state")
        match state:
            case "SOLD_OUT":
                time.sleep(10)
            case "ADD_TO_CART":
                # TODO: Send a text message
                time.sleep(10)
                print("Found!")
                found = True
            case _:
                raise Exception("Got state" + state + "on page: " + page.content())
    browser.close()