from django import forms
from pdf.models import UploadedFile

class ChooseFileForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ChooseFileForm, self).__init__(*args, **kwargs)
        user_files = UploadedFile.objects.filter(user_id=user)
        choices = [(file.id, file.file.name) for file in user_files]
        self.fields['file_choice'] = forms.ChoiceField(choices=choices)