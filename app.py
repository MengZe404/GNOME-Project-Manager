from libgpm import MyGPM # This provides all the main functionalities and database access
import password # This provides the functionality to decrypt data from the database

import threading
from sys import argv, exit 
import subprocess # This provides the functionality to open other softwares
import os
import time
import random

# Modules for GUI design
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, Gdk, Notify


# CSS styleshee
CSS = b"""
.myNotebook {
    background-color: #323232;
}

.myNotebook tab {
    color: white;
    font-size: 14px;
    padding-bottom: 0;
    margin: 0
}

.myNotebook tab:checked {
    color: white;
    transition: 400ms ease-in-out;
    background-color: #E95420;
}

.myNotebook tab:hover {
    background-color: #3a3a3a;
}

.myNotebook tab:checked:hover {
    background-color: #F95620;
}

.home{
    background-color: #3a3a3a;
}
"""


app = MyGPM() # Create an object of MyDMS class
unam = '' # A global variable
# Note: the username (GitHub username) is always unique
pword = ''


# Class - Login
# This class creates Login window (Gtk.Window)
# This runs when the user start the app
class Login(Gtk.Window): # Login Window
    def __init__(self):
        # Create window
        Gtk.Window.__init__(self) 
        self.connect("destroy", Gtk.main_quit)
        # Initialise window
        self.set_default_size(360,500) 
        self.set_border_width(5)
        self.set_title("GNOME Project Manager")
        # Create content
        window = self.loginWindow()
        self.add(window) # add content to the window
        self.show_all()

    # Fucntion: create login window
    def loginWindow(self): # Create contents
        self.window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        # Create widgets
        label = Gtk.Label()
        label.set_markup("<span size='xx-large'><b>Login</b></span>")
        label.set_halign(Gtk.Align.CENTER)
        self.window.pack_start(label, True, True, 0)
        # A box that containes the login form
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        form.set_halign(Gtk.Align.CENTER)
        form.set_size_request(250, 300)
        # Child elements of the form - username section
        username = Gtk.Box(spacing=5)

        uname_label = Gtk.Label()
        uname_label.set_markup("<b>Username</b>")
        uname_input = Gtk.Entry()
        uname_input.set_placeholder_text("GitHub Account")

        # For testing ONLY!!!
        uname_input.set_text(argv[1])

        username.pack_start(uname_label, True, True, 0)
        username.pack_start(uname_input, True, True, 0)

        form.pack_start(username, False, True, 0)
        # Child elements of the form - password section
        password = Gtk.Box(spacing=8)

        pword_label = Gtk.Label()
        pword_label.set_markup("<b>Password</b>")
        pword_input = Gtk.Entry()
        pword_input.set_visibility(False)
        pword_input.set_placeholder_text("Password")
        # For testing ONLY!!!
        pword_input.set_text(argv[2])

        password.pack_start(pword_label, True, True, 0)
        password.pack_start(pword_input, True, True, 0)

        form.pack_start(password, False, True, 0)
        # Child elements of the form - Submit button        
        submit = Gtk.Button(label="Login")
        submit.connect("clicked", self.getInfo, uname_input, pword_input)

        form.pack_start(submit, False, True, 5)
        # Child elements of the form - forgot button linked to `self.forgotPW` method
        forgot = Gtk.Button(label="Forgot Password")
        forgot.connect("clicked", self.forgotPW)

        form.pack_end(forgot, False, True, 0)
        # Child elements of the form - register button linked to `self.createAccount` method
        register = Gtk.Button(label="Register")
        register.set_margin_bottom(10)
        register.connect("clicked", self.createAccount)

        form.pack_end(register, False, True, 0)
        # Add form to the main box
        self.window.pack_start(form, True, True, 0)
        return self.window
        

    # Function: get the user input and varify the user account for login
    def getInfo(self, button, uname_input, pword_input):
        global uname
        global pword
        uname = uname_input.get_text()
        pword = pword_input.get_text()
        # If the user input correct username and password
        if(app.varify(uname, pword)):
            self.set_visible(False)
            win = MyWindow()
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
        else:
            # Displat a modal window
            dialog = Gtk.MessageDialog(
                parent = self,
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Wrong username / password! Please try again!",
            )
            dialog.run()
            dialog.destroy()

    # Function: create register window
    def createAccount(self, button):
        self.register = Gtk.Window(title="GNOME Project Manager - Create Account")
        self.register.set_default_size(300, 500)
        # Create form
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        form.set_halign(Gtk.Align.CENTER)
        form.set_size_request(250, 500)
        # Child elements of the form - title
        label = Gtk.Label()
        label.set_markup("<span size='xx-large'>Register</span>")
        label.set_size_request(100, 100)

        form.pack_start(label, False, True, 0)
        # Child elements of the form - username section
        username = Gtk.Box(spacing=5)
        username.set_valign(Gtk.Align.START)

        uname_label = Gtk.Label()
        uname_label.set_markup("<b>Username*</b>")
        uname_input = Gtk.Entry()
        uname_input.set_placeholder_text("GitHub Username")

        username.pack_start(uname_label, True, True, 0)
        username.pack_start(uname_input, True, True, 0)

        form.pack_start(username, False, True, 0)
        # A short label with small font under the uname_input
        note = Gtk.Label()
        note.set_markup("<span size='small'>*Please enter valid GitHub account username*</span>")
        # Add box `username` to the form
        form.pack_start(note, False, True, 0)
        # Child elements of the form - password section
        password1 = Gtk.Box(spacing=8)

        pword_label1 = Gtk.Label()
        pword_label1.set_markup("<b>Password*</b>")
        pword_input1 = Gtk.Entry()
        pword_input1.set_visibility(False)
        pword_input1.set_placeholder_text("Password")

        password1.pack_start(pword_label1, True, True, 0)
        password1.pack_start(pword_input1, True, True, 0)

        password2 = Gtk.Box(spacing=8) # Confirm the password
        pword_input2 = Gtk.Entry()
        pword_input2.set_visibility(False)
        pword_input2.set_placeholder_text("Confirm")

        password2.pack_start(pword_input2, True, True, 0)
        # Add box `password` to the form
        form.pack_start(password1, False, True, 0)
        form.pack_start(password2, False, True, 0)
        # Add a line break to the form
        linebreak = Gtk.Label()
        linebreak.set_text("----------------------------------------------------------------")
        form.pack_start(linebreak, False, True, 0)
        # Other informations: Get the name
        name = Gtk.Box(spacing=8)
        name_label = Gtk.Label()
        name_label.set_markup("<b>Name*</b>")
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Name*")

        name.pack_start(name_label, True, True, 0)
        name.pack_start(name_input, True, True, 0)

        form.pack_start(name, False, True, 0)
        # Get the email
        email = Gtk.Box(spacing=8)
        email_label = Gtk.Label()
        email_label.set_markup("<b>Email*</b>")
        email_input = Gtk.Entry()
        email_input.set_placeholder_text("Email Address")

        email.pack_start(email_label, True, True, 0)
        email.pack_start(email_input, True, True, 0)

        form.pack_start(email, False, True, 0)
        # Get the GitHub URL
        github = Gtk.Box(spacing=8)
        glabel = Gtk.Label()
        glabel.set_markup("<b>URL</b>")
        github_input = Gtk.Entry()
        github_input.set_placeholder_text("GitHub Page URL")

        github.pack_start(glabel, True, True, 0)
        github.pack_start(github_input, True, True, 0)

        form.pack_start(github, False, True, 0)
        # Child element of the form - submit button linked to `self.recordInfo`        
        submit = Gtk.Button(label="Confirm")

        submit.connect("clicked", self.recordInfo, 
            uname_input,
            pword_input1,
            pword_input2,
            name_input,
            email_input,
            github_input
        )

        form.pack_start(submit, False, True, 0)
        # Add the register form to register window
        self.register.add(form)
        # Display the window
        self.register.show_all()

    # Function: Take the user input from register window and record them in `main.db`
    def recordInfo(self, button, uname_input, pword_input1, pword_input2, name_input, email_input, github_input):
        global uname
        global pword

        uname = uname_input.get_text()
        pword1 = pword_input1.get_text()
        pword2 =  pword_input2.get_text()
        name =  name_input.get_text()
        email =  email_input.get_text()
        github =  github_input.get_text()
        # GitHub URL is not required
        if (github == ''):
            github = None
        # Check for the validity of the data
        if(uname == '' or pword1 == '' or name == '' or email == ''):
            dialog = Gtk.MessageDialog(
                parent = self.register,
                flags = 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0
        elif(pword1 != pword2):
            dialog = Gtk.MessageDialog(
                parent = self.register,
                flags = 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Please make sure your password matches!",
            )
            dialog.run()
            dialog.destroy()
            return 0
        elif(len(pword1) <= 6): # Password must be longer than 6 chars (for security)
            dialog = Gtk.MessageDialog(
                parent = self.register,
                flags = 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Your password is too short! (length > 6)",
            )
            dialog.run()
            dialog.destroy()
            return 0
        # Register the account and save the data into `main.db`

        check = app.checkAccount(uname)
        if check == True:
            dialog = Gtk.MessageDialog(
                parent = self.register,
                flags = 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="The user account with this GitHub username is registered!",
            )
            dialog.run()
            dialog.destroy()
            return 0

        app.register(uname, pword1, name, email, github)
        pword = pword1
        try:
            # Note: This requires internet access! An `ApiError` will be raised
            app.addUserData(uname)
            # Get all the public (open source) repo of the user with his/her GitHub account (username)
            app.createRepoDB(uname)
            dialog = Gtk.MessageDialog(
                parent = self.register,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = "Registered! Please enjoy the app!",
            )
        except:
            dialog = Gtk.MessageDialog(
                parent = self.register,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = """
                Registered! Please restart the app!
                Note: Failed loading repo data (this requires Internet access).
                """,
            )
        dialog.run()
        dialog.destroy()
        self.set_visible(False)
        self.register.set_visible(False)
        window = MyWindow()
        window.connect("destroy", Gtk.main_quit)
        window.show_all()

    # Function: Recover the password    
    def forgotPW(self, button):
        # Create window
        self.window = Gtk.Window()
        # Initialise the window
        self.window.set_title("GNOME Project Manager - Forgot Password")
        self.window.set_default_size(350, 250)
        # Create form (vertical box)
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        form.set_halign(Gtk.Align.CENTER)
        form.set_size_request(300, 200)
        # Child element of the form - label
        title = Gtk.Label()
        title.set_markup("<span size='xx-large'>Recover Password</span>")
        title.set_size_request(100, 100)
        form.pack_start(title, False, True, 0)
        # Chile element of the form - username section
        uname_input = Gtk.Box()
        uname_input_label = Gtk.Label(label="Username")
        uname_input_field = Gtk.Entry()
        uname_input_field.set_placeholder_text("GitHub Account")

        uname_input.pack_start(uname_input_label, False, True, 15)
        uname_input.pack_start(uname_input_field, True, True, 0)

        form.pack_start(uname_input, False, True, 0)
        # Child element of the form - email section
        email_input = Gtk.Box()
        email_input_label = Gtk.Label(label="Registerd Email")
        email_input_field = Gtk.Entry()
        email_input_field.set_placeholder_text("Email")

        email_input.pack_start(email_input_label, False, True, 15)
        email_input.pack_start(email_input_field, False, True, 0)

        form.pack_start(email_input, False, True, 0)
        # Child element of the form - sumbit button linked to `selc.recover` method
        submit = Gtk.Button(label="Sumbit")
        submit.connect("clicked", self.recover, email_input_field, uname_input_field)

        form.pack_start(submit, False, True, 20)
        # Add the form to the window and display the window
        self.window.add(form)
        self.window.show_all()

    # Function: Get the user's password with email and username (highly unsecure!)
    def recover(self, button, email_input, uname_input):
        email = email_input.get_text()
        uname = uname_input.get_text()
        # Get the password
        password = app.recoverAccount(email, uname)
        # If there is a password that matches the username and email
        if (password != None):
            dialog = Gtk.MessageDialog(
                    parent = self.window,
                    flags = 0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=f"Your password is: {password}",
            )
        else:
            dialog = Gtk.MessageDialog(
                parent = self.window,
                flags = 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=f"Incorrect email address",
            )
        dialog.run()
        dialog.destroy()
        self.window.destroy()

##########################################################################

# Class - MyWindow
# This class creates Main window (Gtk.Window)
# This window contains all the child elements
class MyWindow(Gtk.Window): # Main app
    def __init__(self):
        varify()
        Gtk.Window.__init__(self)
        self.set_default_size(1100,650)

        # Set stylesheet
        cssprovider = Gtk.CssProvider()
        cssprovider.load_from_data(CSS)
        screen = Gdk.Screen.get_default()
        stylecontext = Gtk.StyleContext()
        stylecontext.add_provider_for_screen(screen, cssprovider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        # Create headbar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = f"GNOME Project Manager - {uname}"
        # Child element of the headbar - about button linked to `self.about`
        about_button = Gtk.Button()
        about_button.connect("clicked", self.about)
        about_icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        about_image = Gtk.Image.new_from_gicon(about_icon, Gtk.IconSize.BUTTON)
        about_button.add(about_image)
        hb.pack_end(about_button)

        # Set the titlebar of the window to hb
        self.set_titlebar(hb)
        # Create Notebook
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.notebook.set_scrollable(True)
        # Add CSS class to Notebook
        notebook_style = self.notebook.get_style_context()
        notebook_style.add_class("myNotebook")

        # Get data
        for i in app.getUsersData(uname):
            self.data = i

        ####
        # Create self.notebook page(1)        
        page1 = Home(self.data, self)
        # Add CSS class to page1
        home_style = page1.get_style_context()
        home_style.add_class("home")
        # Set the name of the page as `Home`
        home = Gtk.Label(label="Home")
        home.set_size_request(150, 50)
        home.set_xalign(0)
        self.notebook.append_page(page1, home)

        ####
        # Create self.notebook page(2)
        page2 = Repo(self.data, self)
        # Add CSS class to page2
        page2_style = page2.get_style_context()
        page2_style.add_class("home")
        # Set the name of the page as `My Repos`
        title = Gtk.Label(label="\nMy Repos\n")
        title.set_xalign(0)
        self.notebook.append_page(page2, title)

        ####
        # Create self.notebook page(3)
        page3 = Working(self)
        # Add CSS class to page3
        page3_style = page3.get_style_context()
        page3_style.add_class("home")
        # Set the name of the page as `Working`
        title = Gtk.Label(label="\nWorking\n")
        title.set_xalign(0)
        self.notebook.append_page(page3, title)
        
        ####
        # Create self.notebook page(4)
        page4 = Idea(self.notebook, self)
        # Add CSS class to page4
        page4_style = page4.get_style_context()
        page4_style.add_class("home")
        # Set the name of the page as `My Repos`
        title = Gtk.Label(label="__________________________\n\nRecord Project Ideas\n")
        title.set_xalign(0)
        self.notebook.append_page(page4, title)
        # Add self.notebook widget to the main window

        idea_count = app.getIdeaCount(uname)
        for i in range(1, idea_count+1):
            for j in app.getIdeaData(i):
                data = j
            if (data[0]):
                page = IdeaPage(data, self)
                page_style = page.get_style_context()
                page_style.add_class("home")
                title = Gtk.Label(label=('\n' + f"Project Idea {i}" + '\n'))
                title.set_xalign(0)
                self.notebook.append_page(page, title)
        self.add(self.notebook)
        self.connect("destroy", Gtk.main_quit)

    # Function: create AboutDialog that displayed on the title bar
    def about(self, button):
        aboutdialog = Gtk.AboutDialog()

        author = ["MengZe"]
        copyright = "© MengZe 2020"
        version = "Version 1.0"
        # Set info
        aboutdialog.set_program_name("GNOME Project Manager")
        aboutdialog.set_authors(author)
        aboutdialog.set_copyright(copyright)
        aboutdialog.set_version(version)
        aboutdialog.set_website("https://github.com/openMengZe")
        aboutdialog.set_website_label("My GitHub")
        aboutdialog.set_title("About")
        aboutdialog.show_all()

    
    def refreshApp(self, button, page=''):
        if page == '':
            page = self.notebook.get_current_page()
        self.set_visible(False)
        window = MyWindow()
        window.connect("destroy", Gtk.main_quit)
        window.show_all()
        window.set_page(page)
        
    def set_page(self, page):
        self.notebook.set_current_page(page)


##########################################################################

# Class - Home
# This class creates Home page (Gtk.Box)
class Home(Gtk.Box):
    def __init__(self, data, main):
        varify()
        # Create window (vertical box)
        Gtk.Box.__init__(self)
        self.main = main
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(15)
        # Get data from `main.db` using MyDMS class
        self.data = data
        self.repo_count = app.getRepoCount(uname)
        # Set title of the window
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> Welcome Back, {self.data[4]}! </span>")
        title.set_margin_top(40)
        self.pack_start(title, False, True, 0)  
        # Create a vertical box container for containing stack and stack_switcher
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)
        # Create a Stack widget
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        # Child element of the stack - Profile window
        profile = self.profile()
        stack.add_titled(profile, "profile", "Profile")
        # Child element of the stack - Status window(worling)
        edit = self.editProfile(self.data)
        stack.add_titled(edit, "edit", "Edit Profile")
        # Create a stack_switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        hbox = Gtk.Box(spacing=3)
        hbox.pack_start(stack_switcher, False, True, 0)

        guide_button = Gtk.Button()
        guide_button.connect("clicked", self.guide)
        guide_icon = Gio.ThemedIcon(name="dialog-question-symbolic")
        guide_image = Gtk.Image.new_from_gicon(guide_icon, Gtk.IconSize.BUTTON)
        guide_button.add(guide_image)

        hbox.pack_start(guide_button, False, True, 5)

        delete = Gtk.Button(label="Delete Account")
        delete.connect("clicked", self.deleteWindow, uname)
        hbox.pack_end(delete, False, True, 5)

        # Add the stack and stack_switcher widgets to the container
        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(stack, True, True, 0)   
        # Add the container to the window
        self.pack_start(vbox, True, True, 0)

    def guide(self, button):
        Guide()


    def deleteWindow(self, button, uname):
        window = Gtk.Window()
        window.set_title("GNOME Project Manager - Delete Account")
        window.set_default_size(550, 350)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_halign(Gtk.Align.CENTER)

        title = Gtk.Label()
        title.set_markup("<span size='x-large'>Delete Account</span>")
        title.set_margin_top(20)
        vbox.pack_start(title, False, True, 15)

        note = Gtk.Label()
        note.set_markup("<i>Are you sure you want to delete this account?\nThis will delete all your data! permanently</i>")
        vbox.pack_start(note, False, True, 0)

        line_separator = Gtk.Separator()
        vbox.pack_start(line_separator, False, True, 5)

        confirm_note = Gtk.Label()
        confirm_note.set_markup("<b>Please type: 'Delete my account'</b>")
        vbox.pack_start(confirm_note, False, True, 5)

        message_input = Gtk.Entry()
        message_input.set_placeholder_text("Confirm Message")
        vbox.pack_start(message_input, False, False, 0)

        confirm = Gtk.Button(label="Confirm")
        confirm.connect("clicked", self.deleteAccount, message_input, window)

        vbox.pack_start(confirm, False, True, 10)

        window.add(vbox)
        window.show_all()

    def deleteAccount(self, button, message_input, window):
        message = message_input.get_text()
        global run
        if message == "Delete my account":
            app.deleteAccount(uname)
            dialog = Gtk.MessageDialog(
                parent=window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = '''
                Account deleted!
                '''
            )
            dialog.run()
            dialog.destroy()
            run = False
            exit()
            return run
        else:
            dialog = Gtk.MessageDialog(
                parent=window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = '''
                The confirm message is wrong.
                Please try again!
                '''
            )
            dialog.run()
            dialog.destroy()

    # Function: create Profile window for the Home Page (stack)    
    def profile(self):
        # Create a vertical box container
        my_profile = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # Create a container (listbox) that contains all the data using `self.makeProfile` method
        listbox = self.makeProfile(
            ["GitHub Account:", "GitHub URL:", "Repos:", "Followers:", "Email Address:", "Location:", "Company:", "Register Date:"], 
            [self.data[0], self.data[1], self.repo_count, self.data[6], self.data[2], self.data[8], self.data[7], self.data[3]]
            )
        # Add the containerto the box
        my_profile.pack_start(listbox, True, True, 0)
        return my_profile

    # Function: create ListBox and ListBoxRows with given data
    def makeProfile(self, item, content):
        window = Gtk.ScrolledWindow()
        # Create listbox
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        # Create rows for all data provided
        for i in range(len(item)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            row.add(hbox)
            # Set label of the row
            item_label = Gtk.Label(label=('\n' + item[i] + '\n'), xalign=0)
            content_label = Gtk.Label()
            # If the data is a link (app.url_validate == True), display it as a link
            if(app.url_validate(str(content[i])) or i == 4):
                content_label.set_markup(
                    f'<a href="/">{content[i]}</a>'
                )
            else:
                content_label.set_label(str(content[i]))
            # Add both label and content to the same row
            hbox.pack_start(item_label, True, True, 10)
            hbox.pack_start(content_label, False, True, 10)
            # Add the row to listbox
            listbox.add(row)
        window.add(listbox)
        return window
    
    def editProfile(self, data):
        # Create form
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        form.set_margin_top(30)
        name = Gtk.Box(spacing=8)
        name_label = Gtk.Label()
        name_label.set_markup("<b>Name*    </b>")
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Name*")
        try:
            name_input.set_text(data[4])
        except:
            pass

        name.pack_start(name_label, False, True, 40)
        name.pack_start(name_input, True, True, 40)

        form.pack_start(name, False, True, 0)
        # Get the email
        email = Gtk.Box(spacing=8)
        email_label = Gtk.Label()
        email_label.set_markup("<b>Email*     </b>")
        email_input = Gtk.Entry()
        email_input.set_placeholder_text("Email Address")
        try:
            email_input.set_text(data[2])
        except:
            pass
        
        email.pack_start(email_label, False, True, 40)
        email.pack_start(email_input, True, True, 40)

        form.pack_start(email, False, True, 0)
        # Get the GitHub URL
        github = Gtk.Box(spacing=8)
        github_label = Gtk.Label()
        github_label.set_markup("<b>URL         </b>")
        github_input = Gtk.Entry()
        github_input.set_placeholder_text("GitHub Page URL")
        try:
            github_input.set_text(data[1])
        except:
            pass

        github.pack_start(github_label, False, True, 40)
        github.pack_start(github_input, True, True, 40)

        form.pack_start(github, False, True, 0)

        location = Gtk.Box(spacing=8)
        location_label = Gtk.Label()
        location_label.set_markup("<b>Location </b>")
        location_input = Gtk.Entry()
        location_input.set_placeholder_text("Location")
        try:
            location_input.set_text(data[8])
        except:
            pass

        location.pack_start(location_label, False, True, 40)
        location.pack_start(location_input, True, True, 40)

        form.pack_start(location, False, True, 0)

        company = Gtk.Box(spacing=8)
        company_label = Gtk.Label()
        company_label.set_markup("<b>Company</b>")
        company_input = Gtk.Entry()
        company_input.set_placeholder_text("Company")
        try:
            company_input.set_text(data[7])
        except:
            pass

        company.pack_start(company_label, False, True, 40)
        company.pack_start(company_input, True, True, 40)

        form.pack_start(company, False, True, 0)
        # Child element of the form - submit button linked to `self.recordInfo`        
        submit = Gtk.Button(label="Confirm")
        submit.connect("clicked", self.updateData, name_input, github_input, email_input, location_input, company_input)
        form.pack_start(submit, False, True, 0)

        return form
    

    def updateData(self, button, name_input, github_input, email_input, location_input, company_input):
        name = name_input.get_text()
        github = github_input.get_text()
        email = email_input.get_text()
        location = location_input.get_text()
        company = company_input.get_text()

        # Check for the validity of the data
        if(name == '' or email == ''):
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text = "Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0

        try:
            app.updateUserData(uname, name, email, github, location, company)

            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags= 0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = 'Profile Updated!'
            )
            dialog.run()
            dialog.destroy()

            MyWindow.refreshApp(self.main, '')
            
        except:
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text = "Failed updating data!",
            )
            dialog.run()
            dialog.destroy()


