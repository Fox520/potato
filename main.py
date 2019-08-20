from functools import partial

from kivy.clock import Clock, mainthread
from kivymd.list import TwoLineListItem
from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.theming import ThemeManager
from kivymd.toast import toast


def initialize_fonts():
    KIVY_FONTS = [
        {
            "name": "Cursive",
            "fn_regular": "./resources/cursive.ttf"
        }
    ]

    for font in KIVY_FONTS:
        LabelBase.register(**font)


USRNAME = "Potato"
PASSWD = "19"

Builder.load_string("""
#:include login.kv
#:include mainscreen.kv

#:import MDToolbar kivymd.toolbar.MDToolbar
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import MDThemePicker kivymd.pickers.MDThemePicker
#:import MDBottomNavigation kivymd.bottomnavigation.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.bottomnavigation.MDBottomNavigationItem
#:import MDRoundFlatButton kivymd.button.MDRoundFlatButton
#:import SmartTileWithLabel kivymd.imagelists.SmartTileWithLabel
#:import MDRoundFlatIconButton kivymd.button.MDRoundFlatIconButton
#:import MDFloatingActionButton kivymd.button.MDFloatingActionButton
#:import MDSeparator kivymd.cards.MDSeparator
#:import MDTextField kivymd.textfields.MDTextField
#:import MDList kivymd.list.MDList
#:import MDThemePicker kivymd.pickers.MDThemePicker

#:import get_color_from_hex kivy.utils.get_color_from_hex

#:set color_shadow [0, 0, 0, .2980392156862745]
#:set color_lilac [.07058823529411765, .07058823529411765, .14901960784313725, .8]


<MyNavigationDrawerIconButton@NavigationDrawerIconButton>:
    icon: 'checkbox-blank-circle'

<MainNavigationDrawer@MDNavigationDrawer>:
    drawer_logo: "raw_potato.jpg"
    drawer_title: "Hello Potato"

    MyNavigationDrawerIconButton:
        text: "It's your birthday"

    MyNavigationDrawerIconButton:
        text: "Cheers to more smiles"
    
    MyNavigationDrawerIconButton:
        text: "By: Lone Wolf"

    MyNavigationDrawerIconButton:
        text: "Change Theme"
        on_release: MDThemePicker().open()


    """)


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def on_back_pressed(self, *args):
        pass

    def on_menu_pressed(self, *args):
        pass

    def login(self, name, pwd):
        print(name,pwd)
        if name == USRNAME and pwd == PASSWD:
            toast("Login successful")
            sm.current = "conversation_screen"
        else:
            toast("This might not be your app", True)


class Conversation(Screen):

    def __init__(self, **kwargs):
        super(Conversation, self).__init__(**kwargs)
        self.txtMessage = self.ids["txtMessage"]
        self.grid = self.ids["grid"]

    def on_enter(self, *args):
        Clock.schedule_once(self.initiate, 3)

    def initiate(self, dt):
        Clock.schedule_once(partial(self.add_two_line, "Hi Potato!", "Thomas", "#223344"), 0)
        Clock.schedule_once(partial(self.add_two_line, "Hey Thomas", "Didi", "#223344"), 2)
        Clock.schedule_once(partial(self.add_two_line, "It's a special day today!!", "Thomas", "#223344"), 4)
        Clock.schedule_once(partial(self.add_two_line, "I'm wishing you an awesome day filled with all the nice things",
                                    "Thomas", "#223344"), 7)
        Clock.schedule_once(partial(self.add_two_line, "So happy birthday Didi",
                                    "Thomas", "#223344"), 12)
        Clock.schedule_once(partial(self.add_two_line, "This is more original from me ^.^", "Thomas", "#223344"), 15)
        Clock.schedule_once(partial(self.add_two_line, "Awww", "Didi", "#223344"), 17)
        Clock.schedule_once(partial(self.add_two_line, "Now Imma show off", "Didi", "#223344"), 20)
        Clock.schedule_once(partial(self.add_two_line, "Thanks Thomas :-D", "Didi", "#223344"), 23)
        self.txtMessage.disabled = False

    def send_msg(self, text):
        self.add_two_line(text, "Potato")
        Clock.schedule_once(self.do_toast, 2)

    def do_toast(self, dt):
        toast("You talking to yourself now.. hehehe", True)

    @mainthread
    def add_two_line(self, text, name, color="#223344", dt=0):

        a = TwoLineListItem(
            text=text, secondary_text=name, on_release=lambda *args: toast("touch me more"))

        self.grid.add_widget(a)

    def on_back_pressed(self, *args):
        pass

    def on_menu_pressed(self, *args):
        pass


class Tinkle(App):
    global sm
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Yellow'
    theme_cls.theme_style = "Light"
    sm = ScreenManager()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        global sm
        self.bind(on_start=self.post_build_init)
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(Conversation(name="conversation_screen"))
        return sm

    def post_build_init(self, ev):
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)

    def _key_handler(self, *args):
        key = args[1]
        if key in (1000, 27):
            try:
                toast("You're stuck in here. Muahaha", True)
                sm.current_screen.dispatch("on_back_pressed")
            except Exception as e:
                print(e)
            return True
        elif key == 1001:
            try:
                sm.current_screen.dispatch("on_menu_pressed")
            except Exception as e:
                print(e)
            return True


if __name__ == "__main__":
    Tinkle().run()
