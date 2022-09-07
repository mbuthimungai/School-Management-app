from kivy.app import App

import mysql.connector
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.textfield import MDTextField

from signup import SignUp
from Login import Login
from admin_dashboard import AdminDashboardUpdate
from add_teacher_admin import AddTeacherAdmin
from retrieve_teacher_data import TeacherData
from delete import DeleteT
from update_passwd import UpdatePasswd
from add_stud_admin import AddStudentAdmin
from retrieve_student import RetrieveStudent

Window.clearcolor = (240 / 255, 240 / 255, 240 / 255, 1)

Window.size = (320, 600)

sign_up = SignUp()
login_ = Login()
# teacher_data = TeacherData()
add_teacher = AddTeacherAdmin()


class SchoolApp(MDApp):
    # def build(self):
    #     self.theme_cls.theme_style = "Light"
    #     self.title = "School App"
    #     # return

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.title = "School App"
        self.screen_manager = ScreenManager()
        # Heroes Screen
        self.first_page = FirstPage()
        screen = Screen(name="FirstScreen")
        screen.add_widget(self.first_page)
        self.screen_manager.add_widget(screen)
        # sign up
        self.second_page = SignUpPage()
        screen = Screen(name="SecondScreen")
        screen.add_widget(self.second_page)
        self.screen_manager.add_widget(screen)
        # login
        self.third_page = LoginAdminPage()
        screen = Screen(name="ThirdScreen")
        screen.add_widget(self.third_page)
        self.screen_manager.add_widget(screen)
        # Administrators Dashboard
        self.fourth_page = AdministratorPage()
        screen = Screen(name="FourthScreen")
        screen.add_widget(self.fourth_page)
        self.screen_manager.add_widget(screen)
        # Administrator Teachers Page
        self.fifth_page = AdministratorTeachersPage()
        screen = Screen(name="FifthScreen")
        screen.add_widget(self.fifth_page)
        self.screen_manager.add_widget(screen)
        # Administrator Add Teacher
        self.sixth_page = AdministratorAddTeacher()
        screen = Screen(name="SixthScreen")
        screen.add_widget(self.sixth_page)
        self.screen_manager.add_widget(screen)
        # Administrator View Screen
        self.seventh_screen = AdministratorViewTeacher()
        screen = Screen(name="SeventhScreen")
        screen.add_widget(self.seventh_screen)
        self.screen_manager.add_widget(screen)
        self.eighth_screen = AdministratorStudentPage()
        screen = Screen(name="EighthScreen")
        screen.add_widget(self.eighth_screen)
        self.screen_manager.add_widget(screen)
        self.nineth_screen = AdministratorAddStudent()
        screen = Screen(name="NinethScreen")
        screen.add_widget(self.nineth_screen)
        self.screen_manager.add_widget(screen)
        self.tenth_screen = AdministratorViewStudent()
        screen = Screen(name="TenthScreen")
        screen.add_widget(self.tenth_screen)
        self.screen_manager.add_widget(screen)
        return self.screen_manager


class FirstPage(BoxLayout):
    def change_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "SecondScreen"


