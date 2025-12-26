#Everything is being made in english to explain the process in a universal language
#TRADUÇÃO: Tudo está sendo feito em inglês para explicar o processo em uma lingua universal

"""
    This project aims on creating a software that's able to manage worker's info
   by first logging in with your manager account. Then, in case if you don't
   have a manager account, you can create one by clicking on "sign up".
    This project only uses the concepts of file management to create the
   manager account and worker's basic info, as well as editing and deleting
   them. This project is NOT related to any database management conception.
"""

#Main Kivy classes imported:

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

#Kivy's Layout classes imported:

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

#Kivy's setting classes imported:

from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

#This will help us manage files
import os

#defines the software's window as borderless
Window.borderless = True

#We define the window color
Window.clearcolor = (0.01, 0.4, 1, 1)

"""
 The idea is having one Manager and Worker class where
the input datas are saved to be quoted later. The other
classes responsible for the interface connects the user 
to the software.
 Not to lose any data when the software is closed, the
files will do their jobs by bringing everything that
has been previously saved.
"""
class Manager:
    def __init__(self, first_m, last_m, password_m):

        self.first_m = first_m
        self.last_m = last_m
        self.full_name_m = "{} {}".format(first_m, last_m)
        self.password_m = password_m

class Worker:
    def __init__(self, first_w, last_w, phone_w, wage_w):
        self.first_w = first_w
        self.last_w = last_w
        self.phone_w = phone_w
        self.wage_w = wage_w
        self.full_name_w = "{} {}".format(first_w, last_w)
        self.email_w = first_w + '.' + last_w + '@company.com'

#a new class is created that inherits from Button class
class HoverButton(Button):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

#the colors of the buttons are set according to whether the mouse is on the button or not
        self.bd_normal = (0.25, 0.25, 0.25, 1)
        self.bd_dark = (0.35, 0.35, 0.35, 1)

#disables the default Kivy button image, so colors can be used instead. Then sets the initial background color
        self.background_normal = ""
        self.background_color = self.bd_normal

#Tells Kivy to call the on_mouse_pos method whenever the mouse moves
        Window.bind(mouse_pos=self.on_mouse_pos)

#on_mouse_pos method
    def on_mouse_pos(self, window, pos):

#checks if thw widget is currently displayed
        if not self.get_root_window():
            return

#inside is True if the mouse is hovering over the button
        inside = self.collide_point(*self.to_widget(*pos))

#if the mouse is over the button, the color of the button changes
        self.background_color = self.bd_dark if inside else self.bd_normal

#this class inherits from BoxLayout, so we can personalize the layout in a more free way
class ManagerMenu(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super(ManagerMenu, self).__init__(**kwargs)

        self.main_app = main_app

#We define the main settings of our tab size and layout orientation
        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

#arranges child widgets in a grid of rows and columns
        form = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None
        )

#whenever minimum height changes, it updates the layout's height automatically
        form.bind(minimum_height=form.setter('height'))

