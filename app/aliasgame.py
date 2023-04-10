from tools.cross import get_cross_coord

from tkinter import *
import os


PICTURE = './resources/alias_img.png'
RULES = './resources/rules.txt'
MAIN_BG = '#395C6B'
BUTTON_BG = '#FFE156'
BUTTON_BG_UNDER_MOUSE = '#DFFFFD'
FONT = ('Roman', 14, 'normal')


def alias():
        root = Tk()
        main_win = MainWindow(root)
        path = os.path.abspath(PICTURE)
        img = PhotoImage(file=path)  # maybe bug of tkinter
        width = img.width()
        height = img.height()
        main_win.render(width, height)
        main_win.alias_label.create_image(1, 1, image=img, anchor=NW)
        root.mainloop()


class Window:
    def __init__(self, root):
        self.root = root
        self.widgets = []
        self.pack_configurations = []  # I haven't made up anything more clever

    def render(self, *args):
        pass

    def button_config(self, bt: Button, width=20):
        bt.config(width=width, height=2)
        bt.config(bg=BUTTON_BG, font=FONT)
        bt.config(relief=SUNKEN)
        bt.config(activebackground=BUTTON_BG_UNDER_MOUSE)

    def erase_widgets(self, widgets: list):
        for widget in widgets:
            widget.pack_forget()

    def render_widgets(self):
        for i in range(len(self.widgets)):
            self.widgets[i].pack(**self.pack_configurations[i])


class MainWindow(Window):
    def __init__(self, root):
        Window.__init__(self, root)
        self.alias_label = None
        self.buttons = [
            ('ADD WORDS', AddWords(root, self).render),
            ('RULES', Rules(root, self).render),
            ('PLAY', Play(root, self).render),
        ]

    def render(self, width, height):
        Label(self.root, bg=MAIN_BG).pack(side=TOP, fill=X)     # empty space on the top
        Label(self.root, bg=MAIN_BG).pack(side=BOTTOM, fill=X)  # empty space on the bottom
        self.create_alias_label(width, height)
        self.render_alias_label()
        self.create_win()
        self.render_widgets()
        self.root_config(width)

    def create_alias_label(self, width, height):
        can = Canvas(self.root, bg=MAIN_BG, highlightbackground=MAIN_BG)
        can.config(width=width, height=height)
        self.alias_label = can

    def create_win(self):
        for text, command in self.buttons:
            bt = Button(self.root, text=text, command=command)
            self.button_config(bt)
            self.widgets.append(bt)
            self.pack_configurations.append({'side': BOTTOM, 'anchor': S, 'pady': 1})

    def render_alias_label(self):
        self.alias_label.pack()

    def root_config(self, width):
        self.place_window(width + 60, 470)
        self.root.resizable(False, False)
        self.root.config(bg=MAIN_BG)
        self.root.bind('<Escape>', lambda event: self.root.quit())

    def place_window(self, win_width, win_height):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x_cordinate = int((screen_w / 2) - (win_width / 2))
        y_cordinate = int((screen_h / 2) - (win_height / 2))
        self.root.geometry("{}x{}+{}+{}".format(win_width, win_height, x_cordinate, y_cordinate))


class Rules(Window):
    def __init__(self, root, main_win: MainWindow):
        Window.__init__(self, root)
        self.main_win = main_win

    def render(self):
        self.erase_widgets(self.main_win.widgets)
        self.main_win.alias_label.pack_forget()
        if len(self.widgets) == 0:
            self.create_widgets()
        self.render_widgets()

    def create_widgets(self):
        bt = Button(self.root, text='Back', command=self.back_to_main_win)
        self.button_config(bt)
        self.widgets.append(bt)
        self.pack_configurations.append({'side': BOTTOM, 'pady': (10, 0)})

        scroll = Scrollbar(self.root)
        text = Text(self.root)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        self.widgets.extend([scroll, text])
        self.pack_configurations.extend([{'side': RIGHT, 'padx': (0, 10), 'fill': Y},
                                         {'side': LEFT, 'padx': (10, 0)}])
        text.insert('1.0', self.get_rules_text())
        text.config(state=DISABLED, font=FONT, wrap=WORD)

    def get_rules_text(self):
        """
        :return: string with rules of the game
        """
        with open(RULES) as file:
            rules = file.read()
        return rules

    def back_to_main_win(self):
        self.erase_widgets(self.widgets)
        self.main_win.render_alias_label()
        self.main_win.render_widgets()


