import os

from textual.app import App, ComposeResult
from textual.events import Key
from textual.geometry import Offset
from textual.widgets import Static
from rich.text import Text


BOX_HEIGHT = 56
BOX_WIDTH = 115

CAPTION_HEIGHT = 3

KIEV = open("kiev-ascii.txt", mode="r", encoding='utf-8').read()

PAINTINGS = [
    "titlecolor",
    "test",
    "gnomus",
    "castle",
    "babayaga",
    "bydlo",
    "catacombs",
    "chicks",
    "goldenberg",
    "kiev",
    "market",
    "schmuyle",
    "tuileries"
]

class AnimationApp(App):
    def compose(self) -> ComposeResult:
        self.boxes = []
        self.filenames = []
        self.cap = None

        # for filename in ["test.txt"]:
        for filename in sorted([f for f in os.listdir("out") if f.endswith(".txt")]):
        # for filename in [f for f in (os.listdir("bold")) if f.endswith(".txt")]:
            box = Static(Text.from_ansi(open(f"out/{filename}", mode="r", encoding='utf-8').read()))
            box.styles.padding = (0, 0)
            box.styles.height = BOX_HEIGHT
            box.styles.width = BOX_WIDTH
            box.styles.content_align = ("center", "middle")
            box.styles.offset = Offset(self.screen.size.width/2 - BOX_WIDTH/2, -(BOX_HEIGHT)*len(self.boxes))
            box.visible = False

            yield box

            self.boxes.append(box)

            self.filenames.append(filename)

        cap = Static(self.filenames[0])
        cap.styles.width = len(self.filenames[0]) + 6
        cap.styles.padding = (1, 2)
        cap.styles.content_align = ("center", "middle")
        cap.styles.offset = Offset(self.screen.size.width/2 - (len(self.filenames[0]) + 6)/2, -(BOX_HEIGHT)*(len(self.boxes)-1))
        cap.styles.border = ("solid", "rgb(156, 121, 55)")
        cap.visible = True

        yield cap

        self.cap = cap
        
        self.boxes[0].visible = True
        self.current = 0


    def on_mount(self):
        pass

    def on_key(self, event: Key) -> None:
        new_i = self.current
        if event.key == "right":
            new_i += 1
            if new_i > len(self.boxes)-1:
                new_i = 0
        elif event.key == "left":
            new_i -= 1
            if new_i < 0:
                new_i = len(self.boxes)-1
        
        if new_i != self.current:
            self.boxes[self.current].visible = False

            self.boxes[new_i].visible = True

            self.cap.content = self.filenames[new_i]
            self.cap.styles.width = len(self.filenames[new_i]) + 6
            self.cap.styles.offset = Offset(self.screen.size.width/2 - (len(self.filenames[new_i]) + 6)/2, -(BOX_HEIGHT)*(len(self.boxes)-1))

            self.current = new_i
            


if __name__ == "__main__":
    app = AnimationApp()
    app.run()