#adds a label with the text 'Full Name'
        form.add_widget(Label(text='Full Name:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))

#defines a text input and prints it in the screen
        self.fullname_m=TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        form.add_widget(self.fullname_m)

#adds a label with the name 'Password'
        form.add_widget(Label(text='Password:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))

#defines the password text input and prints it in the screen
        self.password_m=TextInput(
            multiline=False,
            size_hint_y=None,
            password=True,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        form.add_widget(self.password_m)

#empty label
        self.confirmation_text = Label(text='',
                              font_size='12sp',
                              color=(1, 0, 0, 1),
                              size_hint_y=None,
                              height=30)
        form.add_widget(self.confirmation_text)

#the final command to finally print in the screen everything that was claimed with "form"
        self.add_widget(form)

#positions its child widgets according to anchor points
        anchor = AnchorLayout(
            anchor_x = 'center',
            anchor_y = 'center',
            size_hint_y=None,
            height=70
        )

#arranges its children in a line, either horizontally or vertically
        buttons = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint=(None, None),
            size=(270, 45)
        )

#buttons 'login' and 'sign up' first defined
        self.login = HoverButton(
            text='Login',
            size_hint=(None, None),
            size=(120, 45)
        )
        self.signup = HoverButton(
            text='Sign Up',
            size_hint=(None, None),
            size=(120, 45)
        )

#the buttons 'login' and 'sign up' are added side by side
        buttons.add_widget(self.login)
        buttons.add_widget(self.signup)

#the row of buttons is added to anchor
        anchor.add_widget(buttons)

#prints the buttons in the screen
        self.add_widget(anchor)

#we set the bind so the methods can be called whenever we press the buttons
        self.login.bind(on_press=self.on_login)
        self.signup.bind(on_press=self.on_signup)

#these methods help us change the window according to the button we click
    def on_login(self, instance):

#the text inputs become variables
        full_name_m = self.fullname_m.text
        password_m = self.password_m.text

#if the user leaves one of both text inputs empty, the software tells him to type his info first
        if not full_name_m or not password_m:
            self.confirmation_text.text = "Please enter your full name and password"
            return

#the title of the file is the full name
        account_m = f"manager account/{full_name_m}.txt"

#checks if the file exists. In case it doesn't, it tells the user that the Manager's name is not signed up
        if os.path.exists(account_m):
            with open(account_m, 'r') as file:
                saved_password = file.read().strip()
        else:
            self.confirmation_text.text = "Manager's name doesn't exist."
            return

#if the Manager's name is signed up and the password is correct, the software opens another tab
        if password_m == saved_password:
            self.main_app.switch_to_login()
        else:
            self.confirmation_text.text = "Password is not correct."

#this method opens the signup tab if the user clicks on the signup button
    def on_signup(self, instance):
        self.main_app.switch_to_signup()



"""
 The SignUp class is responsible for the Manager's account creation
For that, the buttons will have methods that are called by the 'bind' function.
The methods will have the functions that the buttons are responsible for executing.
"""

class SignUp(BoxLayout):

    def __init__(self, main_app, **kwargs):
        super(SignUp, self).__init__(**kwargs)
        self.main_app = main_app

#these are the main settings of the layout
        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

#'form' creates a layout with 2 columns and a spacing of 2 pixels between the widgets
#the size_hint_y=None let us control the vertical space manually
        form = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None
        )

#always the minimum height changes, it updates the real height to its value
        form.bind(minimum_height=form.setter('height'))

#here we define the textinput's and labels
        form.add_widget(Label(text='First Name:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))
        self.firstname_m=TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            input_filter=self.only_letters,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        form.add_widget(self.firstname_m)
        form.add_widget(Label(text='Last Name:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))
        self.lastname_m=TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            input_filter=self.only_letters,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        form.add_widget(self.lastname_m)
        form.add_widget(Label(text='Password:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))

        self.password_m=TextInput(
            multiline=False,
            size_hint_y=None,
            password=True,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        form.add_widget(self.password_m)
        self.confirmation_text = Label(text='',
                                       font_size='12sp',
                                       color = (1, 0, 0, 1),
                                       size_hint_y=None,
                                       height=30
                                       )
        form.add_widget(self.confirmation_text)

#it prints the widgets made with the 'form'
        self.add_widget(form)

#the anchorlayout positions the children widgets in a specific point of the layout
        anchor = AnchorLayout(
            anchor_x = 'center',
            anchor_y = 'center',
            size_hint_y=None,
            height=70
        )

#it makes the buttons be positioned side by side
        buttons = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint=(None, None),
            size=(270, 45)
        )
#the HoverButton helps customise the Button visual effect
        self.submit = HoverButton(
            text='Submit',
            size_hint=(None, None),
            size=(120, 45)
        )
        self.back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45)
        )

#these print the buttons
        buttons.add_widget(self.submit)
        buttons.add_widget(self.back)
        anchor.add_widget(buttons)
        self.add_widget(anchor)

#the bind function calls the method according to the button you click
        self.submit.bind(on_press=self.on_submit)
        self.back.bind(on_press=self.on_back)

#this method is called whenever you click on the SignUp button
    def on_submit(self, instance):

#variables defined. All of them get the texts input by the user
        first_name_m = self.firstname_m.text
        last_name_m = self.lastname_m.text
        password_m = self.password_m.text

#these functions make the software not accept the inputs in cases when the requirements are not met
        if not first_name_m or not last_name_m or not password_m:
            self.confirmation_text.text = "All fields are required"
            return
        if len(password_m) < 4:
           self.confirmation_text.text = "Password must have at least 4 characters"
           return
        if len(password_m) > 8:
           self.confirmation_text.text = "Password can't have more than 8 characters"
           return
        if not any(c.isupper() for c in password_m):
            self.confirmation_text.text = "Password must contain at least one uppercase character"
            return
        if not any(c.islower() for c in password_m):
            self.confirmation_text.text = "Password must contain at least one lowercase character"
            return
        if not any(c.isdigit() for c in password_m):
            self.confirmation_text.text = "Password must contain at least one number character"
            return

#saves all datas in the Manager class
        manager = Manager(first_name_m, last_name_m, password_m)

#creates a path
        if not os.path.exists('manager account'):
            os.mkdir('manager account')

#creates the title and content based on the full name and password
        full_name_m = manager.first_m + ' ' + manager.last_m
        password_m = manager.password_m
        account_m = f"manager account/{full_name_m}.txt"

#defines a function to create only a title that still doesn't exist
        if os.path.exists(account_m):
            self.confirmation_text.text = "Account already exists"
            return

#finally the account is created
        with open(account_m, 'w') as file:
            file.write(password_m)
            self.confirmation_text.text = "Account created"

#witchs the screen back to the Manager Menu
    def on_back(self, instance):
        self.main_app.switch_to_managermenu()

#this is a function that only allows letters to be typed for first and last name
    def only_letters(self, substring, from_undo):
        return ''.join(char for char in substring if char.isalpha())

#the LogIn class is the class where the menu with all options is located
class LogIn(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super(LogIn, self).__init__(**kwargs)

# We define the main settings of our tab size and layout orientation
        self.main_app = main_app
        Window.size = (400, 200)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

#variables anchor and buttons define how the buttons are going to be gathered
        anchor = AnchorLayout(
            anchor_x = 'center',
            anchor_y = 'center',
            size_hint_y=None,
            height = 30,
            width = 200
        )
        buttons = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None
        )
        buttons.bind(minimum_height=buttons.setter('height'))

#here we define all the buttons
        self.Register = HoverButton(
            text='Register Worker',
            size_hint=(None, None),
            size=(120, 45)
        )
        self.Check = HoverButton(
            text='Check Worker',
            size_hint=(None, None),
            size=(120, 45)
        )
        self.Check_list = HoverButton(
            text='Check List',
            size_hint=(None, None),
            size=(120, 45)
        )
        self.Edit = HoverButton(
            text='Edit Info',
            size_hint=(None, None),
            size=(120, 45))
        self.Back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45))
        self.Delete = HoverButton(
            text='Delete Worker',
            size_hint=(None, None),
            size=(120, 45))

#here is the chain of buttons, how they are going to be placed and printed on the screen
        buttons.add_widget(self.Register)
        buttons.add_widget(self.Check)
        buttons.add_widget(self.Check_list)
        buttons.add_widget(self.Edit)
        buttons.add_widget(self.Back)
        buttons.add_widget(self.Delete)

        anchor.add_widget(buttons)
        self.add_widget(anchor)

#the bind function calls the method according to the button
        self.Register.bind(on_press=self.on_register)
        self.Check.bind(on_press=self.on_check)
        self.Check_list.bind(on_press=self.on_check_list)
        self.Edit.bind(on_press=self.on_edit)
        self.Back.bind(on_press=self.on_back)
        self.Delete.bind(on_press=self.on_delete)

#the methods change the screen according to the button you click on
    def on_register(self, instance):
        self.main_app.switch_to_registerworker()
    def on_check(self, instance):
        self.main_app.switch_to_checkworker()
    def on_check_list(self, instance):
        self.main_app.switch_to_checklist()
    def on_edit(self, instance):
        self.main_app.switch_to_editworker()
    def on_delete(self, instance):
        self.main_app.switch_to_deleteworker()
    def on_back(self, instance):
        self.main_app.switch_to_managermenu()
    def on_delete(self, instance):
        self.main_app.switch_to_deleteworker()

#the RegisterWorker class lets the user add worker info to the file
class RegisterWorker(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super(RegisterWorker, self).__init__(**kwargs)
        self.main_app = main_app

#general layout settings
        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

#this form gridlayout helps organize the widgets for the texts and labels that are going to be added
        form = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None
        )
        form.bind(minimum_height=form.setter('height'))
        form.add_widget(Label(text='Register a New Worker',
                              color = 'yellow',
                              font_size='14sp',
                              size_hint_y=None,
                              height=30))
        form.add_widget(Label(text='',
                              font_size='14sp',
                              size_hint_y=None,
                              height=30))
        form.add_widget(Label(text='First Name',
                              font_size='17sp',
                              size_hint_y=None,
                              height=30))
        self.first_name_w = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            input_filter=self.only_letters,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.first_name_w)
        form.add_widget(Label(text='Last Name',
                              font_size='17sp',
                              size_hint_y=None,
                              height=30))
        self.last_name_w = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            input_filter=self.only_letters,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.last_name_w)
        form.add_widget(Label(text='Phone Number',
                              font_size='17sp',
                              size_hint_y=None,
                              height=30))
        self.phone_number = TextInput(
            multiline=False,
            size_hint_y=None,
            input_filter='int',
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.phone_number)
        form.add_widget(Label(text='Wage',
                              font_size='17sp',
                              size_hint_y=None,
                              height=30))
        self.wage = TextInput(
            multiline=False,
            size_hint_y=None,
            input_filter='int',
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.wage)
        self.confirmation_text = Label(text='',
                                       font_size='12sp',
                                       color=(1, 0, 0, 1),
                                       size_hint_y=None,
                                       height=30)
        form.add_widget(self.confirmation_text)
        self.add_widget(form)

#the anchor and buttons organize the button layout
        anchor = AnchorLayout(
            anchor_x = 'center',
            anchor_y = 'center',
            size_hint_y=None,
            height = 1,
        )
        buttons = GridLayout(
            cols=2,
            spacing=20,
            size_hint_y=None
        )
        buttons.bind(minimum_height=buttons.setter('height'))

#the buttons save and back
        self.Save = HoverButton(
            text='Save',
            size_hint=(None, None),
            size=(120, 45))
        self.Back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45))

#here we add both buttons in chains so we can finally print them
        buttons.add_widget(self.Save)
        buttons.add_widget(self.Back)
        anchor.add_widget(buttons)
        self.add_widget(anchor)

#the bind function calls the method according to the button you click
        self.Save.bind(on_press=self.on_save)
        self.Back.bind(on_press=self.on_back)

#the on_save method is going to be actioned whenever the save button is pressed
    def on_save(self, instance):

#the text inputs become method variables here
        first_name_w = self.first_name_w.text
        last_name_w = self.last_name_w.text
        full_name_w = first_name_w + ' ' + last_name_w
        email = first_name_w + '.' + last_name_w + '@company.com'
        phone_number = self.phone_number.text
        wage = self.wage.text

#if the full name typed by the user doesn't match any worker previously registered, the software returns a message
        if not first_name_w or not last_name_w or not phone_number or not wage:
            self.confirmation_text.text = "All fields are required"
            return

#this saves the input data in Worker class
        worker = Worker(first_name_w, last_name_w, phone_number, wage)

#the worker data file is created
        if not os.path.exists('worker data'):
            os.mkdir('worker data')

#the title and content variables are created, and the title is saved in the new file
        worker_title = full_name_w
        worker_data = worker.first_w + '\n' + worker.last_w + '\n' + worker.phone_w + '\n' + worker.wage_w + '\n' + email
        worker_file = f"worker data/{worker_title}.txt"

#if the worker was previously signed in the system the software won't let you sign him up again
        if os.path.exists(worker_file):
            self.confirmation_text.text = "Worker already signed"
            return

#the content is saved under the title
        with open(worker_file, 'w') as file:
            file.write(worker_data)
            self.confirmation_text.text = "Worker saved"

# the on_back method is going to be actioned whenever the back button is pressed
    def on_back(self, instance):
        self.main_app.switch_to_login()

#this is a function that only allows letters to be typed for first and last name
    def only_letters(self, substring, from_undo):
        return ''.join(char for char in substring if char.isalpha())

#CheckWorker class created and the same structures are developed.
#from now one, only the specific button methods are going to be explained, as the layout is basically the same in every case
class CheckWorker(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super(CheckWorker, self).__init__(**kwargs)
        self.main_app = main_app
        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.form = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None
        )
        self.form.bind(minimum_height=self.form.setter('height'))
        self.form.add_widget(Label(text='Check Worker Info',
                              color='yellow',
                              font_size='14sp',
                              size_hint_y=None,
                              height=30))
        self.form.add_widget(Label(text='',
                              font_size='14sp',
                              size_hint_y=None,
                              height=30))
        self.form.add_widget(Label(text="Worker's Full Name",
                              font_size='17sp',
                              size_hint_y=None,
                              height=30))

        self.full_name_w = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        self.form.add_widget(self.full_name_w)
        self.confirmation_text = Label(text='',
                                       font_size='12sp',
                                       color=(1, 0, 0, 1),
                                       size_hint_y=None,
                                       height=30)
        self.form.add_widget(self.confirmation_text)
        self.add_widget(self.form)
        anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=None,
            height=1,
        )
        buttons = GridLayout(
            cols=2,
            spacing=20,
            size_hint_y=None
        )
        buttons.bind(minimum_height=buttons.setter('height'))
        self.Check = HoverButton(
            text='Check',
            size_hint=(None, None),
            size=(120, 45))
        self.Back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45))
        buttons.add_widget(self.Check)
        buttons.add_widget(self.Back)
        anchor.add_widget(buttons)
        self.add_widget(anchor)
        self.Check.bind(on_press=self.on_check)
        self.Back.bind(on_press=self.on_back)