class AddWords(Window):
    def __init__(self, root, main_win: MainWindow):
        Window.__init__(self, root)
        self.main_win = main_win
        self.adder = Adder(root, self.widgets, self.pack_configurations)

    def render(self):
        """
        At this point a user can be suggested to choose the way of adding new words
        """
        self.add_words_manually()

    def add_words_manually(self):
        self.erase_widgets(self.main_win.widgets)
        if len(self.widgets) == 0:
            self.create_widgets()
        self.render_widgets()
        self.adder.create_entry_and_cross()

    def create_widgets(self):
        fr = Frame(self.root, bg=MAIN_BG)
        self.widgets.append(fr)
        self.pack_configurations.append({'padx': (30, 30), 'pady': (10, 10)})
        self.adder.create_canvas_scrollbar(fr)
        self.create_bts()

    def create_bts(self):
        def back():
            self.back_to_init_state()
            self.back_to_main_win()

        back_bt = Button(self.root, text='Back', command=back)
        self.button_config(back_bt, width=10)
        add_bt = Button(self.root, text='Add', command=lambda: self.add_entries())
        self.button_config(add_bt, width=10)
        self.widgets.extend([back_bt, add_bt])
        self.pack_configurations.extend([{'side': LEFT, 'padx': (30, 0)},
                                        {'side': RIGHT, 'padx': (0, 30)}])

    def add_entries(self):
        #TODO some logic of processing data base
        for i in self.adder.entries:
            print(i.get())
        self.back_to_init_state()
        self.adder.create_entry_and_cross()

    def back_to_main_win(self):
        self.erase_widgets(self.widgets)
        self.main_win.render_widgets()

    def back_to_init_state(self):
        self.adder.back_to_init_state()
        self.root.bind("<Button-4>", None)
        self.root.bind("<Button-5>", None)


class Adder:
    def __init__(self, root, widgets, pack_configurations, canvas_height=200):
        self.root = root
        self.widgets = widgets
        self.pack_configurations = pack_configurations
        self.entries = []
        self.increment = 33
        self.start_entry_text = 'Type here'
        self.error_entry_text = 'Input a number'
        self.var_config()
        self.canvas = None
        self.scrollbar = None
        self.canvas_height = canvas_height

    def var_config(self):
        # TODO more adequate computations
        self.ent_x, self.ent_y = 172, 13  # 122 13
        self.cross_x1, self.cross_y1, self.cross_x2, self.cross_y2 = 0, 40, 30, 70
        self.scrollbar_is_packed = False

    def create_canvas_scrollbar(self, fr):
        scroll = Scrollbar(fr)
        can = Canvas(fr)
        scroll.config(command=can.yview)
        can.config(yscrollcommand=scroll.set)
        self.widgets.append(can)
        self.pack_configurations.append({'side': LEFT})
        self.scrollbar = scroll
        self.canvas = can
        self.canvas_config()

    def canvas_config(self):
        self.canvas.config(highlightthickness=0, bg=MAIN_BG,
                           highlightbackground=MAIN_BG,
                           height=self.canvas_height, width=330)
        self.canvas.tag_bind('cross', "<Enter>",
                        lambda event: self.canvas.itemconfig('cross', fill=BUTTON_BG_UNDER_MOUSE))
        self.canvas.tag_bind('cross', "<Leave>",
                        lambda event: self.canvas.itemconfig('cross', fill=BUTTON_BG))
        self.canvas.tag_bind('cross', "<Button-1>", lambda event: self.create_entry_and_cross())

    def create_entry_and_cross(self, ent=None):
        can = self.canvas
        can.delete('cross')
        self.create_entry(ent)
        self.create_cross()

        if self.cross_y2 > can.winfo_reqheight():
            if not self.scrollbar_is_packed:
                self.scrollbar.pack(side=RIGHT, fill=Y)
                self.scrollbar_is_packed = True
                self.root.bind("<Button-4>", lambda event: can.yview_scroll(-1, "units"))
                self.root.bind("<Button-5>", lambda event: can.yview_scroll(1, "units"))
            can.config(scrollregion=(0, 0, 300, self.cross_y2 + self.increment))
        self.ent_y += self.increment
        self.cross_y1 += self.increment
        self.cross_y2 += self.increment

    def create_entry(self, ent=None):
        if ent is None:
            ent = Entry(self.canvas)
            self.entry_config(ent)
        ent.pack()
        self.entries.append(ent)
        self.canvas.create_window(self.ent_x, self.ent_y, window=ent)

    def entry_config(self, ent: Entry):
        ent.config(font=FONT, width=20)
        ent.insert(0, self.start_entry_text)

        def ent_handler(event):
            if ent.get() == self.start_entry_text or ent.get() == self.error_entry_text:
                ent.delete(0, END)
                ent.config(fg='black')
        ent.bind('<1>', ent_handler)

    def create_cross(self):
        # TODO there is no possibility to minus if we want decrease the amount of entries
        id = self.canvas.create_polygon(*get_cross_coord(self.cross_x1, self.cross_y1,
                                                    self.cross_x2, self.cross_y2,
                                                    endx=10, endy=10))
        self.canvas.itemconfig(id, outline='black', fill=BUTTON_BG,
                          tags='cross', width=1)

    def back_to_init_state(self):
        self.scrollbar.pack_forget()
        self.canvas.delete('all')
        for child in self.canvas.winfo_children():
            child.destroy()
        self.var_config()
        # may be it is worth to up the down
        self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()))
        self.entries.clear()


