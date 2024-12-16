from django.forms import CharField, Form, PasswordInput, TextInput


class Loginform(Form):
    username = CharField(label="Username", max_length=100)
    username.widget = TextInput(attrs={'class': "form-control",})
    password = CharField(widget=PasswordInput())
    password.widget = PasswordInput(attrs={'class': "form-control",})