#on_back method makes the user go back to the options screen
    def on_back(self, instance):
        self.main_app.switch_to_login()

#this method is connected to the next "back" button that appears after you check the Worker's info
    def back_to_checkworker(self, instance):
        self.main_app.switch_to_checkworker()

#on_check method guides you to the screen where the Worker's info is shown once you typed the right Worker's full name
    def on_check(self, instance):
        full_name_w = self.full_name_w.text
        worker_file = f"worker data/{full_name_w}.txt"
        if os.path.exists(worker_file):
            with open(worker_file, 'r') as file:
                lines=file.read().split("\n")
                first = lines[0]
                last = lines[1]
                phone_number = lines[2]
                wage = lines[3]
                email = lines[4]

                self.clear_widgets()
                self.add_widget(Label(text='First Name:'+' '+first
                                      + '\nLast Name:'+' '+last
                                      + '\nPhone Number:'+' '+phone_number
                                      + '\nWage:'+' '+wage
                                      + '\nEmail:'+' '+email))
                anchor = AnchorLayout(
                    anchor_x='center',
                    anchor_y='center',
                    size_hint_y=None,
                    height=1,
                )
                buttons = GridLayout(
                    cols=2,
                    spacing=20,
                    size_hint_y=None
                )
                buttons.bind(minimum_height=buttons.setter('height'))

                self.Back = HoverButton(
                    text='Back',
                    size_hint=(None, None),
                    size=(120, 45))
                buttons.add_widget(self.Back)
                anchor.add_widget(buttons)
                self.add_widget(anchor)
                self.Back.bind(on_press=self.back_to_checkworker)
        else:
            self.confirmation_text.text = "Worker not signed"

