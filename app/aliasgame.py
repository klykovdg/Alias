from tools.cross import get_cross_coord
from tools.wordbase import get_words
from app.team import Team

from tkinter import *
import os, random
from multiprocessing import Process, Manager


PICTURE = './resources/alias_img.png'
RULES = './resources/rules.txt'
MAIN_BG = '#395C6B'
BUTTON_BG = '#FFE156'
BUTTON_BG_UNDER_MOUSE = '#DFFFFD'
FONT = ('Roman', 14, 'normal')
TIMER_BG = '#fa574b'
TIMER_FONT = ('Roman', 16, 'normal')


def alias():
        words_base = Manager().list()
        word_base_conaction = Process(target=get_words, args=(words_base,))
        word_base_conaction.start()

        root = Tk()
        main_win = MainWindow(root, word_base_conaction, words_base)
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
    def __init__(self, root, word_base_conaction, words_base):
        Window.__init__(self, root)
        self.word_base_conaction = word_base_conaction
        self.words_base = words_base
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
        self.root.title('Alias Game')
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
        self.canvas = None
        self.scrollbar = None
        self.canvas_height = canvas_height
        self.var_config()


    def var_config(self):
        # TODO more adequate computations
        self.ent_x, self.ent_y = 172, 13  # 122 13
        self.cross_x1, self.cross_y1, self.cross_x2, self.cross_y2 = 0, 40, 30, 70
        self.scrollbar_is_packed = False
        if self.canvas:
            self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()))

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
            can.yview_scroll(self.increment, "units")
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
        game_settings = self.settings.process_settings()
        self.adder.back_to_init_state()
        self.erase_widgets(self.widgets)
        self.settings.set_var_init_state()
        self.settings.pages_widgets.clear()
        Game(self.root, self.main_win, game_settings).start()


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

    def process_settings(self):
        # TODO possibly it should create new Team obj immediately
        arr = self.pages_widgets
        game_settings = []
        game_settings.append([Team(ent.get()) for ent in arr[0]])
        for i in range(1, len(arr)):
            game_settings.append(arr[i][0].get())

        return game_settings


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
    def __init__(self, root, main_win: MainWindow, settings):
        self.root = root
        self.main_win = main_win
        self.teams = settings[0]
        self.cur_team = 0
        self.num_round = 1
        self.duration = int(settings[1])
        self.win_score = int(settings[2])
        self.widgets = []
        self.scrollbar_is_packed = False
        print(settings)

    def start(self):
        self.make_widgets()
        self.main_win.word_base_conaction.join()
        self.new_game()

    def make_widgets(self):
        # TODO make menu for user can open rules during the game
        fr = Frame(self.root, name='fr')
        fr.pack(padx=(30, 30), pady=(10, 10))
        scrollbar = Scrollbar(fr)
        canvas = Canvas(fr)
        canvas.config(highlightthickness=0, bg=MAIN_BG,
                      highlightbackground=MAIN_BG,
                      height=200, width=330)
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT)
        left_bt = Button(self.root)
        left_bt.pack(anchor=SW, padx=(30, 0), side=LEFT)
        self.bt_conf(left_bt)

        right_bt = Button(self.root)
        right_bt.pack(anchor=SE, padx=(0, 30), side=RIGHT)
        self.bt_conf(right_bt)

        timer = Label(self.root, text=str(self.duration), width=10, height=4,
                      bg=TIMER_BG, font=TIMER_FONT, fg='white')
        timer.pack(anchor=S, side=BOTTOM)

        self.timer = timer
        self.left_bt = left_bt
        self.right_bt = right_bt
        self.canvas = canvas
        self.scrollbar = scrollbar
        self.widgets.extend([fr, canvas, scrollbar, left_bt, right_bt, timer])

    def new_game(self):
        self.return_init_state()
        self.round_start_win(self.num_round, self.teams[self.cur_team])

    def return_init_state(self):
        self.canvas.delete(ALL)
        for team in self.teams:
            team.reset_score_to_zero()
        self.num_round = 1
        self.cur_team = 0
        # it's not possible to have more than 10K words, be careful
        self.cur_game_words_base = self.main_win.words_base[:]

    def round_start_win(self, number, team):
        y = 1
        y = self.create_text('Score table', y, 25, 25)
        y = self.print_cur_score_table(y) + 10
        y = self.create_text('Round %d' % number, y, 10, 25)
        y = self.create_text('\nTeam %s! Are you ready?' % team.name, y, 25, 25)

        self.left_bt.config(text='Quit', command=self.back_to_main_menu)
        self.right_bt.config(text='Yes', command=self.yes)

    def yes(self):
        self.left_bt.config(text='Skip', command=self.skip)
        self.right_bt.config(text='Guessed', command=self.guessed)
        self.canvas.delete(ALL)
        self.display_word()
        self.play(self.duration)

    def skip(self):
        team = self.teams[self.cur_team]
        team.down()
        self.canvas.delete(ALL)
        self.display_word()

    def guessed(self):
        team = self.teams[self.cur_team]
        team.up()
        self.canvas.delete(ALL)
        self.display_word()

    def display_word(self):
        # TODO solve case if the words are over
        # TODO bad decor of the card from my point of view
        team = self.teams[self.cur_team]
        self.create_text('Score %d' % team.score, 1, 1, 1)
        index = random.randint(0, len(self.cur_game_words_base) - 1)
        word = self.cur_game_words_base.pop(index)
        width = self.get_card_width(word)
        card = Frame(self.canvas, bg=BUTTON_BG)
        word_on_card = Label(card, text=word, bg=MAIN_BG, fg=BUTTON_BG,
                             width=width, height=4, font=TIMER_FONT, bd=0)
        word_on_card.pack(side=TOP, padx=2, pady=2)
        self.canvas.create_window(self.canvas.winfo_reqwidth() // 2,
                                  self.canvas.winfo_reqheight() // 2,
                                  window=card)

    def get_card_width(self, word):
        sides_space = 6
        default_len = 12
        if len(word) > default_len:
            return len(word) + sides_space
        else:
            return default_len + sides_space

    def play(self, remainder):
        if remainder > 3:
            self.timer.config(text=remainder)
            self.canvas.after(1000, self.play, remainder - 1)
        elif remainder == 0:
            self.end_for_cur_team()
        else:
            self.timer.config(text=remainder, bg=BUTTON_BG_UNDER_MOUSE, fg=TIMER_BG)
            self.timer.bell()
            self.canvas.after(500, self.timer.config, {'bg': TIMER_BG, 'fg': 'white'})
            self.canvas.after(1000, self.play, remainder - 1)

    def end_for_cur_team(self):
        self.update_round_and_cur_team()
        self.timer.config(text=self.duration)
        if self.cur_team == 0:
            self.end_of_round()
        else:
            self.canvas.delete(ALL)
            self.round_start_win(self.num_round, self.teams[self.cur_team])

    def end_of_round(self):
        leaders = self.get_leading_score()
        # if several teams have equal score exceeding win-score the game continue
        if len(leaders) == 1 and leaders[0].score >= self.win_score:
            self.congratulations(leaders[0])
        else:
            self.canvas.delete(ALL)
            self.round_start_win(self.num_round, self.teams[self.cur_team])

    def congratulations(self, team):
        # TODO I like idea with firework
        self.canvas.delete(ALL)
        y = 1
        y = self.create_text('Score table', y, 25, 25)
        y = self.print_cur_score_table(y) + 10
        y = self.create_text('Congratulations %s!' % team.name, y, 25, 25)
        y = self.create_text('You are winner!', y, 10, 25)

        self.left_bt.config(text='Quit', command=self.back_to_main_menu)
        self.right_bt.config(text='New', command=self.new_game)

    def bt_conf(self, bt, width=5):
        bt.config(width=width, height=2)
        bt.config(bg=BUTTON_BG, font=FONT)
        bt.config(relief=SUNKEN)
        bt.config(activebackground=BUTTON_BG_UNDER_MOUSE)

    def get_leading_score(self):
        leading_score = 0
        leaders = []  # in case when several teams have the same score which more than win-score
        for team in self.teams:
            if leading_score < team.score:
                leading_score = team.score
                leaders.clear()
                leaders.append(team)
            elif leading_score == team.score:
                leaders.append(team)

        return leaders

    def create_text(self, text, y, incr, line_y_size):
        self.canvas.create_text(self.canvas.winfo_reqwidth() // 2, y, anchor=N,
                                text=text, fill=BUTTON_BG, font=FONT)
        y += incr
        self.check_canvas_height_and_cur_y(y, line_y_size)

        return y

    def print_cur_score_table(self, y):
        font = ('Roman', 12, 'normal')
        data = [(team.name, team.score) for team in self.teams]
        for n, s in data:
            fr = Frame(self.canvas, bg=MAIN_BG)
            fr.pack()
            Label(fr, text=n, width=15, font=font, bg=MAIN_BG, fg=BUTTON_BG, anchor=W).pack(side=LEFT)
            Label(fr, text=s, width=3, font=font, bg=MAIN_BG, fg=BUTTON_BG).pack(side=RIGHT)
            self.canvas.create_window(self.canvas.winfo_reqwidth() // 2, y, anchor=N, window=fr)
            y += 20
            self.check_canvas_height_and_cur_y(y, 20)
        return y

    def check_canvas_height_and_cur_y(self, y, incr):
        if y > self.canvas.winfo_reqheight():
            if not self.scrollbar_is_packed:
                self.scrollbar.pack(side=RIGHT, fill=Y)
                self.root.bind("<Button-4>", lambda event: self.canvas.yview_scroll(-1, "units"))
                self.root.bind("<Button-5>", lambda event: self.canvas.yview_scroll(1, "units"))
                self.scrollbar_is_packed = True
            self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_reqwidth(), y + incr))

    def update_round_and_cur_team(self):
        if (self.cur_team + 1) == len(self.teams):
            self.num_round += 1
            self.cur_team = (self.cur_team + 1) % len(self.teams)
        else:
            self.cur_team += 1

    def back_to_main_menu(self):
        for widget in self.widgets:
            widget.destroy()
        self.main_win.render_widgets()