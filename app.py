from main import MyDMS
import re

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio, Gdk

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


app = MyDMS() # This provides functionalities
unam = ''

class Login(Gtk.Window): # Login Window
    def __init__(self):
        Gtk.Window.__init__(self) # Create window
        self.set_default_size(400,500)
        self.set_border_width(5)
        self.set_title("GNOME Project Manager")

        window = self.loginWindow() 
        self.add(window)


    def loginWindow(self): # Create contents
        self.window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        label = Gtk.Label()
        label.set_markup("<span size='xx-large'>Login</span>")
        label.set_halign(Gtk.Align.CENTER)
        self.window.pack_start(label, True, True, 0)

        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        form.set_halign(Gtk.Align.CENTER)
        form.set_size_request(250, 300)
        form.set_margin_right(10)

        username = Gtk.Box(spacing=5)

        uname_label = Gtk.Label()
        uname_label.set_markup("<b>Username</b>")
        uname_input = Gtk.Entry()
        uname_input.set_placeholder_text("Username")

        username.pack_start(uname_label, True, True, 0)
        username.pack_start(uname_input, True, True, 0)

        form.pack_start(username, False, True, 0)

        password = Gtk.Box(spacing=8)

        pword_label = Gtk.Label()
        pword_label.set_markup("<b>Password</b>")
        pword_input = Gtk.Entry()
        pword_input.set_visibility(False)
        pword_input.set_placeholder_text("Password")

        password.pack_start(pword_label, True, True, 0)
        password.pack_start(pword_input, True, True, 0)

        form.pack_start(password, False, True, 0)
        
        submit = Gtk.Button(label="Login")
        submit.connect("clicked", self.getInfo, uname_input, pword_input)

        form.pack_start(submit, False, True, 0)

        forgot = Gtk.Button(label="Forgot Password")
        forgot.connect("clicked", self.forgotPW)

        form.pack_end(forgot, False, True, 0)

        register = Gtk.Button(label="Register")
        register.set_margin_bottom(10)
        register.connect("clicked", self.createAccount)

        form.pack_end(register, False, True, 0)

        self.window.pack_start(form, True, True, 0)

        return self.window


    def createAccount(self, button):
        self.register = Gtk.Window(title="GNOME Project Manager - Create Account")
        self.register.set_default_size(300, 500)

        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        form.set_halign(Gtk.Align.CENTER)
        form.set_size_request(250, 500)
        form.set_margin_right(10)

        label = Gtk.Label()
        label.set_markup("<span size='x-large'>Register</span>")
        label.set_size_request(100, 100)

        form.pack_start(label, False, True, 0)


        username = Gtk.Box(spacing=5)
        username.set_valign(Gtk.Align.START)

        ulabel = Gtk.Label()
        ulabel.set_markup("<b>Username*</b>")
        uname_input = Gtk.Entry()
        uname_input.set_placeholder_text("Username")

        username.pack_start(ulabel, True, True, 0)
        username.pack_start(uname_input, True, True, 0)

        form.pack_start(username, False, True, 0)

        password1 = Gtk.Box(spacing=8)

        plabel1 = Gtk.Label()
        plabel1.set_markup("<b>Password*</b>")
        pword_input1 = Gtk.Entry()
        pword_input1.set_visibility(False)
        pword_input1.set_placeholder_text("Password")

        password1.pack_start(plabel1, True, True, 0)
        password1.pack_start(pword_input1, True, True, 0)

        password2 = Gtk.Box(spacing=8)
        plabel2 = Gtk.Label()
        pword_input2 = Gtk.Entry()
        pword_input2.set_visibility(False)
        pword_input2.set_placeholder_text("Confirm")

        password2.pack_start(pword_input2, True, True, 0)

        form.pack_start(password1, False, True, 0)
        form.pack_start(password2, False, True, 0)

        linebreak = Gtk.Label()
        linebreak.set_text("----------------------------------------------------------------")
        form.pack_start(linebreak, False, True, 0)

        name = Gtk.Box(spacing=8)
        nlabel = Gtk.Label()
        nlabel.set_markup("<b>Name*</b>")
        name_input = Gtk.Entry()
        name_input.set_placeholder_text("First Name")

        name.pack_start(nlabel, True, True, 0)
        name.pack_start(name_input, True, True, 0)

        form.pack_start(name, False, True, 0)

        email = Gtk.Box(spacing=8)
        elabel = Gtk.Label()
        elabel.set_markup("<b>Email*</b>")
        email_input = Gtk.Entry()
        email_input.set_placeholder_text("Email Address")

        email.pack_start(elabel, True, True, 0)
        email.pack_start(email_input, True, True, 0)

        form.pack_start(email, False, True, 0)

        github = Gtk.Box(spacing=8)
        glabel = Gtk.Label()
        glabel.set_markup("<b>Github</b>")
        github_input = Gtk.Entry()
        github_input.set_placeholder_text("Github Page")

        github.pack_start(glabel, True, True, 0)
        github.pack_start(github_input, True, True, 0)

        form.pack_start(github, False, True, 0)

        
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

        self.register.add(form)

        self.register.show_all()


    def getInfo(self, button, uname_input, pword_input):
        global uname
        uname = uname_input.get_text()
        pword = pword_input.get_text()
    
        if(app.varify(uname, pword)):
            self.set_visible(False)
            win = MyWindow()
            win.connect("destroy", Gtk.main_quit)
            win.show_all()

        else:
            dialog = Gtk.MessageDialog(
                self,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL,
                "Wrong username / password! Please try again!",
            )
            dialog.run()
            dialog.destroy()


    def recordInfo(self, button, uname_input, pword_input1, pword_input2, name_input, email_input, github_input):
        uname = uname_input.get_text()
        pword1 = pword_input1.get_text()
        pword2 =  pword_input2.get_text()
        name =  name_input.get_text()
        email =  email_input.get_text()
        github =  github_input.get_text()

        if (github == ''):
            github = None

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

        app.register(uname, pword1, name, email, github)

        dialog = Gtk.MessageDialog(
                self.register,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                "Registered! Please restart the app!",
            )
        dialog.run()
        dialog.destroy()

        self.destroy()

    
    def forgotPW(self, button):
        self.window = Gtk.Window()
        self.window.set_title("GNOME Project Manager - Forgot Password")
        self.window.set_default_size(350, 200)

        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        form.set_halign(Gtk.Align.CENTER)
        form.set_size_request(300, 200)

        title = Gtk.Label()
        title.set_markup("<span size='x-large'>Recover Password</span>")
        title.set_size_request(100, 100)
        form.pack_start(title, False, True, 0)

        input = Gtk.Box()
        input_label = Gtk.Label(label="Registerd Email")
        input_field = Gtk.Entry()
        input_field.set_placeholder_text("Email")

        input.pack_start(input_label, False, True, 15)
        input.pack_start(input_field, False, True, 0)

        form.pack_start(input, False, True, 0)

        submit = Gtk.Button(label="Sumbit")
        submit.connect("clicked", self.recover, input_field)

        form.pack_start(submit, False, True, 0)

        self.window.add(form)
        self.window.show_all()


    def recover(self, button, input):
        email = input.get_text()
        password = app.recoverAccount(email)
        
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


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(800,500)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "GNOME Project Manager"

        button = Gtk.Button()
        button.connect("clicked", self.about)
        icon = Gio.ThemedIcon(name="dialog-information-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)

        self.set_titlebar(hb)

        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        
        cssprovider = Gtk.CssProvider()
        cssprovider.load_from_data(CSS)
        screen = Gdk.Screen.get_default()
        stylecontext = Gtk.StyleContext()
        stylecontext.add_provider_for_screen(screen, cssprovider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

        notebook_style = notebook.get_style_context()
        notebook_style.add_class("myNotebook")
        
        page1 = self.home()

        home_style = page1.get_style_context()
        home_style.add_class("home")

        home = Gtk.Label(label="\nHome\n")
        home.set_xalign(0)
        notebook.append_page(page1, home)

        page2 = Gtk.Box()
        page2.add(Gtk.Label(label="Placeholder"))

        title = Gtk.Label(label="\n------Placeholder------\n")
        title.set_xalign(0)

        page2_style = page2.get_style_context()
        page2_style.add_class("home")

        notebook.append_page(
            page2, title
        )

        self.add(notebook)


    def about(self, button):
        aboutdialog = Gtk.AboutDialog()

        author = ["MengZe"]
        copyright = "© MengZe 2020"
        version = "Version 1.0"

        aboutdialog.set_program_name("GNOME Project Manager")
        aboutdialog.set_authors(author)
        aboutdialog.set_copyright(copyright)
        aboutdialog.set_version(version)
        aboutdialog.set_website("https://github.com/openMengZe")
        aboutdialog.set_website_label("My GitHub")
        aboutdialog.set_title("About")
        aboutdialog.show_all()


    def home(self):
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)

        for i in app.getData(uname):
            self.data = i

        title = Gtk.Label()
        title.set_markup(f"<span size='xx-large'> Welcome Back, {self.data[0]}! </span>")
        title.set_margin_top(40)
        window.pack_start(title, False, True, 0)  

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_border_width(10)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        profile = self.profile()

        stack.add_titled(profile, "profile", "Profile")

        # Placeholder
        label = Gtk.Label()
        label.set_markup("<big>A fancy label</big>")
        stack.add_titled(label, "label", "A label")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(stack, True, True, 0)   

        window.pack_start(vbox, True, True, 0)

        return window

    
    def profile(self):
        my_profile = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        listbox = self.makeListRow(["Name:", "Email Address:", "Repos:", "GitHub URL:", "Register Date:"], [self.data[0], self.data[1], 0, self.data[2], self.data[3]])

        my_profile.pack_start(listbox, False, True, 0)

        return my_profile

    def makeListRow(self, item, content):
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        for i in range(len(item)):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            row.add(hbox)

            item_label = Gtk.Label(label=('\n' + item[i] + '\n'), xalign=0)
            content_label = Gtk.Label()

            regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            if(re.match(regex, str(content[i])) is not None):
                content_label.set_markup(
                    f'<a href="{content[i]}">{content[i]}</a>'
                )
            else:
                content_label.set_label(str(content[i]))

            hbox.pack_start(item_label, True, True, 0)
            hbox.pack_start(content_label, False, True, 0)
            listbox.add(row)

        return listbox
        

def main():
    login = Login() # When the app runs, show the login window
    login.connect("destroy", Gtk.main_quit)
    login.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