#the checklist class allows you to check the list of all workers of the company
class CheckList(BoxLayout):
    def __init__(self, main_app,**kwargs):
        super(CheckList, self).__init__(**kwargs)

        self.main_app = main_app

        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        title = Label(
            text='Workers Check List',
            font_size='18sp',
            color='yellow',
            size_hint_y=None,
            height=30
        )
        self.add_widget(title)

#scroll is what we're going to use to scroll down and up the list
        scroll = ScrollView(
            size_hint=(1, 1)
        )
        self.output=Label(
            text = '',
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.output.bind(
            texture_size=lambda *_: setattr(self.output, 'height', self.output.texture_size[1])
        )
        scroll.add_widget(self.output)
        self.add_widget(scroll)
        self.load_workers()

        self.back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45)
        )
        self.back.bind(on_press=self.on_back)
        self.add_widget(self.back)

#the lead_workers method brings the list of worker files
    def load_workers(self):

        folder = 'worker data'

#if the file doesn't exist, the software will return a text print saying it
        if not os.path.exists(folder):
            self.output.text='No workers registered.'
            return
        files = os.listdir(folder)
        if not files:
            self.output.text = 'No workers registered.'
            return
        text = ''

        for filename in files:
            path = os.path.join(folder, filename)

            with open(path, 'r') as file:
                lines = file.read().split("\n")

            if len(lines) < 5:
                continue

            first=lines[0]
            last=lines[1]
            phone_number = lines[2]
            wage = lines[3]
            email = lines[4]

            text += (
                    f'Name: {first} {last}\n'
                    f'Phone Number: {phone_number}\n'
                    f'Wage: {wage}\n'
                    f'Email: {email}\n'
                    f'-------------------------\n'
                )
        self.output.text = text

    def on_back(self, instance):
        self.main_app.switch_to_login()