# Class - Guide
# This class creates Guide window (Gtk.Window)
class Guide(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_title("GNOME Project Manager - User Guide")
        self.set_default_size(500, 500)
        self.set_border_width(5)

        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        notebook_style = notebook.get_style_context()
        notebook_style.add_class('myNotebook')

        page1 = self.home()
        page1_style = page1.get_style_context()
        page1_style.add_class('home')

        page1_label = Gtk.Label()
        page1_label.set_markup("<b>Home</b>")
        page1.set_halign(0)

        notebook.append_page(page1, page1_label)

        self.add(notebook)

        self.show_all()

    
    def home(self):
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        title = Gtk.Label()
        title.set_markup("<span size='xx-large'>Guide</span>")
        window.pack_start(title, False, True, 15)

        important = Gtk.Label()
        important.set_markup("<a href='https://www.howtogeek.com/669755/how-to-enable-dark-mode-on-ubuntu-20.04-lts/'><span color='white' size='large'>Please set your system to <b>DARK</b> theme for best experience</span></a>")
        window.pack_start(important, False, True, 10)
        return window

# Class - Repo
# This class creates Repo page (Gtk.Box)
class Repo(Gtk.Box):       
    # Function: create repo window for My Repos page 
    def __init__(self, data, main):
        varify()
        Gtk.Box.__init__(self)
        self.main = main
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(15)
        self.data = data
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> {self.data[0]}'s Repos! </span>")
        title.set_margin_top(40)
        self.pack_start(title, False, True, 0)  

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        repo_window = self.createRepoWindow()

        stack.add_titled(repo_window, "repo", "Repos")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        button = Gtk.Button()
        button.connect("clicked", self.repoNote)
        icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)

        hbox = Gtk.Box(spacing=15)
        hbox.pack_start(stack_switcher, False, True, 0)
        hbox.pack_start(button, False, True, 0)

        self.spinner = Gtk.Spinner()
        hbox.pack_end(self.spinner, False, True, 0)

        refresh = Gtk.Button(label="Refresh Repo")
        refresh.connect("clicked", self.refreshData, uname)
        hbox.pack_end(refresh, False, True, 5)

        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(stack, True, True, 0)

        self.pack_start(vbox, True, True, 0)
    
    def refreshData(self, button, uname):
        self.spinner.start()
        try:
            app.refreshData(uname)
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags = 0,
                message_type = Gtk.MessageType.INFO,
                buttons = Gtk.ButtonsType.OK,
                text = '''
                Data refreshed!
                Please refresh the app to load new data!
                '''
            )
            dialog.run()
            dialog.destroy()
            
        except:
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags = 0,
                message_type = Gtk.MessageType.INFO,
                buttons = Gtk.ButtonsType.OK,
                text = '''
                This process requires internet access!
                Please try again later!
                '''
            )
            dialog.run()
            dialog.destroy()
        self.spinner.stop()

    def repoNote(self, button):
        dialog = Gtk.MessageDialog(
                parent=MyWindow(),
                flags= 0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = "Note: only public repos are displayed here!"
            )
        dialog.run()
        dialog.destroy()
    

    def createRepoWindow(self):
        my_repo = Gtk.Box(spacing=6)

        self.data = []
        
        for i in app.getReposData(uname):
            self.data.append(i)
        
        listbox = self.makeRepo(self.data)
        my_repo.pack_start(listbox, True, True, 0)
        return my_repo
    
    # Function: create ListBox and ListBoxRows with given data
    def makeRepo(self, data):
        # Create listbox
        window = Gtk.ScrolledWindow()
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(spacing=20)
        row.add(hbox)

        id_label = Gtk.Label()
        id_label.set_markup("\n<b>Repo ID</b>\n")
        id_label.set_xalign(0)
        name_label = Gtk.Label()
        name_label.set_markup("\n<b>Repo Name</b>\n")
        url_label = Gtk.Label()
        url_label.set_markup("<b>Repo URL</b>")
        date_label = Gtk.Label()
        date_label.set_markup("<b>Repo Date</b>")
        forks_label = Gtk.Label()
        forks_label.set_markup("<b>Forks</b>")
        status_label = Gtk.Label(label="Status")
        status_label.set_markup("<b>Status</b>")

        hbox.pack_start(id_label, False, True, 5)
        hbox.pack_start(name_label, False, True, 0)
        hbox.pack_start(url_label, False, True, 0)
        hbox.pack_start(date_label, False, True, 0)
        hbox.pack_start(forks_label, False, True, 0)
        hbox.pack_start(status_label, False, True, 0)

        listbox.add(row)

        linebreak = Gtk.Separator()
        listbox.add(linebreak)
        
        # Create rows for all data provided
        for i in range(len(data)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(spacing=20)
            row.add(hbox)
            for j in range(len(data[i])-3):
                label = Gtk.Label()

                if (j == 0):
                    label.set_xalign(0)
                
                if (j == 3):
                    date = data[i][j][:10]
                    label.set_label(date)
                    hbox.pack_start(label, True, True, 0)
                    continue

                if(app.url_validate(str(data[i][j]))):
                    label.set_markup(f'<a href="{data[i][j]}">{data[i][j]}</a>')
                else:
                    label.set_label(str(data[i][j]))
                hbox.pack_start(label, True, True, 5)

            self.toggle = Gtk.ToggleButton(label="done")
            id = data[i][0]
            status = app.getRepoStatus(id)
            if(status == 1):
                self.toggle.set_active("True")
            self.toggle.connect("toggled", self.toggleSwitch, id) 
            hbox.pack_end(self.toggle, False, True, 5)
            # Add the row to listbox
            listbox.add(row)

        window.add(listbox)
        return window

    # Function - toggleSwitch
    # This allows the user to switch the toggleSwitch widget on/off
    def toggleSwitch(self, toggle, id):
        status = app.getRepoStatus(id)
        if (status == 1):
            app.toggleRepo(0, id, uname)
        else:
            app.toggleRepo(1, id, uname)
            
        MyWindow.refreshApp(self.main, '')


# Class - Working
# This class creates Working page (Gtk.Box)
class Working(Gtk.Box):
    # This is the third page of the app which displays all the repos that the user is currently working on
    def __init__(self, main):
        varify()
        Gtk.Box.__init__(self, spacing=15)
        self.main = main
        self.set_orientation(Gtk.Orientation.VERTICAL)
        # Set title of the window
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> Working </span>")
        title.set_margin_top(40)
        self.pack_start(title, False, True, 0) 

        my_repo = Gtk.Box(spacing=6)

        self.data = []
        
        for i in app.getProjectWorking(uname):
            self.data.append(i)
        
        working_listbox = self.makeProjectWorking(self.data)
        my_repo.pack_start(working_listbox, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        stack.add_titled(my_repo, "repo", "Working Projects")

        repo_new = self.createNewProjectWindow()
        stack.add_titled(repo_new, "repo_new", "New Project")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        button = Gtk.Button()
        button.connect("clicked", self.repoWorkingNote)
        icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)

        hbox = Gtk.Box(spacing=15)
        hbox.pack_start(stack_switcher, False, True, 0)
        hbox.pack_start(button, False, True, 0)

        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(stack, True, True, 0)

        self.pack_start(vbox, True, True, 0)

    
    def repoWorkingNote(self, button):
        dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags= 0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = '''
                This page displays all the projects
                that you are currently working on!
                '''
            )
        dialog.run()
        dialog.destroy()

    def makeProjectWorking(self, data):
        # Create listbox
        window = Gtk.ScrolledWindow()

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(spacing=20)
        row.add(hbox)

        id_label = Gtk.Label()
        id_label.set_markup("\n<b>Project ID</b>\n")
        id_label.set_xalign(0)
        name_label = Gtk.Label()
        name_label.set_markup("<b>Project Name</b>")
        path_label = Gtk.Label()
        path_label.set_markup("<b>Project Path</b>")

        hbox.pack_start(id_label, False, True, 5)
        hbox.pack_start(name_label, False, True, 0)
        hbox.pack_start(path_label, False, True, 0)

        listbox.add(row)

        linebreak = Gtk.Separator()
        listbox.add(linebreak)
        # Create rows for all data provided
        for i in range(len(data)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(spacing=20)
            row.add(hbox)
            for j in range(len(data[i])):
                label = Gtk.Label()
                if (j == 0):
                    label.set_xalign(0)
                    if len(str(data[i][j])) < 9:
                        label.set_label(str(f"{data[i][j]:09d}"))
                        hbox.pack_start(label, True, True, 5)
                        continue

                if(app.url_validate(str(data[i][j]))):
                    label.set_markup(f'<a href="{data[i][j]}">{data[i][j]}</a>')
                else:
                    label.set_label(str(data[i][j]))
                hbox.pack_start(label, True, True, 5)
            # Add the row to listbox
            button = Gtk.Button(label="Details")
            button.connect("clicked", self.createPanel, data[i][0])
            hbox.pack_start(button, False, True, 0)

            self.toggle = Gtk.ToggleButton(label="done")
            id = data[i][0]
            self.toggle.connect("toggled", self.projectDone, id) 
            hbox.pack_end(self.toggle, False, True, 5)
            # Add the row to listbox
            listbox.add(row)
        window.add(listbox)
        return window


    def createNewProjectWindow(self):
        scrolled_window = Gtk.ScrolledWindow()

        window = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        window.set_halign(Gtk.Align.CENTER)

        vbox_l = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        window.pack_start(vbox_l, True, True, 5)

        l_label = Gtk.Label()
        l_label.set_markup("<u><span size='large'>Basics Info</span></u>")
        vbox_l.pack_start(l_label, False, True, 10)

        project_name = Gtk.Box(spacing=6)
        project_name.set_halign(Gtk.Align.CENTER)
        project_name.set_margin_top(10)

        name_label = Gtk.Label()
        name_label.set_markup("<i>Project Name        </i>")
        project_name.pack_start(name_label, False, True, 10)
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Project Name (be creative)")
        project_name.pack_start(name_input, True, True, 0)

        vbox_l.pack_start(project_name, False, True, 0)

        project_type = Gtk.Box(spacing=6)
        project_type.set_halign(Gtk.Align.CENTER)

        type_label = Gtk.Label()
        type_label.set_markup("<i>Project Type          </i>")
        project_type.pack_start(type_label, False, True, 10)
        type_input = Gtk.Entry()
        type_input.set_placeholder_text("Project Type (app, web, algorithm, etc)")
        project_type.pack_start(type_input, False, True, 0)

        vbox_l.pack_start(project_type, False, True, 0)


        project_language = Gtk.Box(spacing=6)
        project_language.set_halign(Gtk.Align.CENTER)

        language_label = Gtk.Label()
        language_label.set_markup("<i>Project Language</i>")
        project_language.pack_start(language_label, False, True, 10)
        language_input = Gtk.Entry()
        language_input.set_placeholder_text("Project Language (JS, Python, PHP etc)")
        project_language.pack_start(language_input, False, True, 0)

        vbox_l.pack_start(project_language, False, True, 0)


        project_audience = Gtk.Box(spacing=6)
        project_audience.set_halign(Gtk.Align.CENTER)

        audience_label = Gtk.Label()
        audience_label.set_markup("<i>Project Audience </i>")
        project_audience.pack_start(audience_label, False, True, 10)
        audience_input = Gtk.Entry()
        audience_input.set_placeholder_text("Project Audience (who will use this project)")
        project_audience.pack_start(audience_input, True, True, 0)

        vbox_l.pack_start(project_audience, False, True, 0)

        url_label = Gtk.Label()
        url_label.set_markup("<i>Project Path</i>")

        vbox_l.pack_start(url_label, False, True, 0)

        url_input = Gtk.FileChooserButton()
        url_input.set_title("GNOME Project Manager - Select Folder")
        url_input.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        vbox_l.pack_start(url_input, False, True, 0)

        project_feature = Gtk.Box(spacing=6)

        feature_input = Gtk.TextView()

        feature_textbuffer = feature_input.get_buffer()
        feature_textbuffer.set_text("What's speacial about this project\n1.\n2.\n3.\n4.\n5.")

        project_feature.pack_start(feature_input, True, True, 15)
        vbox_l.pack_start(project_feature, True, True, 5)

        vbox_r = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        window.pack_start(vbox_r, False, True, 5)

        r_label = Gtk.Label()
        r_label.set_markup("<u><span size='large'>Project Details</span></u>")
        vbox_r.pack_start(r_label, False, True, 15)

        detail_input = Gtk.TextView()
        detail_input.set_wrap_mode(Gtk.WrapMode.WORD)
        detail_input.set_size_request(350, 300)

        detail_textbuffer = detail_input.get_buffer()
        detail_textbuffer.set_text("More details!")

        vbox_r.pack_start(detail_input, True, True, 0)

        record = Gtk.Button(label="Create")
        record.connect("clicked", self.createProject, name_input, type_input, language_input, audience_input, feature_textbuffer, detail_textbuffer, url_input)
        vbox_r.pack_start(record, False, True, 20)

        scrolled_window.add(window)
        return scrolled_window

    def createProject(self, button, name_input, type_input, language_input, audience_input, feature_textbuffer, detail_textbuffer, url_input):
        name = name_input.get_text()
        type = type_input.get_text()
        language = language_input.get_text()
        audience = audience_input.get_text()
        url = url_input.get_uris()

        feature_start_iter = feature_textbuffer.get_start_iter()
        feature_end_iter = feature_textbuffer.get_end_iter()
        feature = feature_textbuffer.get_text(feature_start_iter, feature_end_iter, True)

        detail_start_iter = detail_textbuffer.get_start_iter()
        detail_end_iter = detail_textbuffer.get_end_iter()
        detail = detail_textbuffer.get_text(detail_start_iter, detail_end_iter, True)

        if(name==''):
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Project Name cannot be empty!"
            )
            dialog.run()
            dialog.destroy()
            return 0

        try:
            if(url[0]):
                pass
        except:
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Project URL cannot be empty!"
            )
            dialog.run()
            dialog.destroy()
            return 0
            

        app.insertProjectDB(uname, name, language, type, audience, feature, detail, url[0])


        dialog = Gtk.MessageDialog(
            parent = MyWindow(),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text='''
            Project added!
            '''
        )

        dialog.run()
        dialog.destroy()
        MyWindow.refreshApp(self.main, '')

    
    def projectDone(self, button, id):
        window = Gtk.Window()
        window.set_title("GNOME Project Manager - Delete Account")
        window.set_default_size(550, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_halign(Gtk.Align.CENTER)

        title = Gtk.Label()
        title.set_markup("<span size='xx-large'>Project Done</span>")
        title.set_margin_top(20)
        vbox.pack_start(title, False, True, 15)

        note = Gtk.Label()
        note.set_markup('''
        <i>Are you sure you are done with working on this project? 
        This will delete the project data from database permanently!</i>
        ''')
        vbox.pack_start(note, False, True, 0)

        line_separator = Gtk.Separator()
        vbox.pack_start(line_separator, False, True, 5)

        buttons = Gtk.Box(spacing = 6)
        buttons.set_halign(Gtk.Align.CENTER)

        confirm = Gtk.Button(label="Yes")
        confirm.connect("clicked", self.toggleSwitch, id, window)

        exit = Gtk.Button(label="No")
        exit.connect("clicked", self.close, window)

        buttons.pack_start(confirm, False, True, 0)
        buttons.pack_start(exit, False, True, 0)

        vbox.pack_start(buttons, False, True, 10)

        window.add(vbox)
        window.show_all()
    

    # Function - toggleSwitch
    # This allows the user to switch the toggleSwitch widget on/off
    def toggleSwitch(self, button, id, window):
        app.toggleProject(1, id, uname)
        self.close('', window)

        dialog = Gtk.MessageDialog(
            parent = MyWindow(),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text='''
            Project Deleted!
            '''
        )
        dialog.run()
        dialog.destroy()
        MyWindow.refreshApp(self.main, '')

    def close(self, button, window):
        window.destroy()

    def createPanel(self, button, id):
        panel = projectPanel(id)


# Class - Idea
# This class creates Idea page (Gtk.Box)
class Idea(Gtk.Box):
    # Function: creates Idea window
    def __init__(self, notebook, main):
        varify()
        Gtk.Box.__init__(self, spacing=15)
        self.main = main

        self.set_orientation(Gtk.Orientation.VERTICAL)
            
        self.notebook = notebook

        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> Project Ideas </span>")
        title.set_margin_top(40)
        self.pack_start(title, False, True, 0)  

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        repo_window = self.createIdeaWindow()

        stack.add_titled(repo_window, "repo", "Create Ideas")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        button = Gtk.Button()
        button.connect("clicked", self.ideaNote)
        icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)

        hbox = Gtk.Box(spacing=15)
        hbox.pack_start(stack_switcher, False, True, 0)
        hbox.pack_start(button, False, True, 0)

        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(stack, True, True, 0)

        self.pack_start(vbox, True, True, 0)


    def ideaNote(self, button):
        dialog = Gtk.MessageDialog(
            parent = MyWindow(),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text = '''
            Record your creative project idea and work
            on them later!
            '''
        )
        dialog.run()
        dialog.destroy()


    def createIdeaWindow(self):
        scrolled_window =Gtk.ScrolledWindow()

        window = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        window.set_halign(Gtk.Align.CENTER)

        vbox_l = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        window.pack_start(vbox_l, True, True, 5)

        l_label = Gtk.Label()
        l_label.set_markup("<u><span size='large'>Basics Info</span></u>")
        vbox_l.pack_start(l_label, False, True, 10)

        project_name = Gtk.Box(spacing=6)
        project_name.set_halign(Gtk.Align.CENTER)
        project_name.set_margin_top(10)

        name_label = Gtk.Label()
        name_label.set_markup("<i>Project Name        </i>")
        project_name.pack_start(name_label, False, True, 10)
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Project Name (be creative)")
        project_name.pack_start(name_input, True, True, 0)

        vbox_l.pack_start(project_name, False, True, 0)

        project_type = Gtk.Box(spacing=6)
        project_type.set_halign(Gtk.Align.CENTER)

        type_label = Gtk.Label()
        type_label.set_markup("<i>Project Type          </i>")
        project_type.pack_start(type_label, False, True, 10)
        type_input = Gtk.Entry()
        type_input.set_placeholder_text("Project Type (app, web, algorithm, etc)")
        project_type.pack_start(type_input, False, True, 0)

        vbox_l.pack_start(project_type, False, True, 0)


        project_language = Gtk.Box(spacing=6)
        project_language.set_halign(Gtk.Align.CENTER)

        language_label = Gtk.Label()
        language_label.set_markup("<i>Project Language</i>")
        project_language.pack_start(language_label, False, True, 10)
        language_input = Gtk.Entry()
        language_input.set_placeholder_text("Project Language (JS, Python, PHP etc)")
        project_language.pack_start(language_input, False, True, 0)

        vbox_l.pack_start(project_language, False, True, 0)


        project_audience = Gtk.Box(spacing=6)
        project_audience.set_halign(Gtk.Align.CENTER)

        audience_label = Gtk.Label()
        audience_label.set_markup("<i>Project Audience </i>")
        project_audience.pack_start(audience_label, False, True, 10)
        audience_input = Gtk.Entry()
        audience_input.set_placeholder_text("Project Audience (who will use this project)")
        project_audience.pack_start(audience_input, True, True, 0)

        vbox_l.pack_start(project_audience, False, True, 0)

        project_feature = Gtk.Box(spacing=6)

        feature_input = Gtk.TextView()

        feature_textbuffer = feature_input.get_buffer()
        feature_textbuffer.set_text("Project Features\n1.\n2.\n3.\n4.\n5.")

        project_feature.pack_start(feature_input, True, True, 15)
        vbox_l.pack_start(project_feature, True, True, 20)

        vbox_r = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        window.pack_start(vbox_r, False, True, 5)

        r_label = Gtk.Label()
        r_label.set_markup("<u><span size='large'>Project Details</span></u>")
        vbox_r.pack_start(r_label, False, True, 15)

        detail_input = Gtk.TextView()
        detail_input.set_wrap_mode(Gtk.WrapMode.WORD)
        detail_input.set_size_request(350, 300)

        detail_textbuffer = detail_input.get_buffer()
        detail_textbuffer.set_text("More details!")

        vbox_r.pack_start(detail_input, True, True, 0)

        record = Gtk.Button(label="Record")
        record.connect("clicked", self.recordIdea, name_input, type_input, language_input, audience_input, feature_textbuffer, detail_textbuffer)
        
        vbox_r.pack_end(record, False, True, 20)

        scrolled_window.add(window)
        return scrolled_window
    
    def recordIdea(self, button, name_input, type_input, language_input, audience_input, feature_textbuffer, detail_textbuffer):
        name = name_input.get_text()
        type = type_input.get_text()
        language = language_input.get_text()
        audience = audience_input.get_text()

        feature_start_iter = feature_textbuffer.get_start_iter()
        feature_end_iter = feature_textbuffer.get_end_iter()
        feature = feature_textbuffer.get_text(feature_start_iter, feature_end_iter, True)

        detail_start_iter = detail_textbuffer.get_start_iter()
        detail_end_iter = detail_textbuffer.get_end_iter()
        detail = detail_textbuffer.get_text(detail_start_iter, detail_end_iter, True)

        if(name==''):
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Project Name cannot be empty!"
            )
            dialog.run()
            dialog.destroy()
            return 0

        app.insertIdeaDB(uname, name, language, type, audience, feature, detail)

        dialog = Gtk.MessageDialog(
            parent = MyWindow(),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Idea added!"
        )
        dialog.run()
        dialog.destroy()
        
        idea_count = app.getIdeaCount(uname)

        data = app.getIdeaData(idea_count)
        for i in data:
            data = i
        page = IdeaPage(data, self.main)
        page_style = page.get_style_context()
        page_style.add_class("home")

        title = Gtk.Label(label=('\n' + f"Project Idea {idea_count}" + '\n'))
        title.set_xalign(0)

        self.notebook.append_page(page, title)
        self.notebook.show_all()


