import time

from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem, \
    ILeftBodyTouch
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    def mark(self, check, the_list_item):
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
        else:
            the_list_item.text = str(the_list_item.text.replace('[s]', ''))
            pass

    def delete_item(self, the_list_item):

        self.parent.remove_widget(the_list_item)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

    def add_item(self, text):
        self.root.ids.list.add_widget(ListItemWithCheckbox(text=text + time.strftime("%H:%M:%S", time.localtime())))
        self.root.ids.listinput.text = ""

    def delete_item(self, the_list_item):
        self.root.remove_widget(the_list_item)

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


if __name__ == '__main__':
    MainApp().run()
