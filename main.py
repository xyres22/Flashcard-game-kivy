from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager,NoTransition
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
import random
import json
from datetime import datetime
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.button.button import MDFillRoundFlatButton,MDFlatButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from plyer import tts
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout

Window.size = (300,550)
Builder.load_file('design.kv')

class WelcomeScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(self.msg,10)

    def msg(self,dt):
        self.manager.current = 'login_screen'

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current='sign_up'

    def clear(self):
        self.ids.username.text = ''
        self.ids.password.text = ''
        self.ids.username.error = False
        self.ids.password.error = False


    def log_in(self,uname,pword):
        with open('user.json',encoding='utf8') as file:
            users = json.load(file)
            if uname not in users:
                self.ids.username.error = True
                self.ids.username.helper_text = 'No acoount with that username!'
                self.ids.password.text = ''
            if uname in users and users[uname]['password'] != pword:
                self.ids.password.text = ''     
                self.ids.password.error = True           
                self.ids.password.helper_text = 'Wrong password'
            if uname in users and users[uname]['password'] == pword:
                self.manager.current='login_succesfull'
               
    def get_pw(self):
        self.manager.current='forgot_password'
        
                    
class SignUpScreen(Screen):
 
    def submit(self,uname,pword):
        min_length = 5
        max_length = 20
        with open('user.json',encoding='utf8') as file:
            users = json.load(file)
            if uname in users:
                self.ids.username.error = True
                self.ids.username.helper_text = 'User is already taken'
            elif min_length>len(uname):
                self.ids.username.error = True
                self.ids.username.helper_text = 'User is too short'
            elif len(uname)>max_length:
                self.ids.username.error = True
                self.ids.username.helper_text = 'User is too long'
            elif min_length>len(pword):
                self.ids.password.error = True
                self.ids.password.helper_text = 'Password is too short'
            elif len(pword)>max_length:
                self.ids.password.error = True
                self.ids.password.helper_text = 'Password is too long'
            else:
                users[uname] = {'username':uname, 'password':pword,
                            'created': datetime.now().strftime('%d/%m/%Y  %H:%M:%S')}
            
                with open('user.json', 'w',encoding='utf8') as file:
                    json.dump(users,file)
                show_popup('Notification', ' You registered succesfully.')
                self.manager.current='login_screen'
            
                with open('data.json',encoding='utf8') as file:
                    words = json.load(file)
                    name = self.ids.username.text
                    words[name] = {}
                with open('data.json','w',encoding='utf8') as file:
                    json.dump(words,file)
                self.ids.username.error = False
                self.ids.password.error = False

class ForgotPassword(Screen):
    def forgot(self,uname):
        self.ids.password.text = ""
        with open('user.json',encoding='utf8') as file:
            users = json.load(file)
            if uname in users:
                self.ids.password.text = f'Your password is: {users[uname]["password"]}'
            if uname not in users:
                self.ids.username.error = True
                self.ids.username.helper_text = 'Invalid username'


    def home(self):
        self.manager.current='login_screen'
        self.ids.username.text = ''
        self.ids.password.text = ''


