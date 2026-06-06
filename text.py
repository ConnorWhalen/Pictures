from time import sleep

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.css.scalar import ScalarOffset
from textual.events import Key
from textual.geometry import Offset
from textual.widgets import Static
from rich.text import Text

from stream_audio import AudioPlayer, SONG_PATH


PAINTING_HEIGHT = 48
PAINTING_WIDTH = 115
TITLE_HEIGHT = 56
TITLE_WIDTH = 115
TEXT_HEIGHT = 8
TEXT_WIDTH = 60

START_SECTIONS = [
    ("start1", 0, 10, "On August 4th 1873, Russian architect and painter Viktor Hartmann died suddenly at the age of 39."),
    ("start2", 8, 10, "The Imperial Academy of Arts held an exhibition of over 400 of his works the following year."),
    ("start3", 18, 10, "Inspired by his friend's work, composer Modest Mussorgsky wrote this ten-part suite."),
]

START_PAINTINGS = [
    ("hartmann", 18),
    ("mussorgsky", 10),
]

_SECTIONS = [  # test sections
    ("promenade1", 20, 10, "Promenade I"), # 1:42
    (
        "gnomus", 30, 10, 
        " 1. Gnomus\n"
        "\\[The Gnome]"
    ), # 2:44
    ("promenade2", 40, 10, "Promenade II"), # 0:58
    (
        "castle",50, 10,
        "2. Il vecchio castello\n"
        "   \\[The Old Castle]"
    ), # 4:47
    ("promenade3", 60, 10, "Promenade III"), # 0:32
    (
        "tuileries", 70, 10,
        "3. Tuileries (Dispute d'enfants après jeux)\n"
        "     \\[Children's Quarrel after Games]"
    ), # 1:04
    ("bydlo", 80, 10, "4. Bydło \\[Cattle]"), # 2:21
    ("promenade4", 90, 10, "Promenade IV"), # 0:43
    (
        "chicks", 100, 10,
        "5. Balet nevylupivshikhsya ptentsov\n"
        "   \\[Ballet of Unhatched Chicks]"
    ), # 1:20
    (
        "goldenberg", 110, 10,
        "6. Samuel Goldenberg und Shmuÿle\n"
        "\\[Samuel Goldenberg and Shmuÿle]"
    ), # 2:10
    (
        "market", 120, 10,
        "7. Limoges. Le marché (La grande nouvelle)\n"
        "      \\[The Market (The Great News)]"
    ), # 1:40
    (
        "catacombs1", 130, 10,
        "8a. Catacombae (Sepulcrum romanum)"
        "     \\[Catacombs (Roman Tomb)]"
    ), # 1:53
    (
        "catacombs2", 140, 10,
        " 8b. Cum mortuis in lingua mortua"
        "\\[With the Dead in a Dead Language]"
    ), # 1:53
    (
        "babayaga", 150, 10,
        "9. Izbushka na kuryikh nozhkakh (Baba-Yaga)\n"
        "          \\[The Hut on Hen's Legs]"
    ), # 3:33
    (
        "kiev", 160, 10,
        "10. Bogatyrskiye vorota (V stolnom gorode vo Kiyeve)\n"
        "    \\[The Bogatyr Gates (In the Capital in Kiev)]"
    ), # 5:29
]