# Class - Idea
# This class creates contents based on `ideas` database table
class IdeaPage(Gtk.Box):
    def __init__(self, data, main):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.data = data
        self.main = main
        self.key = 8
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> Idea - {password.decrypt(self.key, self.data[1])} </span>")
        title.set_margin_top(40)
        self.pack_start(title, False, True, 0)
        # Create a vertical box container for containing stack and stack_switcher
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)
        # Create a Stack widget
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        # Child element of the stack - Profile window
        profile = self.Info()
        stack.add_titled(profile, "profile", "Profile")
        # Child element of the stack - Status window(worling)
        edit = self.editInfo()
        stack.add_titled(edit, "edit", "Edit Profile")
        # Create a stack_switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        hbox = Gtk.Box(spacing=3)
        hbox.pack_start(stack_switcher, False, True, 5)

        delete = Gtk.Button(label="Delete Idea")
        delete.connect("clicked", self.deleteIdea)
        hbox.pack_end(delete, False, True, 5)

        start = Gtk.Button(label="Start Idea")
        start.connect("clicked", self.startProject, uname)
        hbox.pack_end(start, False, True, 5)

        # Add the stack and stack_switcher widgets to the container
        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(stack, True, True, 0)   
        # Add the container to the window
        self.pack_start(vbox, True, True, 0)

    def Info(self):
        # Create a vertical box container
        idea_Info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        id = self.data[0]
        # Create a container (listbox) that contains all the data using `self.makeProfile` method
        listbox = self.makeInfo(
            ["Idea Name:", "Idea Language:", "Idea Type:", "Idea Audience:", "Idea Feature:", "Idea Detail:", "Created Date:"], 
            [password.decrypt(self.key, self.data[1]), self.data[2], self.data[3], self.data[4], password.decrypt(self.key, self.data[5]), password.decrypt(self.key, self.data[6]), self.data[7]]
            )
        # Add the containerto the box
        idea_Info.pack_start(listbox, True, True, 0)
        return idea_Info

    # Function: create ListBox and ListBoxRows with given data
    def makeInfo(self, item, content):
        # Create listbox
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        # Create rows for all data provided
        for i in range(len(item)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            row.add(hbox)
            # Set label of the row
            item_label = Gtk.Label(label=('\n' + item[i] + '\n'), xalign=0)
            content_label = Gtk.Label()
            content_label.set_label(str(content[i]))
            # Add both label and content to the same row
            hbox.pack_start(item_label, True, True, 10)
            hbox.pack_start(content_label, False, True, 10)
            # Add the row to listbox
            listbox.add(row)
        return listbox

    def deleteIdea(self, button):
        id = self.data[0]
        app.deleteIdea(id)
        MyWindow.refreshApp(self.main, '', 2)
    
    def startProject(self, button, uname):
        app.insertProjectDB(uname, password.decrypt(8, self.data[1]), self.data[2], self.data[3], self.data[4], password.decrypt(8, self.data[5]), password.decrypt(8, self.data[6]))
        self.deleteIdea(button)


    def editInfo(self):
        # Create form
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        form.set_margin_top(30)
        name = Gtk.Box(spacing=8)
        name_label = Gtk.Label()
        name_label.set_markup("<b>Idea Name*     </b>")
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Idea Name*")
        name_input.set_text(password.decrypt(self.key, self.data[1]))

        name.pack_start(name_label, False, True, 40)
        name.pack_start(name_input, True, True, 40)

        form.pack_start(name, False, True, 0)
        # Get the email
        language = Gtk.Box(spacing=8)
        language_label = Gtk.Label()
        language_label.set_markup("<b>Idea Language</b>")
        language_input = Gtk.Entry()
        language_input.set_placeholder_text("Idea Language")
        language_input.set_text(self.data[2])
        
        language.pack_start(language_label, False, True, 40)
        language.pack_start(language_input, True, True, 40)

        form.pack_start(language, False, True, 0)
        # Get the GitHub URL
        type = Gtk.Box(spacing=8)
        type_label = Gtk.Label()
        type_label.set_markup("<b>Idea Type         </b>")
        type_input = Gtk.Entry()
        type_input.set_placeholder_text("Idea Type")
        type_input.set_text(self.data[3])

        type.pack_start(type_label, False, True, 40)
        type.pack_start(type_input, True, True, 40)

        form.pack_start(type, False, True, 0)

        audience = Gtk.Box(spacing=8)
        audience_label = Gtk.Label()
        audience_label.set_markup("<b>Idea Audience </b>")
        audience_input = Gtk.Entry()
        audience_input.set_placeholder_text("Idea Audience")
        audience_input.set_text(self.data[4])

        audience.pack_start(audience_label, False, True, 40)
        audience.pack_start(audience_input, True, True, 40)

        form.pack_start(audience, False, True, 0)

        feature = Gtk.Box(spacing=8)
        feature_label = Gtk.Label()
        feature_label.set_markup("<b>Idea Feature    </b>")
        feature_input = Gtk.Entry()
        feature_input.set_placeholder_text("Idea Feature")
        feature_input.set_text(password.decrypt(self.key, self.data[5]))

        feature.pack_start(feature_label, False, True, 40)
        feature.pack_start(feature_input, True, True, 40)

        form.pack_start(feature, False, True, 0)

        detail = Gtk.Box(spacing=8)
        detail_label = Gtk.Label()
        detail_label.set_markup("<b>Idea Details     </b>")
        detail_input = Gtk.Entry()
        detail_input.set_placeholder_text("Idea Details")
        detail_input.set_text(password.decrypt(self.key, self.data[6]))

        detail.pack_start(detail_label, False, True, 40)
        detail.pack_start(detail_input, True, True, 40)

        form.pack_start(detail, False, True, 0)
        # Child element of the form - submit button linked to `self.recordInfo`        
        submit = Gtk.Button(label="Confirm")
        submit.connect("clicked", self.updateData, name_input, language_input, type_input, audience_input, feature_input, detail_input)
        form.pack_start(submit, False, True, 0)

        return form

    def updateData(self, button, name_input, language_input, type_input, audience_input, feature_input, detail_input):
        id = self.data[0]
        name = name_input.get_text()
        language = language_input.get_text()
        type = type_input.get_text()
        audience = audience_input.get_text()
        feature = feature_input.get_text()
        detail = detail_input.get_text()


         # Check for the validity of the data
        if(name == ''):
            dialog = Gtk.MessageDialog(
                parent = MyWindow(),
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text = "Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0

        app.updateIdeaData(id, name, language, type, audience, feature, detail)
        MyWindow.refreshApp(self.main, '')
            
    
##########################################################################


# Class - workingPanel
# This class provides all the main functionalities of the app
class projectPanel(Gtk.Window):
    def __init__(self, id):
        varify()
        Gtk.Window.__init__(self)
        self.set_title("GNOME Project Manager - Project Panel")
        self.set_default_size(1000, 650)
        
        self.main = main
        self.id = id

        self.data = app.getProjectData(id)

        for i in self.data:
            self.data = i

        # Create headbar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = f"GNOME Project Manager - Project Panel"
        # Child element of the headbar - about button linked to `self.about`
        about_button = Gtk.Button()
        about_button.connect("clicked", self.about)
        about_icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        about_image = Gtk.Image.new_from_gicon(about_icon, Gtk.IconSize.BUTTON)
        about_button.add(about_image)
        hb.pack_end(about_button)

        refresh = Gtk.Button(label="Refresh App")
        refresh.connect("clicked", self.refreshApp)
        hb.pack_start(refresh)

        # Set the titlebar of the window to hb
        self.set_titlebar(hb)
        # Create Notebook
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.notebook.set_scrollable(True)
        # Add CSS class to Notebook
        notebook_style = self.notebook.get_style_context()
        notebook_style.add_class("myNotebook")

        ####
        # Create self.notebook page(1)     
        page1 = Info(self.data, self, self.id)
        # Add CSS class to page1
        home_style = page1.get_style_context()
        home_style.add_class("home")
        # Set the name of the page as `Home`
        home = Gtk.Label(label="\nProject Info\n")
        home.set_size_request(150, 50)
        home.set_xalign(0)
        self.notebook.append_page(page1, home)

        ####
        # Create self.notebook page(2)      
        page2 = Code(self.data[6], self, self.id)
        # Add CSS class to page1
        home_style = page2.get_style_context()
        home_style.add_class("home")
        # Set the name of the page as `Home`
        code = Gtk.Label(label="\nStart Coding\n")
        code.set_size_request(150, 50)
        code.set_xalign(0)
        self.notebook.append_page(page2, code)

        ####
        # Create self.notebook page(3)      
        page3 = Search(self, self.id)
        # Add CSS class to page1
        home_style = page3.get_style_context()
        home_style.add_class("home")
        # Set the name of the page as `Home`
        stack_overflow = Gtk.Label(label="\nSearch\n")
        stack_overflow.set_size_request(150, 50)
        stack_overflow.set_xalign(0)
        self.notebook.append_page(page3, stack_overflow)

        ####
        # Create self.notebook page(4)      
        page4 = Resources(self, self.id)
        # Add CSS class to page1
        home_style = page4.get_style_context()
        home_style.add_class("home")
        # Set the name of the page as `Home`
        resources = Gtk.Label(label="\nResources\n")
        resources.set_size_request(150, 50)
        resources.set_xalign(0)
        self.notebook.append_page(page4, resources)

        self.add(self.notebook)
        self.show_all()

    # Function: create AboutDialog that displayed on the title bar
    def about(self, button):
        aboutdialog = Gtk.AboutDialog()

        author = ["MengZe"]
        copyright = "© MengZe 2020"
        version = "Version 1.0"
        # Set info
        aboutdialog.set_program_name("GNOME Project Manager")
        aboutdialog.set_authors(author)
        aboutdialog.set_copyright(copyright)
        aboutdialog.set_version(version)
        aboutdialog.set_website("https://github.com/openMengZe")
        aboutdialog.set_website_label("My GitHub")
        aboutdialog.set_title("About")
        aboutdialog.show_all()

    def refreshApp(self, button):
        page = self.notebook.get_current_page()
        self.set_visible(False)
        window = projectPanel(self.id)
        window.show_all()
        window.set_page(page)

    def set_page(self, page):
        self.notebook.set_current_page(page)



class Info(Gtk.Box):
    def __init__(self, data, main, id):
        # Create window (vertical box)
        Gtk.Box.__init__(self)
        self.main = main
        self.id = id

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(15)
        # Get data from `main.db` using MyDMS class
        self.data = data
        # Set title of the window
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> {self.data[0]} </span>")
        title.set_margin_top(40)
        self.pack_start(title, False, True, 0)  
        # Create a vertical box container for containing stack and stack_switcher
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)
        # Create a Stack widget
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        # Child element of the stack - Profile window
        info = self.projectInfo()
        stack.add_titled(info, "info", "Project Info")
        # Child element of the stack - Status window(worling)
        edit = self.editProject()
        stack.add_titled(edit, "edit", "Edit Project")
        # Create a stack_switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        hbox = Gtk.Box(spacing=3)
        hbox.pack_start(stack_switcher, False, True, 0)

        # Add the stack and stack_switcher widgets to the container
        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(stack, True, True, 0)   
        # Add the container to the window
        self.pack_start(vbox, True, True, 0)

        # Function: create Profile window for the Home Page (stack)    
    def projectInfo(self):
        # Create a vertical box container
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # Create a container (listbox) that contains all the data using `self.makeProfile` method
        listbox = self.makeInfo(
            ["Project Name:", "Project Language:", "Project Type", "Project Audience", "Project Feature", "Project Details:", "Project URL:", "Register Date:"], 
            [self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5], self.data[6], self.data[7]]
            )
        # Add the containerto the box
        info.pack_start(listbox, True, True, 0)
        return info

    # Function: create ListBox and ListBoxRows with given data
    def makeInfo(self, item, content):
        # Create listbox
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        # Create rows for all data provided
        for i in range(len(item)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            row.add(hbox)
            # Set label of the row
            item_label = Gtk.Label(label=('\n' + item[i] + '\n'), xalign=0)
            content_label = Gtk.Label()
            # If the data is a link (app.url_validate == True), display it as a link
            content_label.set_label(str(content[i]))
            # Add both label and content to the same row
            hbox.pack_start(item_label, True, True, 10)
            hbox.pack_start(content_label, False, True, 10)
            # Add the row to listbox
            listbox.add(row)
        return listbox
    
    def editProject(self):
        # Create form
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        form.set_margin_top(30)
        name = Gtk.Box(spacing=8)
        name_label = Gtk.Label()
        name_label.set_markup("<b>Project Name*     </b>")
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Project Name*")
        name_input.set_text(self.data[0])

        name.pack_start(name_label, False, True, 40)
        name.pack_start(name_input, True, True, 40)

        form.pack_start(name, False, True, 0)
        # Get the email
        language = Gtk.Box(spacing=8)
        language_label = Gtk.Label()
        language_label.set_markup("<b>Project Language</b>")
        language_input = Gtk.Entry()
        language_input.set_placeholder_text("Project Language")
        language_input.set_text(self.data[1])
        
        language.pack_start(language_label, False, True, 40)
        language.pack_start(language_input, True, True, 40)

        form.pack_start(language, False, True, 0)
        # Get the GitHub URL
        type = Gtk.Box(spacing=8)
        type_label = Gtk.Label()
        type_label.set_markup("<b>Project Type         </b>")
        type_input = Gtk.Entry()
        type_input.set_placeholder_text("Project Type")
        type_input.set_text(self.data[2])

        type.pack_start(type_label, False, True, 40)
        type.pack_start(type_input, True, True, 40)

        form.pack_start(type, False, True, 0)

        audience = Gtk.Box(spacing=8)
        audience_label = Gtk.Label()
        audience_label.set_markup("<b>Project Audience </b>")
        audience_input = Gtk.Entry()
        audience_input.set_placeholder_text("Project Audience")
        audience_input.set_text(self.data[3])

        audience.pack_start(audience_label, False, True, 40)
        audience.pack_start(audience_input, True, True, 40)

        form.pack_start(audience, False, True, 0)

        feature = Gtk.Box(spacing=8)
        feature_label = Gtk.Label()
        feature_label.set_markup("<b>Project Feature    </b>")
        feature_input = Gtk.Entry()
        feature_input.set_placeholder_text("Project Feature")
        feature_input.set_text(self.data[4])

        feature.pack_start(feature_label, False, True, 40)
        feature.pack_start(feature_input, True, True, 40)

        form.pack_start(feature, False, True, 0)

        detail = Gtk.Box(spacing=8)
        detail_label = Gtk.Label()
        detail_label.set_markup("<b>Project Details     </b>")
        detail_input = Gtk.Entry()
        detail_input.set_placeholder_text("Project Details")
        detail_input.set_text(self.data[5])

        detail.pack_start(detail_label, False, True, 40)
        detail.pack_start(detail_input, True, True, 40)

        form.pack_start(detail, False, True, 0)

        path = Gtk.Box(spacing=8)

        path_label = Gtk.Label()
        path_label.set_markup("<b>Project Directory*</b>")

        path_input = Gtk.FileChooserButton()
        path_input.set_title("GNOME Project Manager - Select Folder")
        path_input.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        path.pack_start(path_label, False, True, 40)
        path.pack_start(path_input, True, True, 40)

        form.pack_start(path, False, True, 0)
        # Child element of the form - submit button linked to `self.recordInfo`        
        submit = Gtk.Button(label="Confirm")
        submit.connect("clicked", self.updateData, name_input, language_input, type_input, audience_input, feature_input, detail_input, path_input)
        form.pack_start(submit, False, True, 0)

        return form
    

    def updateData(self, button, name_input, language_input, type_input, audience_input, feature_input, detail_input, path_input):
        name = name_input.get_text()
        language = language_input.get_text()
        type = type_input.get_text()
        audience = audience_input.get_text()
        feature = feature_input.get_text()
        detail = detail_input.get_text()
        path = path_input.get_uris()


         # Check for the validity of the data
        if(name == ''):
            dialog = Gtk.MessageDialog(
                parent = self,
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text = "Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0

        try:
            if(path[0]):
                pass
        except:
            dialog = Gtk.MessageDialog(
                parent = self.main,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="Project URL cannot be empty!"
            )
            dialog.run()
            dialog.destroy()
            return 0

        app.updateProjectData(self.id, name, language, type, audience, feature, detail, path[0])

        try:
            dialog = Gtk.MessageDialog(
                parent = self.main,
                flags= 0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text = '''
                Project data updated!
                ''',
            )
            dialog.run()
            dialog.destroy()
            projectPanel.refreshApp(self.main, '')
            
        except:
            dialog = Gtk.MessageDialog(
                parent = self.main,
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text = "Failed updating data!",
            )
            dialog.run()
            dialog.destroy()


class Code(Gtk.Box):
    def __init__(self, address, main, id):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(15)

        self.main = main
        self.id = id

        title = Gtk.Label()
        title.set_markup("<span size='xx-large'>Starting Coding</span>")
        title.set_margin_top(50)
        self.pack_start(title, False, True, 15)

        selectIDE = Gtk.Box(spacing=6)
        selectIDE.set_halign(Gtk.Align.CENTER)

        label = Gtk.Label()
        label.set_markup("<b>Choose a code editor</b>")

        selectIDE.pack_start(label, False, True, 0)

        self.selector = Gtk.ComboBoxText()
        self.selector.insert(0, "0", "Visual Studio Code")
        self.selector.insert(1, "1", "Sublime Text")
        self.selector.set_active(0)
        selectIDE.pack_start(self.selector, False, True, 0)

        about_button = Gtk.Button()
        about_button.connect("clicked", self.about)
        about_icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        about_image = Gtk.Image.new_from_gicon(about_icon, Gtk.IconSize.BUTTON)
        about_button.add(about_image)
        selectIDE.pack_start(about_button, False, True, 10)

        self.pack_start(selectIDE, False, True, 0)

        button = Gtk.Button(label="Start Coding")
        button.connect("clicked", self.runIDE, address)
        button.set_halign(Gtk.Align.CENTER)

        self.pack_start(button, False, True, 0)

        todo_label = Gtk.Label()
        todo_label.set_markup("<span size='x-large'> <u> Todo List </u> </span>")
        todo_label.set_halign(Gtk.Align.START)

        self.pack_start(todo_label, False, True, 5)

        window = Gtk.ScrolledWindow()
        window.set_size_request(0, 250)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        todo = app.getTodo(self.id)

        if todo == '':
            todo = "1.\n2.\n3.\n4.\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

        todo_box = Gtk.Box(spacing=6)

        todo_list = Gtk.TextView()
        textbuffer = todo_list.get_buffer()
        textbuffer.set_text(todo)
        todo_box.pack_start(todo_list, True, True, 10)

        vbox.pack_start(todo_box, False, False, 0)

        window.add(vbox)
        self.pack_start(window, False, True, 0)

        todo_button = Gtk.Button(label="Update Todo")
        todo_button.connect("clicked", self.recordTodo, textbuffer)
        self.pack_start(todo_button, False, True, 0)


    def runIDE(self, button, address):
        IDE = self.selector.get_active()
        if IDE == 0:
            try:
                os.system(f"code --folder-uri {address}")
            except:
                dialog = Gtk.MessageDialog(
                    parent = self.main,
                    flags= 0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text = "Invalid URL",
                )
                dialog.run()
                dialog.destroy()
                return 0
        elif IDE == 1:
            try:
                os.system(f"subl {address[5:]}")
            except:
                dialog = Gtk.MessageDialog(
                    parent = self.main,
                    flags= 0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text = "Invalid URL",
                )
                dialog.run()
                dialog.destroy()
                return 0

    def recordTodo(self, button, textbuffer):
        start = textbuffer.get_start_iter()
        end = textbuffer.get_end_iter()

        todo_content = textbuffer.get_text(start, end, True)
        app.updateTodo(self.id, todo_content)

        projectPanel.refreshApp(self.main, '')


    def about(self, button):
        dialog = Gtk.MessageDialog(
            parent = self.main,
            flags = 0,
            message_type = Gtk.MessageType.INFO,
            buttons = Gtk.ButtonsType.OK,
            text = 
            '''
            Only 2 IDEs are available at this stage
            (the developer of this app cannot handle Vim)
            '''
        )

        dialog.run()
        dialog.destroy()        


class Search(Gtk.Box):
    def __init__(self, main, id):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(15)

        self.main = main
        self.id = id

        title = Gtk.Label()
        title.set_markup("<span size='xx-large'> Search Online </span>")
        title.set_margin_top(50)

        self.pack_start(title, False, True, 5)

        selectBrowser = Gtk.Box(spacing=6)
        selectBrowser.set_halign(Gtk.Align.CENTER)

        label = Gtk.Label()
        label.set_markup("<b>Choose a browser</b>")

        selectBrowser.pack_start(label, False, True, 0)

        self.browser_selector = Gtk.ComboBoxText()
        self.browser_selector.insert(0, "0", "Firefox")
        self.browser_selector.insert(1, "1", "Google Chrome")
        self.browser_selector.set_active(0)
        selectBrowser.pack_start(self.browser_selector, False, True, 0)

        about_button = Gtk.Button()
        about_button.connect("clicked", self.about)
        about_icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        about_image = Gtk.Image.new_from_gicon(about_icon, Gtk.IconSize.BUTTON)
        about_button.add(about_image)
        selectBrowser.pack_start(about_button, False, True, 10)

        self.pack_start(selectBrowser, False, True, 0)

        search = Gtk.Box()
        search.set_halign(Gtk.Align.CENTER)
        search.set_size_request(700, 0)

        self.website_selector = Gtk.ComboBoxText()
        self.website_selector.insert(0, "0", "Google")
        self.website_selector.insert(1, "1", "StackOverflow")
        self.website_selector.set_active(0)

        question_input = Gtk.Entry()
        question_input.set_placeholder_text("Eg. How to use pyinstaller")

        search.pack_start(self.website_selector, False, False, 15)
        search.pack_start(question_input, True, True, 20)

        self.pack_start(search, False, True, 5)

        search = Gtk.Button(label='Search')
        search.connect("clicked", self.search, question_input)

        self.pack_start(search, False, True, 5)

        history = self.history()

        self.pack_start(history, True, False, 15)

        clear = Gtk.Button(label='Clear History')
        clear.connect("clicked", self.clearHistory)
        self.pack_end(clear, False, True, 0)

    
    def search(self, button, question_input, question=''):
        if question == '':
            question = question_input.get_text()
        browser = self.browser_selector.get_active()
        website = self.website_selector.get_active()

        if website == 0:
            if browser == 0:
                link = f"firefox 'https://www.google.com/search?q={question}'"
                os.system(link)
            elif browser == 1:
                link = f"google-chrome 'https://www.google.com/search?q={question}'"
                os.system(link)
        
        elif website == 1:
            if browser == 0:
                link = f"firefox 'https://stackoverflow.com/search?q={question}'"
                os.system(link)
            elif browser == 1:
                link = f"google-chrome 'https://stackoverflow.com/search?q={question}'"
                os.system(link)

        app.insertSearchDB(self.id, question, link)
        question_input.set_text('')
        projectPanel.refreshApp(self.main, '')
    
    def history(self):
        window = Gtk.ScrolledWindow()
        window.set_size_request(0, 300)

        box = Gtk.Box()
        box.set_halign(Gtk.Align.CENTER)

        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        box.pack_start(self.vbox1, False, True, random.randint(20, 60))
        box.pack_start(self.vbox2, False, True, random.randint(20, 60))
        box.pack_start(self.vbox3, False, True, random.randint(20, 60))

        data = app.getHistory(self.id)

        for i in data:
            question = i[1]
            url = i[2]

            button = Gtk.Button()
            button.set_label(question)
            button.connect("clicked", self.search, '', question)
            button.set_size_request(random.randint(0, 30), random.randint(30, 70))
            container = random.randint(1, 3)
            if container == 1:
                self.vbox1.pack_start(button, False, False, random.randint(5, 25))
            if container == 2:
                self.vbox2.pack_start(button, False, False, random.randint(5, 25))
            if container == 3:
                self.vbox3.pack_start(button, False, False, random.randint(5, 25))

        window.add(box)

        return window

    def visitURL(self, button, url):
        try:
            os.system(f"firefox '{url}'")
        except:
            os.system(f"google-chrome '{url}'")

    def clearHistory(self, button):
        app.clearHistory(self.id)
        projectPanel.refreshApp(self.main, '')

    def about(self, button):
        dialog = Gtk.MessageDialog(
            parent = self.main,
            flags = 0,
            message_type = Gtk.MessageType.INFO,
            buttons = Gtk.ButtonsType.OK,
            text = "This requires internet access!"     
        )
        dialog.run()
        dialog.destroy()


class Resources(Gtk.Box):
    def __init__(self, main, id):
        Gtk.Box.__init__(self)
        self.set_spacing(15)
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.main = main
        self.id = id

        title = Gtk.Label()
        title.set_markup("<span size='xx-large'>Resources</span>")
        title.set_margin_top(40)

        self.pack_start(title, False, True, 15)

        recordName = Gtk.Box(spacing=6)
        recordName.set_halign(Gtk.Align.CENTER)
        recordName.set_size_request(600, 0)

        name_label = Gtk.Label()
        name_label.set_markup("<b>Website Name*</b>")

        recordName.pack_start(name_label, False, True, 10)

        name_input = Gtk.Entry()

        recordName.pack_start(name_input, True , True, 0)

        self.pack_start(recordName, False, True, 0)

        recordURL = Gtk.Box(spacing=6)
        recordURL.set_halign(Gtk.Align.CENTER)
        recordURL.set_size_request(600, 0)

        label = Gtk.Label()
        label.set_markup("<b>Website URL*   </b>")

        recordURL.pack_start(label, False, True, 10)

        url_input = Gtk.Entry()

        recordURL.pack_start(url_input, True , True, 0)

        self.pack_start(recordURL, False, True, 0)

        button = Gtk.Button(label="Record")
        button.connect("clicked", self.recordResource, name_input, url_input)
        self.pack_start(button, False, True, 0)

        display = self.display()

        self.pack_start(display, True, False, 15)

        clear = Gtk.Button(label="Clear All")
        clear.connect("clicked", self.clearResource)
        self.pack_end(clear, False, True, 0)

    
    def recordResource(self, button, name_input, url_input):
        name = name_input.get_text()
        url = url_input.get_text()

        if(name == '' or url == ''):
            dialog = Gtk.MessageDialog(
                parent = self.main,
                flags= 0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text = "Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0

        if(app.url_validate(url) == False):
            dialog = Gtk.MessageDialog(
                parent=self.main,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Invalid URL"
            )

            dialog.run()
            dialog.destroy()
            return 0 

        app.insertResourceDB(self.id, name, url) 

        button = Gtk.Button()
        button.set_label(name)
        button.connect("clicked", self.visitURL, url)
        button.set_size_request(random.randint(0, 30), random.randint(30, 80))
        container = random.randint(1, 3)
        if container == 1:
            self.vbox1.pack_start(button, False, False, random.randint(5, 25))
            self.vbox1.show_all()
        if container == 2:
            self.vbox2.pack_start(button, False, False, random.randint(5, 25))
            self.vbox2.show_all()
        if container == 3:
            self.vbox3.pack_start(button, False, False, random.randint(5, 25))
            self.vbox3.show_all()

        name_input.set_text('')
        url_input.set_text('')

        projectPanel.refreshApp(self.main, '')


    
    def display(self):
        window = Gtk.ScrolledWindow()
        window.set_size_request(0, 250)

        box = Gtk.Box()
        box.set_halign(Gtk.Align.CENTER)

        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        box.pack_start(self.vbox1, False, True, random.randint(50, 90))
        box.pack_start(self.vbox2, False, True, random.randint(50, 90))
        box.pack_start(self.vbox3, False, True, random.randint(50, 90))

        data = app.getResources(self.id)

        for i in data:
            name = i[1]
            url = i[2]

            button = Gtk.Button()
            button.set_label(name)
            button.connect("clicked", self.visitURL, url)
            button.set_size_request(random.randint(0, 30), random.randint(30, 100))
            container = random.randint(1, 3)
            if container == 1:
                self.vbox1.pack_start(button, False, False, random.randint(5, 25))
            if container == 2:
                self.vbox2.pack_start(button, False, False, random.randint(5, 25))
            if container == 3:
                self.vbox3.pack_start(button, False, False, random.randint(5, 25))

        window.add(box)

        return window

    def visitURL(self, button, url):
        try:
            os.system(f"firefox '{url}'")
        except:
            os.system(f"google-chrome '{url}'")

    
    def clearResource(self, button):
        app.clearResource(self.id)
        projectPanel.refreshApp(self.main, '')



    
# Function - varify
# This function varify the user info to prevent unauthorized access to data
def varify():
    try:
        if(app.varify(uname, pword)==False):
            exit()
    except:
        exit()

# Function - main
# This runs the app
def main():
    login = Login() # When the app runs, show the login window
    Gtk.main()
    

if __name__ == "__main__":
    main()