class CardGame(Screen):
    result = []
    ind_ex = 0

    def cards(self):
        self.ind_ex = 0
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            self.result = [key for key in words[user][name].items()]
            random.shuffle(self.result)
            self.ids.word.text = self.result[0][0]
        if self.ind_ex == (len(self.result) -1):
            self.ids.next.disabled=True
        else:
            self.ids.next.disabled=False
        self.ids.previous.disabled=True
        

    def back(self):
        self.manager.current='before_game'

    def change(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            for key in words[user][name]:
                obj = words[user][name]
                if self.ids.word.text == key:
                    self.ids.word.text = obj[key]
                elif self.ids.word.text == obj[key]:
                    self.ids.word.text = key

    def previous(self):
        self.ids.next.disabled=False
        if self.ind_ex == 1:
            self.ind_ex -= 1
            self.ids.word.text = self.result[self.ind_ex][0]
            self.ids.previous.disabled=True 
            self.ids.previous.md_bg_color_disabled='grey'    
        elif self.ind_ex > 1:
            self.ind_ex -= 1
            self.ids.word.text = self.result[self.ind_ex][0]

    def next(self):
        self.ids.previous.disabled=False
        if self.ind_ex == (len(self.result) -2):
            self.ind_ex += 1
            self.ids.word.text = self.result[self.ind_ex][0]
            self.ids.next.disabled=True
            self.ids.next.md_bg_color_disabled='grey'
        elif self.ind_ex < (len(self.result) -2):
            self.ind_ex += 1
            self.ids.word.text = self.result[self.ind_ex][0]


class LoginSuccesfull(Screen):

    def home(self):
        self.manager.current='login_screen'
    def game(self):
        self.manager.current='before_game'
    
    def n_word(self):
        self.manager.current='new_word'
    
    def edit(self):
        self.manager.current = 'edit_folder'

class BeforeGame(Screen):

    def all(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            if self.ids.spinner.text == 'Folder':
                show_popup('Warning! File not found','Choose folder.')
            elif words[user][name] == {}:
                show_popup('Warning!','Your folder is empty.')
            else:
                self.manager.current='card_game'
        
    def menu_open(self):
        user = self.manager.get_screen('login_screen').ids.username.text
        with open('data.json') as file:
            words = json.load(file)
            self.list = [i for i in words[user]]
        menu_items = [
            {
                "viewclass":"OneLineListItem",
                "text": i,
                "on_release": lambda x= i: self.menu_callback(x,menu),
            } for i in self.list
        ]
        menu = MDDropdownMenu(
            caller=self.ids.spinner, items=menu_items,
            border_margin = 24, position ='center',
            max_height = 240,width_mult= 4
        )
        menu.open()

    def menu_callback(self, text_item,menu):
        self.ids.spinner.text = text_item
        menu.dismiss()


    def clear_spinner(self):
        self.ids.spinner.text='Folder'
    
    def home(self):
        self.manager.current = 'login_succesfull'

    def one_try(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            if self.ids.spinner.text == 'Folder':
                show_popup('Warning! File not found','Choose folder.')
            elif words[user][name] == {}:
                show_popup('Warning!','Your folder is empty.')
            else:
                self.manager.current = 'one_try_game'
        
    def write_game(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            if self.ids.spinner.text == 'Folder':
                show_popup('Warning! File not found','Choose folder.')
            elif words[user][name] == {}:
                show_popup('Warning!','Your folder is empty.')
            else:
                self.manager.current='second_game'
    
    def voice_game(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            if self.ids.spinner.text == 'Folder':
                show_popup('Warning! File not found','Choose folder.')
            elif words[user][name] == {}:
                show_popup('Warning!','Your folder is empty.')
            else:
                self.manager.current = 'voice_game'

class OneTryGame(Screen):
    result= []
    correct = 0
    wrong = 0
    def back(self):
        self.manager.current='before_game'

    def submit(self,info):
        current = self.ids.progress.value
        try:
            if info.lower() != (self.result[0][1]).lower():
                self.wrong += 1
            elif info.lower == self.result[0][1].lower():
                self.correct += 1   
            self.ids.input.text = ''
            del self.result[0]
            current += 1
            self.ids.progress.value = current
            self.ids.key.text = self.result[0][0]
        except IndexError:
            self.manager.current ='win_second'
            self.manager.get_screen('win_second').ids.correct.text = str(self.correct)
            self.manager.get_screen('win_second').ids.wrong.text = str(self.wrong)
            self.ids.progress.value = 0
        
    def validation(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            self.result = [key for key in words[user][name].items()]
            self.ids.progress.max = len(self.result)
            random.shuffle(self.result)
            self.ids.key.text = self.result[0][0]

    def clear_page(self, *args):
        self.ids.key.text = ''
        self.ids.input.text = ''
        self.results = []
        self.ids.progress.value = 0
        self.ids.progress.max = 0


class SecondGame(Screen):
    result= []

    def back(self):
        self.manager.current='before_game'

    def submit(self,info):
        current = self.ids.progress.value
        try:
            if info.lower() != self.result[0][1].lower():
                self.ids.input.error = True
                self.ids.input.helper_text="Wrong answer"
            elif info.lower() == self.result[0][1].lower():
                self.ids.input.error = False
                self.ids.input.text = ''
                del self.result[0]
                current += 1
                self.ids.progress.value = current
                self.ids.key.text = self.result[0][0]
        except IndexError:
            self.manager.current ='win_window'
            self.ids.progress.value = 0

        
    def validation(self):
        self.ids.progress.value = 0
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            self.result = [key for key in words[user][name].items()]
            self.ids.progress.max = len(self.result)
            random.shuffle(self.result)
            self.ids.key.text = self.result[0][0]

    def clear_page(self, *args):
        self.ids.key.text = ''
        self.ids.input.text = ''
        self.results = []
        self.ids.progress.value = 0

class VoiceGame(Screen):
    result= []

    def back(self):
        self.manager.current='before_game'

    def submit(self,info):
        current = self.ids.progress.value
        try:
            if info.lower() != self.result[0][1].lower():
                self.ids.input.error = True
                self.ids.input.helper_text="Wrong answer"
            elif info.lower() == self.result[0][1].lower():
                self.ids.input.error = False
                self.ids.input.text = ''
                del self.result[0]
                current += 1
                self.ids.progress.value = current
                self.tts = self.result[0][1]
        except IndexError:
            self.manager.current ='win_window'
            self.ids.progress.value = 0
    def voice(self):
        try:
            tts.speak(self.tts)
        except NotImplementedError:
            toast('Error!', duration = 1)
        
    def validation(self):
        self.ids.progress.value = 0
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = self.manager.get_screen('login_screen').ids.username.text
            name = self.manager.get_screen('before_game').ids.spinner.text
            self.result = [key for key in words[user][name].items()]
            self.ids.progress.max = len(self.result)
            random.shuffle(self.result)
            self.tts = self.result[0][1]

    def clear_page(self, *args):
        self.ids.input.text = ''
        self.results = []
        self.ids.progress.value = 0


class NewWord(Screen):
    def menu_open(self):
        user = self.manager.get_screen('login_screen').ids.username.text
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            self.list = [i for i in words[user]]
        menu_items = [
            {
                "viewclass":"OneLineListItem",
                "text": i,
                "on_release": lambda x= i: self.menu_callback(x,menu),
            } for i in self.list
        ]
        menu = MDDropdownMenu(
            caller=self.ids.spinner, items=menu_items,
            border_margin = 24, position ='center',
            max_height = 240,width_mult = 4
        )
        menu.open()

    def menu_callback(self, text_item,menu):
        self.ids.spinner.text = text_item
        menu.dismiss()

    def start(self):
        self.ids.spinner.text = 'Folder'
        self.ids.word.text = ''
        self.ids.translation.text = ''
    
    def saving(self,folder,word,trans):
        user = self.manager.get_screen('login_screen').ids.username.text
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            if folder == 'Folder':
                toast(text ='Choose folder', duration =1)
            elif word == '' or trans == '':
                self.ids.translation.helper_text = 'Required'
                self.ids.translation.error = True
                self.ids.word.helper_text = 'Required'
                self.ids.word.error = True
            else:
                storage = words[user][folder]
                storage[word]= trans
                with open('data.json','w',encoding='utf8') as file:
                    json.dump(words,file)               
                self.ids.word.text = ''
                self.ids.translation.text = ''
                toast('Added')
                self.ids.translation.required = False
                self.ids.word.required = False

    def back_after_saving(self):
        self.manager.current = 'login_succesfull'

    def create_folder(self,name):
        if name == '':
            self.ids.folder.error = True
            self.ids.folder.helper_text = 'Required'
        else:
            user = self.manager.get_screen('login_screen').ids.username.text
            with open('data.json',encoding='utf8') as file:
                words = json.load(file)
                words[user][name] = {}
            with open('data.json','w',encoding='utf8') as file:
                json.dump(words,file)
            self.ids.folder.text = ''
            list = [i for i in words[user]]
            self.ids.spinner.values = list
            toast('Created')

class Content(MDFloatLayout):
    dialog = None
    text1 = StringProperty(None)
    text2 = StringProperty(None)

    def delete(self,obj):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = app.root.get_screen('login_screen').ids.username.text 
            self.folder = app.root.get_screen('edit_words').ids.topbarname.title
            del_word = self.ids.word1.hint_text
            del words[user][self.folder][del_word]
            with open('data.json','w',encoding='utf8') as file:
                json.dump(words,file)
        self.dialog.dismiss()
        app.root.get_screen('edit_words').ids.words.clear_widgets()
        with open('data.json',encoding='utf8') as file:
            self.result = [key for key in words[user][self.folder].items()]
            for i in self.result:
                app.root.get_screen('edit_words').ids.words.add_widget(
                    MDExpansionPanel(
                        icon='translate',
                        content=Content(text1 =i[0] ,text2 =i[1] ),
                        panel_cls=MDExpansionPanelTwoLine(
                            text=i[0],
                            secondary_text=i[1],
                        )
                    )
                ) 
        #self.dialog.dismiss()
        toast('Deleted')

    def alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Delete word?",
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.close
                    ),
                    MDFlatButton(
                        text="Delete",
                        on_release = self.delete
                    ),
                ],
            )
        self.dialog.open()

    def close(self,obj):
        self.dialog.dismiss()

    def update_word(self,old_word1,new_word1,old_word2,new_word2):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = app.root.get_screen('login_screen').ids.username.text
            folder = app.root.get_screen('edit_words').ids.topbarname.title
            words[user][folder] = {(new_word1 if k==old_word1 else k):(new_word2 if k ==old_word1 and v==old_word2 else v) for k, v in words[user][folder].items()}
        with open('data.json','w',encoding='utf8') as file:
            json.dump(words,file)
        app.root.get_screen('edit_words').ids.words.clear_widgets()
        with open('data.json',encoding='utf8') as file:
            self.result = [key for key in words[user][folder].items()]
            for i in self.result:
                app.root.get_screen('edit_words').ids.words.add_widget(
                    MDExpansionPanel(
                        icon='translate',
                        content=Content(text1 =i[0] ,text2 =i[1] ),
                        panel_cls=MDExpansionPanelTwoLine(
                            text=i[0],
                            secondary_text=i[1],
                        )
                    )
                ) 
        toast('Updated')

class Cardy(MDCard):
    card_name = StringProperty('')

    def word_list(self):
        app.root.get_screen('edit_words').ids.topbarname.title = self.ids.name.text
        app.root.current= 'edit_words'


class EditWords(Screen):
    dialog = None

    def on_pre_enter(self):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = app.root.get_screen('login_screen').ids.username.text
            self.result = [key for key in words[user][self.ids.topbarname.title].items()]
            for i in self.result:
                app.root.get_screen('edit_words').ids.words.add_widget(
                    MDExpansionPanel(
                        icon='translate',
                        content=Content(text1 =i[0] ,text2 =i[1] ),
                        panel_cls=MDExpansionPanelTwoLine(
                            text=i[0],
                            secondary_text=i[1],
                        )
                    )
                )

    def back(self):
        self.manager.current ='edit_folder'
        self.ids.words.clear_widgets()

    def remove(self,obj):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = app.root.get_screen('login_screen').ids.username.text 
            folder =  self.ids.topbarname.title
            del words[user][folder]   
            with open('data.json','w',encoding='utf8') as file:
                json.dump(words,file)
        self.manager.current = 'edit_folder'  
        self.dialog.dismiss()     
        toast('Deleted')

    def change_name(self,folder):
        show_popup('Update Folder',folder,2)    

    def add_words_pop(self):
        show_popup('Add words!','Enter data',3)

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Delete folder?",
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Delete",
                        on_release = self.remove
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()


class EditFolder(Screen):

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        user = self.manager.get_screen('login_screen').ids.username.text
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            self.list = [i for i in words[user]]
            for i in self.list:
                self.ids.box.add_widget(Cardy(card_name= str(i)))
        
    def back(self):
        self.manager.current ='login_succesfull'
        self.ids.box.clear_widgets()

    def add(self):
        show_popup('Create Folder','Folder name',1)

    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''

        def refresh_callback(interval):
            self.ids.box.clear_widgets()
            self.on_pre_enter()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0
        Clock.schedule_once(refresh_callback, 1)


class WinWindow(Screen):
    def play_again(self):
            self.manager.current = 'second_game'

    def back(self):
        self.manager.current = 'before_game'

class WinSecond(Screen):
    def on_pre_enter(self):
        self.ids.img.anim_delay = 0.05
        self.ids.img.anim_loop = 0
        self.ids.img.source = 'assets/win2.gif'

    def back(self):
        self.manager.current = 'before_game'
        
    def again(self):
        self.manager.current = 'one_try_game'


class CreateFolderPopup(Screen):
    popup = ObjectProperty(None)
    def create_folder(self,name):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = app.root.get_screen('login_screen').ids.username.text
            if name == '':
                self.ids.folder.error = True
                self.ids.folder.helper_text = 'Required'
            elif name in words[user]:
                self.ids.folder.error = True
                self.ids.folder.helper_text = 'Already exist'
            else:
                words[user][name] = {}
                with open('data.json','w',encoding='utf8') as file:
                    json.dump(words,file)
                toast('Created')
                app.root.get_screen('edit_folder').ids.box.add_widget(Cardy(card_name= self.ids.folder.text ))
                self.ids.folder.text = ''
                self.popup.dismiss()

class UpdateFolder(Screen):
    def upd(self,folder,new_name):
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            user = app.root.get_screen('login_screen').ids.username.text
            if new_name in words[user]:
                self.ids.upd.error = True
                self.ids.upd.helper_text = 'Already exist'
            else:
                words[user] = {new_name if k == folder else k:v for k,v in words[user].items()}
                with open('data.json','w',encoding='utf8') as file:
                    json.dump(words,file)
                app.root.get_screen('edit_words').ids.topbarname.title = new_name
                self.ids.upd.text = ''
                self.ids.upd.required = False
                toast('Updated')
                self.popup.dismiss()

class AddWordPopup(Screen):
    def add_new_word(self,word1,word2):
        user = app.root.get_screen('login_screen').ids.username.text
        folder = app.root.get_screen('edit_words').ids.topbarname.title
        with open('data.json',encoding='utf8') as file:
            words = json.load(file)
            if word1 == '' or word2 == '':
                self.ids.trans2.helper_text = 'Required'
                self.ids.trans2.error = True
                self.ids.word2.helper_text = 'Required'
                self.ids.word2.error = True
            elif word1 in words[user][folder]:
                self.ids.word2.helper_text = 'Already exist'
                self.ids.word2.error = True              
            else:
                storage = words[user][folder]
                storage[word1]= word2
                with open('data.json','w',encoding='utf8') as file:
                    json.dump(words,file)               
                self.ids.word2.text = ''
                self.ids.trans2.text = ''
                self.ids.trans2.required = False
                self.ids.word2.required = False
                app.root.get_screen('edit_words').ids.words.add_widget(
                    MDExpansionPanel(
                        icon='translate',
                        content=Content(text1 =word1 ,text2 =word2 ),
                        panel_cls=MDExpansionPanelTwoLine(
                            text=word1,
                            secondary_text=word2,
                        )
                    )
                )
                toast('Added')
                self.popup.dismiss()




class P(Screen):
    popup = ObjectProperty(None)

class ImageButton(ButtonBehavior,Image):
    pass

    
def show_popup(info,text,nr=0):
    # 0 = normal popup
    # 1 = Create folder popup
    # 2 = UpdateFolder
    # 3 = Add Wordpopup
    if nr == 0:
        show = P()
        size = (200,200)
    elif nr == 1:
        show = CreateFolderPopup()
        size = (250,250)
    elif nr == 2:
        show = UpdateFolder()
        size = (250,250)
    elif nr == 3:
        show = AddWordPopup()
        size = (250,250)
    show.ids.pop_label.text = text
    pop = Popup(title=info,title_color =(60/255,60/255,60/255,1),auto_dismiss=True ,content=show, size_hint=(None,None),size=size,background= '',background_color =(240/255,240/255,240/255,1),title_align ='center')
    
    show.popup = pop
    pop.open()

class RootWidget(ScreenManager):
    pass

class MainApp(MDApp):

    def build(self):
        return RootWidget()

if __name__ ==  '__main__':
    app = MainApp()
    app.run()