from django.forms import CharField, Form, PasswordInput, TextInput, FileField

class Loginform(Form):
    username = CharField(label="Username", max_length=100)
    username.widget = TextInput(attrs={'class': "form-control,text-left",})
    password = CharField(widget=PasswordInput())
    password.widget = PasswordInput(attrs={'class': "form-control,text-left",})

class NewElementForm(Form):
    name = CharField(label="Name", max_length=30)
    name.widget = TextInput(attrs={'class': "form-control",})
    code = CharField(label="Code", max_length=10)
    code.widget = TextInput(attrs={'class': "form-control",})

class UploadFileForm(Form):
    description = CharField(label="Description", max_length=40)
    description.widget = TextInput(attrs={'class': "form-control",})
    file = FileField()

class NewVendorForm(Form):
    company = CharField(label="Company name", max_length=20)
    company.widget = TextInput(attrs={'class': "form-control",})
    address = CharField(label="Address", max_length=100)
    address.widget = TextInput(attrs={'class': "form-control",})