class SignUpPage(BoxLayout):
    """This is class is also concerned with creating a user interface from where the user
    enters the sign in credentials"""
    text_btn_sign_up = StringProperty("Show")
    text_btn_confirm = StringProperty("Show")
    u_name_txt_ = StringProperty("")
    p_num_txt_ = StringProperty("")
    email_txt_ = StringProperty("")
    passwd_main_ = StringProperty("")
    confirm_passwd = StringProperty("")
    title_pop_box = StringProperty("")
    label_pop_box = StringProperty("")
    dialog_response = None
    dialog_passwd = None
    item_1_txt = ""
    item_1_img = ""
    item_2_txt = ""
    item_2_img = ""
    item_3_txt = ""
    item_3_img = ""
    item_4_txt = ""
    item_4_img = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_to_login_screen(self):
        school_app.screen_manager.current = "ThirdScreen"

    def toggle_visibility(self):
        """Responsible for toggle effect when user wants to view the password
        enters in the text field"""
        if self.ids.text_input_password_sign_up.password:
            self.ids.md_icon_3.icon = "eye"
            self.ids.text_input_password_sign_up.password = False
        elif not self.ids.text_input_password_sign_up.password:
            self.ids.md_icon_3.icon = "eye-off"
            self.ids.text_input_password_sign_up.password = True

    def toggle_visibility_confirm(self):
        """Responsible for toggle effect when user wants to view the password
                enters in the text field"""
        if self.ids.text_input_confirm_password_sign_up.password:
            self.ids.md_icon_2.icon = "eye"
            self.ids.text_input_confirm_password_sign_up.password = False
        elif not self.ids.text_input_confirm_password_sign_up.password:
            self.ids.md_icon_2.icon = "eye-off"
            self.ids.text_input_confirm_password_sign_up.password = True

    def get_details(self):
        """Responsible for getting the details entered by the user on the text field.
        """
        self.u_name_txt_ = self.ids.text_input_sign_up.text
        self.p_num_txt_ = str("+254") + self.ids.text_input_phone_number.text
        self.email_txt_ = self.ids.text_input_email_sign_up.text
        self.passwd_main_ = self.ids.text_input_password_sign_up.text
        self.confirm_passwd = self.ids.text_input_confirm_password_sign_up.text
        self.perform_insertion()

    def perform_insertion(self):
        """Responsible for performing insertion of the values entered on the text field into the database
         This function is responsible for calling some methods in the Sign Up class so as so pass the data to
         the respective methods in the sign up class"""
        self.passwd_main_ = self.passwd_main_.strip()
        self.confirm_passwd = self.confirm_passwd.strip()
        self.u_name_txt_ = self.u_name_txt_.strip()
        self.p_num_txt_ = self.p_num_txt_.strip()
        self.email_txt_ = self.email_txt_.strip()
        """The below if statement is responsible for calling the check_empty_fields() function which is for the sign 
        up class and the method is Responsible for checking whether there are any empty text fields in left by the 
        user in the sign up form. If user has left some text fields empty the function returns False otherwise True """
        if sign_up.check_empty_fields(self.u_name_txt_, self.p_num_txt_, self.email_txt_,
                                      self.passwd_main_,
                                      self.confirm_passwd):
            """
            The below if statement is executed if the above if returns True.
            This if statement calls the confirm_passwd_equals_main_passwd() from the
            Sign Up class and the confirm_passwd_equals_main_passwd() is for confirming 
            whether the password entered in the confirm password field
            actually matches the on entered in the password text fields. If password does  not match the
            function returns False else True 
            """
            if sign_up.confirm_passwd_equals_main_passwd(self.passwd_main_, self.confirm_passwd):
                """The below if statement is executed if the above if returns True. This if statement calls the 
                check_password() from the Sign Up class and the check_password() function Responsible for verifying 
                if the password entered by the user has the correct number of symbols, words and numbers. If the 
                passwords satisfies the fields the function returns True """
                if sign_up.check_password(self.passwd_main_):
                    sign_up.create_table()
                    sign_up.insert_into_administrators(self.u_name_txt_,
                                                       self.p_num_txt_,
                                                       self.email_txt_,
                                                       self.passwd_main_,
                                                       )
                    self.item_1_txt = "Account Created"
                    self.item_1_img = "images/check.png"
                    self.response_dialog()
                    school_app.screen_manager.transition = SlideTransition(direction="left")
                    school_app.screen_manager.current = "ThirdScreen"
                else:
                    self.item_1_txt = "Weak Password"
                    self.item_1_img = "images/exclamation-mark.png"
                    self.item_2_txt = "Numbers More than 3"
                    self.item_3_txt = "Characters More than 3"
                    self.item_4_txt = "Symbols More than 3"
                    if sign_up.count_num < 3:
                        self.item_2_img = "images/cancel.png"
                    else:
                        self.item_2_img = "images/check.png"
                    if sign_up.count_symbols < 3:
                        self.item_3_img = "images/cancel.png"
                    else:
                        self.item_3_img = "images/check.png"
                    if sign_up.count_chars < 3:
                        self.item_4_img = "images/cancel.png"
                    else:
                        self.item_4_img = "images/check.png"
                    self.response_passwd()

            else:
                self.item_1_txt = "Password Mismatch"
                self.item_1_img = "images/exclamation-mark.png"
                self.response_dialog()

        else:
            self.item_1_txt = "All Fields Required"
            self.item_1_img = "images/file.png"
            self.response_dialog()

    def prev_screen(self):
        """Responsible for changing the screen if the details entered by user are correct"""
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "FirstScreen"

    def response_dialog(self):
        """Responsible for creating a dialog to show the user if the details entered
        are in the correct format"""
        self.dialog_response = MDDialog(
            auto_dismiss=True,
            type="simple",
            items=[
                ResponseDialogContent(text=self.item_1_txt, source=self.item_1_img),

            ]
        ).open()

    def response_passwd(self):
        """Responsible for creating a dialog to show the user if the details entered
        are in the correct format"""
        self.dialog_passwd = MDDialog(
            auto_dismiss=True,
            type="simple",
            items=[
                ResponseDialogContent(text=self.item_1_txt, source=self.item_1_img),
                ResponseDialogContent(text=self.item_2_txt, source=self.item_2_img),
                ResponseDialogContent(text=self.item_3_txt, source=self.item_3_img),
                ResponseDialogContent(text=self.item_4_txt, source=self.item_4_img),
            ]
        ).open()


