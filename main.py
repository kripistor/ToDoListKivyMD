from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem, \
    ILeftBodyTouch
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from sqlalchemy import Table, Column, Integer, String, MetaData

from bd import meta, tasks, engine

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk
    def mark(self, check, the_list_item):
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            text = the_list_item.text.replace('[s]', '')
            text = text.replace('[/s]', '')
            conn = engine.connect()
            conn.execute(tasks.update().where(tasks.c.task == text).values(is_done=True))
            conn.commit()

        else:
            the_list_item.text = str(the_list_item.text.replace('[s]', ''))
            the_list_item.text = str(the_list_item.text.replace('[/s]', ''))
            conn = engine.connect()
            conn.execute(tasks.update().where(tasks.c.task == the_list_item.text).values(is_done=False))
            conn.commit()

    def delete_item(self, the_list_item):

        self.parent.remove_widget(the_list_item)
        conn = engine.connect()
        conn.execute(tasks.delete().where(tasks.c.task == the_list_item.text))
        conn.commit()

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
    def on_start(self):
        conn = engine.connect()
        completed = conn.execute(tasks.select().where(tasks.c.is_done == True))
        un_completed = conn.execute(tasks.select().where(tasks.c.is_done == False))
        for row in completed:
            self.root.ids.list.add_widget(ListItemWithCheckbox(pk=True,text = '[s]' + row[0] + '[/s]'))
        for row in un_completed:
            self.root.ids.list.add_widget(ListItemWithCheckbox(pk=False,text=row[0]))


    def add_item(self, text):
        self.root.ids.list.add_widget(ListItemWithCheckbox(text=text))
        self.root.ids.listinput.text = ""
        ins = tasks.insert().values(task=text)
        conn = engine.connect()
        result = conn.execute(ins)
        conn.commit()

    def on_save(self,instance,*args,**kwargs):
        print(args)
        print(kwargs)
        #self.root.ids.list.add_widget(ListItemWithCheckbox(text=str(value)))
        #self.root.ids.listinput.text = ""

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self, text):
        print(text)
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


if __name__ == '__main__':
    MainApp().run()
