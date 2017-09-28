from django import forms

class Registration_Form(forms.Form):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label="Birthday", widget=forms.SelectDateWidget(years=range(1920, 2016), attrs={'class': 'form-control'}))

class Login_Form(forms.Form):
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class Add_Book_Form(forms.Form):
    book_title = forms.CharField(label="Book Title")
class Add_Author_Form(forms.Form):
    new_author = forms.CharField(label="Or add a new author", required=False)
class Add_Review_Form(forms.Form):
    choices = (('-', '-'), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    body = forms.CharField(label="Add a Review", widget=forms.Textarea(attrs={'class': 'form-control'}))
    rating = forms.ChoiceField(choices=choices)