SECTIONS = [
    ("promenade1a", 23, 14, "Promenade I"), # 1:42
    ("promenade1b", 37, 14, "The promenades serve as the suite's \"overworld theme\""), # 1:42
    ("promenade1c", 51, 14, "Critic Victor Stasov was a peer of Hartmann and Mussorgsky. The suite is dedicated to him."), # 1:42
    (
        "promenade1d", 65, 23,
        "Stasov: In this piece Mussorgsky depicts himself \"roving through the exhibition, now leisurely, now briskly in order to come close to a picture that had attracted his attention, and at times sadly, thinking of his departed friend.\""
    ), # 1:42
    ("promenade1e", 88, 14, "Promenade I"), # 1:42
    (
        "gnomus1", 102, 14,
        " 1. Gnomus\n" +
        "\\[The Gnome]"
    ), # 2:44
    (
        "gnomus2", 116, 14,
        "Stasov: \"A sketch depicting a little gnome, clumsily running with crooked legs.\""
    ), # 2:44
    (
        "gnomus3", 130, 14,
        "Several of Hartmann's original pictures have been lost, including Gnomus. Alternative artwork is used for these pieces."
    ), # 2:44
    (
        "gnomus4", 144, 14,
        "In The Big Lebowski, The Dude's landlord Marty performs his interpretive dance to this piece."
    ), # 2:44
    (
        "gnomus5", 158, 108,
        " 1. Gnomus\n" +
        "\\[The Gnome]"
    ), # 2:44
    ("promenade2a", 266, 14, "Promenade II"), # 0:58
    (
        "promenade2b", 280, 14,
        "Mussorgsky's original piece was written for piano. French composer Maurice Ravel wrote this orchestration in 1922."
    ), # 0:58
    ("promenade2c", 294, 30, "Promenade II"), # 0:58
    (
        "castle1", 324, 14,
        "2. Il vecchio castello\n" +
        "   \\[The Old Castle]"
    ), # 4:47
    (
        "castle2", 338, 14,
        "Stasov: \"A medieval castle before which a troubadour sings a song.\""
    ), # 4:47
    (
        "castle3", 352, 259,
        "2. Il vecchio castello\n" +
        "   \\[The Old Castle]"
    ), # 4:47
    ("promenade3", 611, 32, "Promenade III"), # 0:32
    (
        "tuileries1", 643, 14,
        "3. Tuileries (Dispute d'enfants après jeux)\n" +
        "     \\[Children's Quarrel after Games]"
    ), # 1:04
    (
        "tuileries2", 657, 14,
        "Stasov: \"An avenue in the garden of the Tuileries, with a swarm of children and nurses.\""
    ), # 1:04
    (
        "tuileries3", 671, 36,
        "3. Tuileries (Dispute d'enfants après jeux)\n" +
        "     \\[Children's Quarrel after Games]"
    ), # 1:04
    (
        "bydlo1", 707, 14,
        "4. Bydło \\[Cattle]"
    ), # 2:21
    (
        "bydlo2", 721, 14,
        "Stasov: \"A Polish cart on enormous wheels, drawn by oxen.\""
    ), # 2:21
    (
        "bydlo3", 735, 113,
        "4. Bydło \\[Cattle]"
    ), # 2:21
    ("promenade4a", 848, 14, "Promenade IV"), # 0:43
    ("promenade4b", 862, 19, "\"Pictures\" was never performed within Mussorgsky's lifetime. Its subject matter was considered radical and the piece was shelved until Nikolai Rimsky-Korsakov published it 5 years after Mussorgsky's death."), # 0:43
    ("promenade4c", 881, 10, "Promenade IV"), # 0:43
    (
        "chicks1", 891, 14,
        "5. Balet nevylupivshikhsya ptentsov\n" +
        "   \\[Ballet of Unhatched Chicks]"
    ), # 1:20,
    (
        "chicks2", 905, 14,
        "Stasov: \"Hartmann's design for the décor of a picturesque scene in the ballet Trilby.\""
    ), # 1:20
    (
        "chicks3", 919, 52,
        "5. Balet nevylupivshikhsya ptentsov\n" +
        "   \\[Ballet of Unhatched Chicks]"
    ), # 1:20,
    (
        "goldenberg1", 971, 14,
        "6. Samuel Goldenberg und Shmuÿle\n" +
        "\\[Samuel Goldenberg and Shmuÿle]"
    ), # 2:10,
    (
        "goldenberg2", 985, 14,
        "Stasov: \"Two Jews: rich and poor\""
    ), # 2:10
    (
        "goldenberg3", 999, 102,
        "6. Samuel Goldenberg und Shmuÿle\n" +
        "\\[Samuel Goldenberg and Shmuÿle]"
    ), # 2:10,
    (
        "market1", 1101, 14,
        "7. Limoges. Le marché (La grande nouvelle)\n" +
        "      \\[The Market (The Great News)]"
    ), # 1:40
    (
        "market2", 1115, 14,
        "Stasov: \"French women quarrelling violently in the market.\""
    ), # 1:40
    (
        "market3", 1129, 72,
        "7. Limoges. Le marché (La grande nouvelle)\n" +
        "      \\[The Market (The Great News)]"
    ), # 1:40
    (
        "catacombs1a", 1201, 14,
        "8a. Catacombae (Sepulcrum romanum)\n" +
        "     \\[Catacombs (Roman Tomb)]"
    ), # 1:53
    (
        "catacombs1b", 1215, 14,
        "Stasov: \"Hartmann represented himself examining the Paris catacombs by the light of a lantern.\""
    ), # 1:53
    (
        "catacombs1c", 1229, 85,
        "8a. Catacombae (Sepulcrum romanum)\n" +
        "     \\[Catacombs (Roman Tomb)]"
    ), # 1:53
    (
        "catacombs2", 1314, 113,
        " 8b. Cum mortuis in lingua mortua\n" +
        "\\[With the Dead in a Dead Language]"
    ), # 1:53
    (
        "babayaga1", 1427, 14,
        "9. Izbushka na kuryikh nozhkakh (Baba-Yaga)\n" +
        "          \\[The Hut on Hen's Legs]"
    ), # 3:33
    (
        "babayaga2", 1441, 14,
        "Stasov: \"Hartmann's drawing depicted a clock in the form of Baba Yaga's hut on hen's legs. Mussorgsky added the witch's flight in a mortar.\""
    ), # 3:33
    (
        "babayaga3", 1455, 14,
        "This piece is used as a boss theme in the video game Catherine"
    ), # 3:33
    (
        "babayaga4", 1469, 171,
        "9. Izbushka na kuryikh nozhkakh (Baba-Yaga)\n" +
        "          \\[The Hut on Hen's Legs]"
    ), # 3:33
    (
        "kiev1", 1640, 14,
        "10. Bogatyrskiye vorota (V stolnom gorode vo Kiyeve)\n" +
        "    \\[The Bogatyr Gates (In the Capital in Kiev)]"
    ), # 5:29
    (
        "kiev2", 1654, 14,
        "Stasov: \"Hartmann's sketch was his design for city gates at Kiev in the ancient Russian massive style with a cupola shaped like a slavonic helmet.\""
    ), # 5:29
    (
        "kiev3", 1668, 301,
        "10. Bogatyrskiye vorota (V stolnom gorode vo Kiyeve)\n" +
        "    \\[The Bogatyr Gates (In the Capital in Kiev)]"
    ), # 5:29
]

