from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Header, Footer
from textual.containers import ScrollableContainer
from tkinter import Tk, filedialog
import requests
import random



root = Tk()
root.withdraw()

class PurrOs(App):
    def get_weather(self):
        return requests.get(
            f"https://wttr.in/{self.city}?format=3"
        ).text
    

    

    BINDINGS = [
        ("escape", "dt", "Return to desktop")
    ]

    def open_catvex(self):
        self.isInApp = True
        self.cos.remove_children()

        weather = self.get_weather()

        rand = random.randint(1, 3)

        if rand == 1:
            n = "Mildly chaotic"
        elif rand == 2:
            n = "Few hairballs in the CPU (Central pheline unit)"
        elif rand == 3:
            n = "Cat-astrophic"

        view = Static(
        "[ForeCat]\n\n"
        f"Weather:\n{weather}\n\n"
        f"Status: {n}"
        )

        self.cos.mount(view)

    def action_dt(self):
        self.set_focus(None)
        self.desktop()

    def desktop(self):
        if not self.isInApp:
            for item in self.listitems:
                item.remove()
            return
        self.isInApp = False
        self.cos.remove_children()
        appo = Input(placeholder='Type app name to open or "/list" to see all your apps', id="appo")
        self.cos.mount(appo)


    def compose(self) -> ComposeResult:
        self.data = requests.get("https://ipinfo.io").json()
        self.city = self.data["city"]
        self.isInApp = False
        self.apps = {

        }
        self.bootspeed = 0.05
        self.progress = 0
        self.load = None
        self.listitems = []
        yield Header()
        yield Static("[#A16D64]PurrOS[/]")
        yield Static("")
        yield Input(placeholder='Type "/meow" to continue', id="boot")
        self.cos = ScrollableContainer()
        yield self.cos
        yield Footer()
    
    def addapp(self, appname, func):
        self.apps[appname] = func


    def parse(self, line):
        if not line or not ':' in line:
            return
        line = line.split(':')
        cmd = line[0]
        msg = line[1]
        if not cmd or not msg:
            return
        if cmd == 'text':
            newtext = Static(msg)
            self.cos.mount(newtext)
            self.listitems.append(newtext)

    def open_koder(self):
        file = filedialog.askopenfilename(
            filetypes=[("VTP Files", "*.vtp")]
        )
        if not file:
            return
        with open(file, "r") as f:
            lines = f.readlines()
        for line in lines:
            self.parse(line)

    def boot(self):
        self.progress += 1
        self.load.update(f"Purrfecting Purseces... {self.progress}%")
        if self.progress == 100:
            self.timer.stop()
            self.load.remove()
            appo = Input(placeholder='Type app name to open or "/list" to see all your apps', id="appo")
            self.cos.mount(appo)
            self.addapp("ForeCat.vex", self.open_catvex)
            self.addapp("CatCoder.vex", self.open_koder)

    def listapps(self):
        for app in self.apps:
            newitem = Static(app)
            self.cos.mount(newitem)
            self.listitems.append(newitem)        

    def start(self):
        self.timer = self.set_interval(self.bootspeed, self.boot)

    def on_input_submitted(self, event: Input.Submitted):
        command = event.value
        if event.input.id == "boot":
            if command == "/meow":
                event.input.display = "none"
                self.load = Static("Purrfecting Purseces... 1%")
                self.cos.mount(self.load)
                self.start()
        elif event.input.id == "appo":
            if command == '/list':
                self.listapps()
            if command in self.apps:
                self.apps[command]()

        event.input.clear()


PurrOs().run()

root.destroy()