"""
 The EditWorker class is actioned by the Edit Worker button.
It asks for the Worker's full name, and then it gives you the
text inputs with the data already there, so you can do your changes
according to what specifically you want to change.
"""
class EditWorker(BoxLayout):
    def __init__(self, main_app,**kwargs):
        super(EditWorker, self).__init__(**kwargs)
        self.main_app = main_app
        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        form = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        form.add_widget(Label(text='Full Name:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))
        self.fullname_w = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.fullname_w)
        self.confirmation_text=Label(text='',
                                       font_size='12sp',
                                       color=(1, 0, 0, 1),
                                       size_hint_y=None,
                                       height=30)
        form.add_widget(self.confirmation_text)
        self.add_widget(form)

        anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=None,
            height=70)
        buttons = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint=(None, None),
            size=(270, 45))
        self.edit = HoverButton(
            text='Edit',
            size_hint=(None, None),
            size=(120, 45))
        self.back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45))
        buttons.add_widget(self.edit)
        buttons.add_widget(self.back)
        anchor.add_widget(buttons)
        self.add_widget(anchor)

        self.back.bind(on_press=self.on_back)
        self.edit.bind(on_press=self.on_edit)

    def on_back(self, instance):
        self.main_app.switch_to_login()
    def on_edit(self, instance):
        fullname_w = self.fullname_w.text
        self.original_title = self.fullname_w.text
        worker_file = f"worker data/{fullname_w}.txt"
        if not os.path.exists(worker_file):
            self.confirmation_text.text = 'No workers found'
            return
        with open(worker_file, 'r') as file:
            lines = file.read().split("\n")
        first = lines[0]
        last = lines[1]
        phone_number = lines[2]
        wage = lines[3]

        self.clear_widgets()

        form = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        form.add_widget(Label(text = 'First Name:'))
        self.first_input=TextInput(
            text=first,
            input_filter = self.only_letters,
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.first_input)

        form.add_widget(Label(text = 'Last Name:'))
        self.last_input=TextInput(
            text=last,
            multiline=False,
            input_filter = self.only_letters,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.last_input)

        form.add_widget(Label(text = 'Phone Number:'))
        self.phone_input=TextInput(
            text=phone_number,
            input_filter = 'int',
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.phone_input)

        form.add_widget(Label(text = 'Wage:'))
        self.wage_input=TextInput(
            text=wage,
            input_filter = 'int',
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.wage_input)
        self.confirmation_text = Label(text='',
                                       font_size='12sp',
                                       color=(1, 0, 0, 1),
                                       size_hint_y=None,
                                       height=30)
        form.add_widget(self.confirmation_text)

        self.add_widget(form)
        anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=None,
            height=10)
        buttons = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint=(None, None),
            size=(270, 45))
        self.save = HoverButton(
            text='Save',
            size_hint=(None, None),
            size=(120, 45))
        self.back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45))
        buttons.add_widget(self.save)
        buttons.add_widget(self.back)
        anchor.add_widget(buttons)
        self.add_widget(anchor)
        self.back.bind(on_press=self.on_back_2)
        self.save.bind(on_press=self.on_save)
    def on_save(self, instance):
        new_first=self.first_input.text
        new_last=self.last_input.text
        new_full = new_first + ' ' + new_last
        new_phone_number=self.phone_input.text
        new_wage=self.wage_input.text
        new_email= new_first + '.' + new_last + '@company.com'

        new_worker=Worker(new_first, new_last, new_phone_number, new_wage)
        old_filename=f"worker data/{self.original_title}.txt"
        new_filename = f"worker data/{new_full}.txt"
        new_content = (
           new_worker.first_w + '\n' +
           new_worker.last_w + '\n' +
           new_worker.phone_w + '\n' +
           new_worker.wage_w  + '\n' +
           new_email
        )

        if old_filename != new_filename and os.path.exists(old_filename):
            os.remove(old_filename)

        with open(new_filename, 'w') as file:
            file.write(new_content)
        self.confirmation_text.text = "Changes saved"
    def on_back_2(self, instance):
        self.main_app.switch_to_editworker()

        # this is a function that only allows letters to be typed for first and last name
    def only_letters(self, substring, from_undo):
          return ''.join(char for char in substring if char.isalpha())