PAINTING_SEQUENCE = [
    (None, 51), # 1:42
    ("stasov", 37), # 1:42
    (None, 14), # 1:42
    ("gnomus", 164), # 2:44
    (None, 58), # 0:58
    ("castle", 287), # 4:47
    (None, 32), # 0:32
    ("tuileries", 64), # 1:04
    ("bydlo", 141), # 2:21
    (None, 43), # 0:43
    ("chicks", 80), # 1:20
    (["goldenberg", "schmuyle"], 130), # 2:10
    ("market", 100), # 1:40
    ("catacombs", 226), # 1:53
    ("babayaga", 213), # 3:33
    ("kiev", 329), # 5:29
]

_PAINTING_SEQUENCE = [  # test sections
    (None, 30), # 1:42
    (["goldenberg", "schmuyle"], 10), # 2:10
    (None, 10), # 0:58
    ("castle", 10), # 4:47
    (None, 10), # 0:32
    ("tuileries", 10), # 1:04
    ("bydlo", 10), # 2:21
    (None, 10), # 0:43
    ("chicks", 10), # 1:20
    ("gnomus", 10), # 2:44
    ("market", 10), # 1:40
    ("catacombs", 20), # 1:53
    ("babayaga", 10), # 3:33
    ("kiev", 10), # 5:29
]

PAINTINGS = [
    "hartmann",
    "mussorgsky",
    "stasov",
    "gnomus",
    "castle",
    "bydlo",
    "tuileries",
    "chicks",
    "goldenberg",
    "schmuyle",
    "market",
    "catacombs",
    "babayaga",
    "kiev",
]

