from main import MyDMS # This provides all the main functionalities and database
from sys import argv

# Modules for GUI design
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk

# CSS stylesheet
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

a{
    color: white;
}
"""


app = MyDMS() # Create an object of MyDMS class
unam = '' # A global variable
# Note: the username (GitHub username) is always unique

class Login(Gtk.Window): # Login Window
    def __init__(self):
        # Create window
        Gtk.Window.__init__(self) 
        # Initialise window
        self.set_default_size(360,500) 
        self.set_border_width(5)
        self.set_title("GNOME Project Manager")
        # Create content
        window = self.loginWindow()
        self.add(window) # add content to the window

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
                self,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Wrong username / password! Please try again!",
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
                self.register,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0
        elif(pword1 != pword2):
            dialog = Gtk.MessageDialog(
                self.register,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Please make sure your password matches!",
            )
            dialog.run()
            dialog.destroy()
            return 0
        elif(len(pword1) <= 6): # Password must be longer than 6 chars (for security)
            dialog = Gtk.MessageDialog(
                self.register,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Your password is too short! (length > 6)",
            )
            dialog.run()
            dialog.destroy()
            return 0
        # Register the account and save the data into `main.db`
        app.register(uname, pword1, name, email, github)
        try:
            # Get all the public (open source) repo of the user with his/her GitHub account (username)
            # Note: This requires internet access! An `ApiError` will be raised
            app.createRepoDB(uname)
            dialog = Gtk.MessageDialog(
                self.register,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                "Registered! Please restart the app!",
            )
        except:
            dialog = Gtk.MessageDialog(
                self.register,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                """
                Registered! Please restart the app!
                Note: Failed loading repo data (this requires Internet access).
                """,
            )
        dialog.run()
        dialog.destroy()
        # Close the app
        self.destroy()

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
                    self.window,
                    0,
                    Gtk.MessageType.INFO,
                    Gtk.ButtonsType.OK,
                    f"Your password is: {password}",
            )
        else:
            dialog = Gtk.MessageDialog(
                self.window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                f"Incorrect email address",
            )
        dialog.run()
        dialog.destroy()
        self.window.destroy()


class MyWindow(Gtk.Window): # Main app
    def __init__(self):
        Gtk.Window.__init__(self)
        # Set stylesheet
        cssprovider = Gtk.CssProvider()
        cssprovider.load_from_data(CSS)
        screen = Gdk.Screen.get_default()
        stylecontext = Gtk.StyleContext()
        stylecontext.add_provider_for_screen(screen, cssprovider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.set_default_size(800,600)
        # Create headbar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = f"GNOME Project Manager - {uname}"
        # Child element of the headbar - about button linked to `self.about`
        button = Gtk.Button()
        button.connect("clicked", self.about)
        icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)
        # Set the titlebar of the window to hb
        self.set_titlebar(hb)
        # Create Notebook
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        # Add CSS class to Notebook
        notebook_style = notebook.get_style_context()
        notebook_style.add_class("myNotebook")
        # Create notebook page(1) using `self.home()` method        
        page1 = self.home()
        # Add CSS class to page1
        home_style = page1.get_style_context()
        home_style.add_class("home")
        # Set the name of the page as `Home`
        home = Gtk.Label(label="\nHome\n")
        home.set_xalign(0)
        notebook.append_page(page1, home)
        # Create notebook page(2) using `self.repo` method
        page2 = self.repo()
        # Add CSS class to page2
        page2_style = page2.get_style_context()
        page2_style.add_class("home")
        # Set the name of the page as `My Repos`
        title = Gtk.Label(label="\nMy Repos\n")
        title.set_xalign(0)
        notebook.append_page(page2, title)
        # Add notebook widget to the main window
        self.add(notebook)

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

    # Function: create home page
    def home(self):
        # Create window (vertical box)
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
        # Get data from `main.db` using MyDMS class
        for i in app.getData(uname):
            self.data = i
        self.repo_count = app.getRepoCount(uname)
        # Set title of the window
        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> Welcome Back, {self.data[4]}! </span>")
        title.set_margin_top(40)
        window.pack_start(title, False, True, 0)  
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
        edit = self.editProfile()
        stack.add_titled(edit, "edit", "Edit Profile")
        # Create a stack_switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        # Add the stack and stack_switcher widgets to the container
        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(stack, True, True, 0)   
        # Add the container to the window
        window.pack_start(vbox, True, True, 0)
        return window

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
        my_profile.pack_start(listbox, False, True, 0)
        return my_profile

    # Function: create ListBox and ListBoxRows with given data
    def makeProfile(self, item, content):
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
            if(app.url_validate(str(content[i]))):
                content_label.set_markup(
                    f'<a href="{content[i]}">{content[i]}</a>'
                )
            else:
                content_label.set_label(str(content[i]))
            # Add both label and content to the same row
            hbox.pack_start(item_label, True, True, 10)
            hbox.pack_start(content_label, False, True, 10)
            # Add the row to listbox
            listbox.add(row)
        return listbox
    
    def editProfile(self):
        # Create form
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        form.set_margin_top(30)
        name = Gtk.Box(spacing=8)
        name_label = Gtk.Label()
        name_label.set_markup("<b>Name*    </b>")
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("Name*")

        name.pack_start(name_label, False, True, 40)
        name.pack_start(name_input, True, True, 40)

        form.pack_start(name, False, True, 0)
        # Get the email
        email = Gtk.Box(spacing=8)
        email_label = Gtk.Label()
        email_label.set_markup("<b>Email*     </b>")
        email_input = Gtk.Entry()
        email_input.set_placeholder_text("Email Address")

        email.pack_start(email_label, False, True, 40)
        email.pack_start(email_input, True, True, 40)

        form.pack_start(email, False, True, 0)
        # Get the GitHub URL
        github = Gtk.Box(spacing=8)
        github_label = Gtk.Label()
        github_label.set_markup("<b>URL         </b>")
        github_input = Gtk.Entry()
        github_input.set_placeholder_text("GitHub Page URL")

        github.pack_start(github_label, False, True, 40)
        github.pack_start(github_input, True, True, 40)

        form.pack_start(github, False, True, 0)

        location = Gtk.Box(spacing=8)
        location_label = Gtk.Label()
        location_label.set_markup("<b>Location </b>")
        location_input = Gtk.Entry()
        location_input.set_placeholder_text("Location")

        location.pack_start(location_label, False, True, 40)
        location.pack_start(location_input, True, True, 40)

        form.pack_start(location, False, True, 0)

        company = Gtk.Box(spacing=8)
        company_label = Gtk.Label()
        company_label.set_markup("<b>Company</b>")
        company_input = Gtk.Entry()
        company_input.set_placeholder_text("Company")

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
                self,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Fields with * can not be empty!",
            )
            dialog.run()
            dialog.destroy()
            return 0

        try:
            app.updateData(uname, name, email, github, location, company)
            dialog = Gtk.MessageDialog(
                self,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                '''
                Updated!
                Please restart the app to load new data!
                ''',
            )
            dialog.run()
            dialog.destroy()
            self.destroy()
            
        except:
            dialog = Gtk.MessageDialog(
                self,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Failed updating data!",
            )
            dialog.run()
            dialog.destroy()
    # Function: create repo window for My Repos page 
    def repo(self):
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)

        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> {self.data[0]}'s Repos! </span>")
        title.set_margin_top(40)
        window.pack_start(title, False, True, 0)  

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        repo_window = self.createRepoWindow()

        stack.add_titled(repo_window, "repo", "Repos")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(stack, False, True, 0)

        window.pack_start(vbox, True, True, 0)

        return window

    def createRepoWindow(self):
        my_repo = Gtk.Box(spacing=6)

        self.data = []
        
        for i in app.getRepoData(uname):
            self.data.append(i)
        
        listbox = self.makeRepo(self.data)
        my_repo.pack_start(listbox, True, True, 0)
        return my_repo
    
    # Function: create ListBox and ListBoxRows with given data
    def makeRepo(self, data):
        # Create listbox
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
        url_label.set_markup("<b>____________________Repo URL__________________</b>")
        date_label = Gtk.Label()
        date_label.set_markup("<b>Repo Date</b>")
        forks_label = Gtk.Label()
        forks_label.set_markup("<b>Forks</b>")
        status_label = Gtk.Label(label="Status")
        status_label.set_markup("<b>Status</b>")

        hbox.pack_start(id_label, True, True, 5)
        hbox.pack_start(name_label, True, True, 5)
        hbox.pack_start(url_label, True, True, 5)
        hbox.pack_start(date_label, True, True, 5)
        hbox.pack_start(forks_label, True, True, 5)
        hbox.pack_start(status_label, True, True, 5)

        listbox.add(row)
        
        # Create rows for all data provided
        for i in range(len(data)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(spacing=20)
            row.add(hbox)
            for j in range(len(data[i])-2):
                label = Gtk.Label()

                if (j == 0):
                    label.set_xalign(0)

                if(app.url_validate(str(data[i][j]))):
                    label.set_markup(f'<a href="{data[i][j]}">{data[i][j]}</a>')
                else:
                    label.set_markup(str(data[i][j]))
                hbox.pack_start(label, True, True, 5)

            self.toggle = Gtk.ToggleButton(label="done")
            status = data[i][-2]
            id = data[i][0]
            if(status == 1):
                self.toggle.set_active("True")
            self.toggle.connect("toggled", self.toggleSwitch, status, id) 
            hbox.pack_end(self.toggle, False, True, 5)
            # Add the row to listbox
            listbox.add(row)
        return listbox


    def toggleSwitch(self, toggle, status, id):
        if (status == 1):
            app.toggle(0, id)
        else:
            app.toggle(1, id)


def main():
    login = Login() # When the app runs, show the login window
    login.connect("destroy", Gtk.main_quit)
    login.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