#this class basically deletes the Worker's data once you type their full name.
class DeleteWorker(BoxLayout):
    def __init__(self, main_app,**kwargs):
        super(DeleteWorker, self).__init__(**kwargs)
        self.main_app = main_app
        Window.size = (600, 300)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        form = GridLayout(
            cols=2,
            spacing=2,
            size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        form.add_widget(Label(text='Full Name:',
                              font_size='18sp',
                              size_hint_y=None,
                              height=30))
        self.fullname_w = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_normal="",
            background_active="",
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1))
        form.add_widget(self.fullname_w)
        self.confirmation_text=Label(text='',
                                       font_size='12sp',
                                       color=(1, 0, 0, 1),
                                       size_hint_y=None,
                                       height=30)
        form.add_widget(self.confirmation_text)
        self.add_widget(form)

        anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=None,
            height=70)
        buttons = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint=(None, None),
            size=(270, 45))
        self.delete = HoverButton(
            text='Delete',
            size_hint=(None, None),
            size=(120, 45))
        self.back = HoverButton(
            text='Back',
            size_hint=(None, None),
            size=(120, 45))
        buttons.add_widget(self.delete)
        buttons.add_widget(self.back)
        anchor.add_widget(buttons)
        self.add_widget(anchor)

        self.back.bind(on_press=self.on_back)
        self.delete.bind(on_press=self.on_delete)
    def on_back(self, instance):
        self.main_app.switch_to_login()
    def on_delete(self, instance):
        filename = self.fullname_w.text

        if not filename:
            self.confirmation_text.text = 'Enter a full name'
            return
        path = f"worker data/{filename}.txt"

        if os.path.exists(path):
            os.remove(path)
            self.confirmation_text.text = 'Worker deleted successfully'
        else:
            self.confirmation_text.text = 'Worker not found'

#the MainApp class defines what classes all buttons are going to move you to
class MainApp(App):
    def build(self):
        return ManagerMenu(self)
    def switch_to_managermenu(self):
        self.root.clear_widgets()
        self.root.add_widget(ManagerMenu(self))
    def switch_to_signup(self):
        self.root.clear_widgets()
        self.root.add_widget(SignUp(self))
    def switch_to_login(self):
        self.root.clear_widgets()
        self.root.add_widget(LogIn(self))
    def switch_to_registerworker(self):
        self.root.clear_widgets()
        self.root.add_widget(RegisterWorker(self))
    def switch_to_checkworker(self):
        self.root.clear_widgets()
        self.root.add_widget(CheckWorker(self))
    def switch_to_checklist(self):
        self.root.clear_widgets()
        self.root.add_widget(CheckList(self))
    def switch_to_editworker(self):
        self.root.clear_widgets()
        self.root.add_widget(EditWorker(self))
    def switch_to_deleteworker(self):
        self.root.clear_widgets()
        self.root.add_widget(DeleteWorker(self))
MainApp().run()