class Block:
    def __init__(self, content, padding, height, width, pos_x, pos_y, screen_width, border = False):
        self.box = Static(content)
        self.box.styles.padding = padding
        self.box.styles.height = height
        self.box.styles.width = width
        self.box.styles.content_align = ("center", "middle")
        self.box.styles.offset = Offset(pos_x - screen_width/2, pos_y)
        if border:
            self.box.styles.border = ("solid", "rgb(156, 121, 55)")
        self.box.visible = False

        self.height = height
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.start_time = 0
        self.end_time = 0
    
    def widget(self):
        return self.box
    
    def start(self):
        return self.start_time
    
    def set_pos_x(self, pos_x, screen_width):
        self.pos_x = pos_x
        self.box.styles.offset = Offset(pos_x - screen_width/2, self.pos_y)

    
    def program(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
    
    def animate(self, screen_width):
        self.box.visible = True

        transition_time = 2.0

        self.box.styles.animate(
            "offset",
            value=ScalarOffset.from_offset(
                (
                    self.pos_x + screen_width/2.0,
                    self.pos_y
                )
            ),
            easing="linear",
            duration=transition_time
        )
        self.box.styles.animate(
            "offset",
            value=ScalarOffset.from_offset(
                (
                    self.pos_x + screen_width*1.8,
                    self.pos_y
                )
            ),
            easing="linear",
            duration=transition_time,
            delay=(self.end_time - self.start_time) - transition_time
        )


class AnimationApp(App):
    def compose(self) -> ComposeResult:
        self.started = False
        self.paintings_dict = {}
        self.texts_dict = {}

        height_cursor = 0

        self.menu_block = Block(
            Text.from_ansi(open(f"out/menu.txt", mode="r", encoding='utf-8').read()),
            (0, 0),
            TITLE_HEIGHT,
            TITLE_WIDTH,
            self.screen.size.width - TITLE_WIDTH/2,
            height_cursor,
            self.screen.size.width,
            border=True,
        )
        self.menu_block.widget().visible = True

        height_cursor -= TITLE_HEIGHT

        for painting in PAINTINGS:
            x_pos = -PAINTING_WIDTH/2
            if painting == "goldenberg":
                x_pos -= 40
            elif painting == "schmuyle":
                x_pos += 40

            p_block = Block(
                Text.from_ansi(open(f"out/{painting}_bold.txt", mode="r", encoding='utf-8').read()),
                (0, 0),
                PAINTING_HEIGHT,
                PAINTING_WIDTH,
                x_pos,
                height_cursor,
                self.screen.size.width,
            )

            self.paintings_dict[painting] = p_block
            height_cursor -= PAINTING_HEIGHT
        
        for tag, _start, _duration, text in SECTIONS + START_SECTIONS:
            t_block = Block(
                text,
                (0, 2),
                TEXT_HEIGHT,
                TEXT_WIDTH,
                -TEXT_WIDTH/2,
                height_cursor + PAINTING_HEIGHT,
                self.screen.size.width,
                border=True
            )

            self.texts_dict[tag] = t_block
            height_cursor -= TEXT_HEIGHT

        self.title_block = Block(
            Text.from_ansi(open(f"out/titlecolor.txt", mode="r", encoding='utf-8').read()),
            (0, 0),
            TITLE_HEIGHT,
            TITLE_WIDTH,
            -TITLE_WIDTH/2,
            height_cursor,
            self.screen.size.width,
        )

        height_cursor -= TITLE_HEIGHT

        self.styles.overflow_x = "hidden"
        self.styles.overflow_y = "hidden"
    
        self.container = Vertical(
            self.menu_block.widget(),
            *[p.widget() for p in self.paintings_dict.values()],
            *[t.widget() for t in self.texts_dict.values()],
            self.title_block.widget(),
        )
        self.container.styles.overflow_x = "hidden"
        self.container.styles.overflow_y = "hidden"
        yield self.container

    def on_key(self, event: Key) -> None:
        if event.key == "enter" and not self.started:
            self.started = True
            self.menu_block.widget().visible = False
            self.start()

    def on_mount(self):
        pass

    def start(self):
        self.audio_player = AudioPlayer(SONG_PATH)

        time_cursor = 0.0

        for tag, start, duration, _text in START_SECTIONS:
            self.texts_dict[tag].program(time_cursor + start, time_cursor + start + duration)
        
        time_cursor = START_SECTIONS[-1][1] + START_SECTIONS[-1][2]

        self.audio_player.start(defer=time_cursor)
        self.start_delay = time_cursor

        self.title_block.program(time_cursor + 6.0, time_cursor + 23.0)

        for tag, start, duration, _text in SECTIONS:
            self.texts_dict[tag].program(time_cursor + start, time_cursor + start + duration)

        time_cursor = 0.0

        for painting, duration in START_PAINTINGS + PAINTING_SEQUENCE:
            if painting is not None:
                if isinstance(painting, list):
                    for p in painting:
                        self.paintings_dict[p].program(time_cursor, time_cursor + duration)
                else:
                    self.paintings_dict[painting].program(time_cursor, time_cursor + duration)

            time_cursor += duration
        
        self.to_animate: list[Block] = list(self.texts_dict.values()) + [self.title_block] + list(self.paintings_dict.values())
        
        self.interval = 0.25
        self.start_time_pos = 0

        def poll():
            if self.start_time_pos < self.start_delay:
                self.start_time_pos += self.interval

            time_pos = self.start_time_pos + self.audio_player.get_pos()

            for i in range(len(self.to_animate)-1, -1, -1):
                block = self.to_animate[i]

                if time_pos > block.start():
                    block.animate(self.screen.size.width)
                    self.to_animate.pop(i)
            
            if self.audio_player.get_pos() >= 1967:
                self.exit()

        self.set_interval(self.interval, poll)    
    
    def on_resize(self):
        self.menu_block.set_pos_x(self.screen.size.width - TITLE_WIDTH/2, self.screen.size.width)

    def on_unmount(self):
        if hasattr(self, "audio_player"):
            self.audio_player.terminate()


if __name__ == "__main__":
    app = AnimationApp()
    app.run()