class Play(Window):
    def __init__(self, root, main_win: MainWindow):
        Window.__init__(self, root)
        self.main_win = main_win
        self.adder = Adder(root, self.widgets, self.pack_configurations, canvas_height=160)
        self.settings = Settings(self.widgets, self.adder)

    def render(self):
        self.erase_widgets(self.main_win.widgets)
        if len(self.widgets) == 0:
            self.create_widgets()
        self.render_widgets()
        self.settings.print_next_page()

    def create_widgets(self):
        fr = Frame(self.root, bg=MAIN_BG)
        label = Label(fr)
        label.config(bg=MAIN_BG, fg=BUTTON_BG, font=FONT)
        self.widgets.extend([fr, label])
        self.pack_configurations.extend([{'padx': (30, 30), 'pady': (10, 10)},
                                         {'side': TOP, 'fill': X, 'pady': (0, 10)}])
        self.adder.create_canvas_scrollbar(fr)
        self.create_bts()

    def create_bts(self):
        back_bt = Button(self.root, text='Back', command=self.back)
        self.button_config(back_bt, width=10)
        next_bt = Button(self.root, text='Next', command=self.next)
        self.button_config(next_bt, width=10)
        self.widgets.extend([back_bt, next_bt])
        self.pack_configurations.extend([{'side': LEFT, 'padx': (30, 0)},
                                        {'side': RIGHT, 'padx': (0, 30)}])

    def back(self):
        if self.settings.back_index == -1:
            self.back_to_main_win()
        else:
            self.settings.print_back_page()

    def next(self):
        try:
            self.settings.entry_checking()
        except ValueError:
            return
        self.settings.next_index += 1
        self.settings.back_index += 1
        cur_ents = self.adder.entries[:]
        self.settings.pages_widgets.append(cur_ents)
        self.clear_canvas()
        if self.settings.next_index < len(self.settings.settings):
            self.settings.print_next_page()
        else:
            self.start_play()

    def clear_canvas(self):
        self.adder.scrollbar.pack_forget()  # TODO It needs only first time for multiple entries
        self.adder.canvas.delete('all')  # TODO It needs only first time for multiple entries
        for child in self.adder.canvas.winfo_children():
            child.pack_forget()
        self.adder.var_config()
        self.adder.entries.clear()

    def back_to_main_win(self):
        self.adder.back_to_init_state()
        self.erase_widgets(self.widgets)
        self.settings.set_var_init_state()
        self.settings.pages_widgets.clear()
        self.main_win.render_widgets()

    def start_play(self):
        game_settings = self.process_settings()
        self.adder.back_to_init_state()
        self.erase_widgets(self.widgets)
        self.settings.set_var_init_state()
        self.settings.pages_widgets.clear()
        Game(self.root, game_settings).start()

    def process_settings(self):
        # TODO possibly it should create new Team obj immediately
        game_settings = []
        for list_of_ents in self.settings.pages_widgets:
            game_settings.append([ent.get() for ent in list_of_ents])

        return game_settings


