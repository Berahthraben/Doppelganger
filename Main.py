import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
from kivy.config import Config

Config.set('kivy', 'log_level', 'error')
Config.write()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup

from functools import partial
from Functions import Controller
import tkinter as tk
from tkinter import filedialog
import sys, os, threading

# TODO:
# - CONFIRMATION/ERROR POPUPS
# - DELETE MESSAGES BUTTON
# - CHANNEL BROWSER
# - LOAD/RELOAD/SAVE FILE BUTTON
# - REMOVE EMPTY SERVERS/BUGGED

controller = Controller("")
current_event = ""


class DeleteMessagesPopup(Popup):
    def check_controller_state(self, thr, settingui, dp):
        global controller, current_event
        if thr.is_alive():
            self.ids["progress"].value = controller.load_percentage
        else:
            self.dismiss()
            Clock.unschedule(current_event)
            #print(Clock.get_events())
            settingui.send_message_btn_func()


class SendFilePopup(Popup):
    def check_controller_state(self, thr, dp):
        global controller, current_event
        if thr.is_alive():
            self.ids["progress"].value = controller.load_percentage
        else:
            self.dismiss()
            Clock.unschedule(current_event)
            Window.enabled = True


class LoadFilePopup(Popup):
    def check_controller_state(self, thr, dp):
        global controller, current_event
        if thr.is_alive():
            self.ids["progress"].value = controller.load_percentage
        else:
            self.dismiss()
            Clock.unschedule(current_event)
            Window.enabled = True


class DeleteConfirmationPopup(Popup):

    def delete_confirm(self, settingui, dp):
        global current_event
        self.dismiss()
        thr = threading.Thread(target=controller.delete_message_all)
        thr.start()
        pop = DeleteMessagesPopup(auto_dismiss=False)
        pop.open()
        Window.enabled = False
        current_event = Clock.schedule_interval(partial(pop.check_controller_state, thr, settingui), 1 / 10.)

    def delete_reject(self, settingui, dp):
        self.dismiss()
        settingui.send_message_btn_func()


class Attachment(BoxLayout):
    def show_load(self):
        root = tk.Tk()
        root.withdraw()
        self.ids["attachment"].text = filedialog.askopenfilename().replace("/", "\\")
        return


class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children[0].ids["loaded_file_lbl"].text = "File loaded: \n" + controller.file_path


class SettingsUI(BoxLayout):

    def on_checkbox_active(self, checkbox, active):
        if active:
            self.ids["attachments_layout"].disabled = False
            self.ids["attachments_chk_layout"].disabled = False
            self.ids["spoiler_chk"].disabled = False
            self.ids["legacy_chk"].disabled = False
            self.ids["add_widget_btn"].disabled = False
            self.ids["spoiler_lbl"].disabled = False
            self.ids["legacy_lbl"].disabled = False
        else:
            self.ids["attachments_layout"].disabled = True
            self.ids["attachments_chk_layout"].disabled = True
            self.ids["spoiler_chk"].disabled = True
            self.ids["spoiler_chk"].active = False
            self.ids["legacy_chk"].disabled = True
            self.ids["legacy_chk"].active = False
            self.ids["add_widget_btn"].disabled = True
            self.ids["spoiler_lbl"].disabled = True
            self.ids["legacy_lbl"].disabled = True

    def adicionar_attachment(self):
        att_layout = self.ids["attachments_layout"]
        att_layout.add_widget(Attachment())
        att_layout.size_hint_y = att_layout.size_hint_y + 0.15

    def check_deletion(self):
        if controller.previous_delete:
            Window.disabled = True
            popup = DeleteConfirmationPopup(auto_dismiss=False)
            popup.ids["popup_yes_btn"].bind(
                on_release=partial(popup.delete_confirm, self))
            popup.ids["popup_no_btn"].bind(
                on_release=partial(popup.delete_reject, self))
            popup.open()
            Window.disabled = False
        else:
            self.send_message_btn_func()

    # Send message
    def send_message_btn_func(self, *args):
        global controller, current_event
        paths = []
        message = self.ids["message_txt"].text
        delay = 0
        spoiler = False
        legacy = False
        save_ids = False
        if self.ids["attachments_chk"].active:
            for child in self.ids["attachments_layout"].children:
                if child.ids["attachment"].text != "":
                    paths.append(child.ids["attachment"].text)
        if self.ids["delay_chk"].active:
            delay = 2
        if self.ids["spoiler_chk"].active:
            spoiler = True
        if self.ids["legacy_chk"].active:
            legacy = True
        if self.ids["save_ids_chk"].active:
            save_ids = True
        pop = SendFilePopup(auto_dismiss=False)
        pop.open()
        Window.enabled = False
        thr = threading.Thread(target=partial(controller.send_message,
                                              paths,
                                              message,
                                              delay,
                                              spoiler,
                                              legacy
                                              ,save_ids))
        thr.start()
        current_event = Clock.schedule_interval(partial(pop.check_controller_state, thr), 1 / 10.)


class DoppelApp(App):
    def build(self):
        global controller
        Config.set('graphics', 'width', '600')
        Config.set('graphics', 'height', '800')
        Config.write()
        Builder.load_file('./general.kv')
        return MainUI()

    def on_start(self):
        global controller, current_event
        pop = LoadFilePopup(auto_dismiss=False)
        pop.open()
        Window.enabled = False
        thr = threading.Thread(target=controller.load_file)
        thr.start()
        current_event = Clock.schedule_interval(partial(pop.check_controller_state, thr), 1 / 10.)

    # def teste(self, instance, width, height):
    #     print("Width: {}. Height: {}".format(width, height))


def start(args):
    global controller
    if len(args) < 1:
        print(
            """Parameter file wasn't loaded! Either drag the file on top of the program 
            or use an argument in a command line"""
            )
        os.system("pause")
        return
    controller = Controller(args[1])
    DoppelApp().run()


start(sys.argv)