class LoginAdminPage(BoxLayout):
    """This class creates a user interface for the user
    to login"""
    dialog_change = None
    dialog_inputs = None
    dialog_response = None
    dialog_response_text = None
    dialog_response_img_path = None
    toggle_btn_txt_login = StringProperty("Show")
    u_name_txt_login = StringProperty("")
    u_passwd_txt_login = StringProperty("")
    lbl_txt = StringProperty("")
    pop_up_title = StringProperty("")

    def toggle_visibility(self):
        """Responsible for toggle effect when user wants to view the password
                enters in the text field"""
        if self.ids.txt_passwd_login_admin.password:
            self.ids.md_icon_1.icon = "eye"
            self.ids.txt_passwd_login_admin.password = False
        elif not self.ids.txt_passwd_login_admin.password:
            self.ids.md_icon_1.icon = "eye-off"
            self.ids.txt_passwd_login_admin.password = True

    def validate_user(self):
        """Responsible for taking the user data in the text fields
         and passing it to the Login class
        for validation"""
        self.u_name_txt_login = self.ids.txt_input_login_adm.text
        self.u_passwd_txt_login = self.ids.txt_passwd_login_admin.text
        if login_.identify_empty_input(self.u_name_txt_login, self.u_passwd_txt_login):
            if login_.user_validation(self.u_name_txt_login, self.u_passwd_txt_login):
                self.lbl_txt = "login successful"
                self.dialog_response_text = "Login Successfully"
                self.dialog_response_img_path = "images/check.png"
                self.response_dialog()
                school_app.screen_manager.transition = SlideTransition(direction="left")
                school_app.screen_manager.current = "FourthScreen"
            else:
                self.dialog_response_text = "Login Unsuccessful"
                self.dialog_response_img_path = "images/cancel.png"
                self.response_dialog()
        else:
            self.dialog_response_text = "All Fields Required"
            self.dialog_response_img_path = "images/file.png"
            self.response_dialog()

    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "SecondScreen"

    def change_passwd(self):
        self.dialog_change = MDDialog(
            auto_dismiss=False,
            title="change password?",
            type='custom',
            # content_cls=DialogContent(),
            buttons=[
                MDFlatButton(text="No", on_release=self.close_dialog_1),
                MDFlatButton(text="Yes", on_release=self.swipe_dialog)
            ],
        )
        self.dialog_change.open()

    def swipe_dialog(self, obj):
        self.dialog_change.dismiss()
        self.change_passwd_dialog()

    def close_dialog_2(self, obj):
        self.dialog_inputs.dismiss()

    def close_dialog_1(self, obj):
        self.dialog_change.dismiss()

    def update_btn(self, obj):
        update_passwd = UpdatePasswd()
        update_passwd.update_details(self.dialog_inputs.content_cls.ids.old_passwd.text,
                                     self.dialog_inputs.content_cls.ids.new_passwd.text,
                                     self.dialog_inputs.content_cls.ids.user_name_.text)
        self.dialog_inputs.dismiss()
        self.dialog_response_text = "Successfully Updated"
        self.dialog_response_img_path = "images/check.png"
        self.response_dialog()


    def show_successful_update(self):
        pass

    def change_passwd_dialog(self):
        self.dialog_inputs = MDDialog(
            auto_dismiss=False,
            title="Password",
            type="custom",
            content_cls=DialogContent(),
            buttons=[
                MDRaisedButton(text="update", on_release=self.update_btn),
                MDFlatButton(text="cancel", on_release=self.close_dialog_2)
            ]
        )
        self.dialog_inputs.open()

    def response_dialog(self):
        """Responsible for creating a response in form of a dialog
         when user enters his or her credentials"""
        self.dialog_response = MDDialog(
            auto_dismiss=True,
            type="simple",
            items=[
                ResponseDialogContent(text=self.dialog_response_text, source=self.dialog_response_img_path)
            ]
        ).open()