class Settings:
    def __init__(self, widgets, adder: Adder):
        self.widgets = widgets
        self.adder = adder
        # TODO make more clear way to set settings (text, func, number_checking)
        self.settings = [('Please, input the teams names', self.adder.create_entry_and_cross, False),
                         ('Input the round duration in sec', self.adder.create_entry, True),
                         ('Input the win-score', self.adder.create_entry, True)]
        self.set_var_init_state()

    def set_var_init_state(self):
        self.next_index = 0
        self.back_index = -1
        self.pages_widgets = []

    def print_next_page(self):
        label = self.widgets[1]  # TODO very bad!!!
        text = self.settings[self.next_index][0]
        label.config(text=text)
        func = self.settings[self.next_index][1]
        func()

    def print_back_page(self):
        self.next_index -= 1
        self.back_index -= 1
        label = self.widgets[1]  # TODO very bad!!!
        text = self.settings[self.next_index][0]
        label.config(text=text)

        self.adder.canvas.winfo_children()[-1].destroy()  # TODO demand more flexable destroy
        self.adder.var_config()
        self.adder.entries.clear()

        # if a lot of entries: print them and cross if not - only entry
        for ent in self.pages_widgets[self.next_index]:
            if len(self.pages_widgets[self.next_index]) > 1:
                self.adder.create_entry_and_cross(ent)
            else:
                self.adder.create_entry(ent)
        # return to list of entries its values which was erased after "Next" bt pressed
        self.adder.entries = list(self.pages_widgets.pop(self.next_index))

    def entry_checking(self):
        if self.settings[self.next_index][2]:
            for ent in self.adder.entries:
                try:
                    int(ent.get())
                except ValueError:
                    ent.delete(0, END)
                    ent.insert(0, self.adder.error_entry_text)
                    ent.config(fg='red')
                    raise


class Game:
    """
    Loop iteration is a round
    Before team start to play they asked "Are you ready?"
    (Two buttons 'Quit' 'Yes')
    Game starts and team try to earn points. They can skip word
    (The last two button change its display onto 'Skip', 'Earned'/'Next word')
    When timer display the last 5 seconds it srates bells and blinks
    (timer functionality implements with canvas.after())
    When all teams finished the round the current score appears
    After that the next iteration
    Game continues till the first team earn points equals or more than win-score.
    It will be very good to add some congratulations page and button
    start new game (just refresh scores of teams) of back to main menu
    If round is completed and there are several team whoes points are more than
    win-score then the winner is a team with the biggest amount of points
    """
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings

    def start(self):
        fr = Frame(self.root)
        fr.pack(padx=(30, 30), pady=(10, 10))
        canvas = Canvas(fr)
        canvas.config(highlightthickness=0, bg='white',
                           highlightbackground=MAIN_BG,
                           height=200, width=330)
        canvas.pack()
        bt1 = Button(self.root, text='left', bg=BUTTON_BG, width=10)
        bt1.pack(side=LEFT, padx=(30, 0))
        self.bt_conf(bt1)
        Label(self.root, text=str(self.settings[1][0]), width=10, height=2).pack(side=LEFT, padx=(10, 10))
        bt2 = Button(self.root, text='right', bg=BUTTON_BG, width=10)
        bt2.pack(side=RIGHT, padx=(0, 30))
        self.bt_conf(bt2)

    def bt_conf(self, bt, width=5):
        bt.config(width=width, height=2)
        bt.config(bg=BUTTON_BG, font=FONT)
        bt.config(relief=SUNKEN)
        bt.config(activebackground=BUTTON_BG_UNDER_MOUSE)
# h = self.adder.canvas.winfo_reqheight()
# w = self.adder.canvas.winfo_reqwidth()
# self.adder.canvas.delete('all')
# self.adder.canvas.create_text(w // 2, h // 2, text='Are you ready to start the game?',
#                               fill=BUTTON_BG, font=FONT)
# label = self.widgets[1]
# label.config(text='')
# no = self.widgets[-2]
# yes = self.widgets[-1]
# no.config(text='No', command=self.back_to_main_win)
# yes.config(text='Yes', command=None)