class DialogContent(BoxLayout):
    name = ObjectProperty()
    pass


class ResponseDialogContent(OneLineAvatarListItem):
    divider = None
    source = StringProperty()
    pass


class AdministratorPage(BoxLayout):
    admin_num = StringProperty("0")
    teacher_num = StringProperty("")
    student_num = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        admin_dashboard = AdminDashboardUpdate()
        self.admin_num = str(admin_dashboard.number_of_rows)
        self.teacher_num = str(admin_dashboard.number_of_rows_teachers)
        self.student_num = str(admin_dashboard.number_of_rows_students)

    def change_window_teacher_admin(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "FifthScreen"

    def change_window_student_admin(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "EighthScreen"


class AdministratorTeachersPage(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_event_btn(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "SixthScreen"

    def view_event_btn(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "SeventhScreen"

    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "FourthScreen"


class AdministratorAddTeacher(BoxLayout):
    lbl_pop_label = StringProperty("")
    pop_title = StringProperty("")
    dialog_response = None
    txt_ = None
    source_img = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_teacher = AddTeacherAdmin()

    def add_teacher_admin_btn(self):
        if self.add_teacher.check_empty_field(self.ids.text_input_u_name_teacher_admin.text,
                                              self.ids.text_input_f_name_teacher_admin.text,
                                              self.ids.text_input_l_name_teacher_admin.text,
                                              self.ids.text_input_p_number_teacher_admin.text):
            try:
                self.add_teacher.insert_into_teachers(self.ids.text_input_u_name_teacher_admin.text,
                                                      self.ids.text_input_f_name_teacher_admin.text,
                                                      self.ids.text_input_l_name_teacher_admin.text,
                                                      "254" + self.ids.text_input_p_number_teacher_admin.text)
            except mysql.connector.errors.IntegrityError:
                self.txt_ = self.ids.text_input_u_name_teacher_admin.text + " " + "already exists"
                self.source_img = "images/exclamation-mark.png"
                self.response_dialog()
            else:
                self.pop_title = self.ids.text_input_f_name_teacher_admin.text + " " + \
                                 self.ids.text_input_l_name_teacher_admin.text
                self.txt_ = "Successfully added"
                self.source_img = "images/check.png"
                self.response_dialog()
                self.add_teacher = AddTeacherAdmin()
                # self.add_teacher_admin_btn()
        else:
            self.txt_ = "All Fields Required"
            self.pop_title = "Missing Fields"
            self.source_img = "images/cancel.png"
            self.response_dialog()

    def response_dialog(self):
        self.dialog_response = MDDialog(
            auto_dismiss=True,
            title=self.pop_title,
            type="simple",
            items=[
                ResponseDialogContent(text=self.txt_, source=self.source_img)
            ]
        ).open()

    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "FifthScreen"


class AdministratorViewTeacher(BoxLayout):
    dialog = None
    teacher_details = []
    this_class = None
    dialog_delete = None
    teacher_data_vals = None
    table = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teacher_data = TeacherData()
        self.teacher_data_vals = self.teacher_data.get_teacher_vals()
        self.create_table(self.teacher_data_vals)
        self.table.bind(on_row_press=self.on_row_press)

    def create_table(self, data):
        self.table = MDDataTable(
            pos_hint={"center_": .5, "center_y": .5},
            size_hint=(1, .6),
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",
            # background_color_header=get_color_from_hex("#65275d"),
            # background_color_cell=get_color_from_hex("#451938"),
            # background_color_cell=[1,0,0,1],
            # background_color_selected_cell=get_color_from_hex("e4514f"),
            column_data=[
                ("User Name", dp(30)),
                ("First Name", dp(30)),
                ("Last Name", dp(30)),
                ("Phone Number", dp(30)),
                ("Email Address", dp(30)),
            ],
            row_data=data
        )
        self.add_widget(self.table)

    def on_row_press(self, instance_table, instance_row):
        """Responsible for getting the instance of the object
        which is select on the table. Th instance is then sent to the
        DeleteT class through teacher_details() function which takes the
        parameter of the instance selected."""
        self.teacher_details = []
        start_index, end_index = \
            instance_row.table.recycle_data[instance_row.index]["range"]

        for i in range(start_index, end_index):
            self.teacher_details.append(instance_row.table.recycle_data[i]["text"])

        self.show_dialog()
        self.teacher_data = TeacherData()
        # self.this_class = AdministratorViewTeacher()

        self.teacher_data_vals = self.teacher_data.get_teacher_vals()

        # self.table.row_data = self.teacher_data_vals
        self.remove_widget(self.table)
        self.create_table(self.teacher_data_vals)
        # self.add_widget(self.table)

        # self.add_widget(self.table)

    def show_dialog(self):
        """Responsible for displaying a dialog box asking the user to
        whether continue with the deletion or not
        """
        if not self.dialog:
            self.dialog = MDDialog(
                title=f"Delete {self.teacher_details[1]} {self.teacher_details[2]}",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        on_press=self.close_dialog
                    ),
                    MDFlatButton(
                        text="DELETE",
                        theme_text_color="Custom",
                        on_press=self.delete_operation
                    )
                ]
            )

        self.dialog.open()

    def successful_deletion(self):
        """Responsible for displaying a dialog box if the deletion
                of the instance was successful"""
        if not self.dialog_delete:
            self.dialog_delete = MDDialog(
                title="Deleted Successfully",
                items=[
                    Item(text="hello", source="images/check.png")
                ],
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_press=self.close_delete_dialog
                        # text_color=self.theme_cls.primary_color,
                    )
                ]
            )
        self.dialog_delete.open()

    def delete_operation(self, inst):
        delete_t = DeleteT()
        delete_t.delete_teacher(self.teacher_details[0])
        self.dialog.dismiss()
        self.successful_deletion()

    def close_dialog(self, widget):
        self.dialog.dismiss()

    def close_delete_dialog(self, widget):
        self.dialog_delete.dismiss()

    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "FifthScreen"


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class AdministratorStudentPage(BoxLayout):
    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "FourthScreen"

    def go_to_add_student(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "NinethScreen"

    def go_to_view_student(self):
        school_app.screen_manager.transition = SlideTransition(direction="left")
        school_app.screen_manager.current = "TenthScreen"


class AdministratorViewStudent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.retrieve_student = RetrieveStudent()
        self.table = MDDataTable(
            column_data=[
                ("Reg No", dp(30)),
                ("First Name", dp(30)),
                ("Last Name", dp(30)),
                ("City", dp(30))
            ],
            row_data=
            self.retrieve_student.get_student_details(),
            size_hint=(1, .6),
            use_pagination=True,
            pos_hint={"center_x": .5, "center_y": .5}
        )
        self.add_widget(self.table)

    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "EighthScreen"


class AdministratorAddStudent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_add = AddStudentAdmin()
        self.dialog = None

    def add_student(self):
        self.student_add = AddStudentAdmin()
        adm_no = self.ids.stud_adm_admin.text
        f_name = self.ids.stud_f_name_admin.text
        l_name = self.ids.stud_l_name_admin.text
        city = self.ids.stud_city_admin.text
        if (adm_no,) in self.student_add.check_id_exists():
            self.dialog_err()
        else:
            self.student_add.add_function(adm_no, f_name, l_name, city)
        # self.student_add = AddStudentAdmin()

    def dialog_err(self):
        self.dialog = MDDialog(
            title=f"{self.ids.stud_adm_admin.text}",
            text="already exists",
            auto_dismiss=True,
            radius=[20, 7, 20, 7]
        ).open()

    def prev_screen(self):
        school_app.screen_manager.transition = SlideTransition(direction="right")
        school_app.screen_manager.current = "EighthScreen"


if __name__ == "__main__":
    school_app = SchoolApp()
    school_app.run()
