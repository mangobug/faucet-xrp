from django.forms import CharField, DateInput, FileField, Form, ModelForm, Textarea, TextInput, ValidationError

from xrp.course.models import Course, Forum


class AddForumForm(Form):
    """
    Add new Forum
    """
    title = CharField(max_length=100)
    uploads = FileField(required = True)

    def clean_uploads(self):
        uploads = self.cleaned_data['uploads']
        ext = uploads.name.split('.')[-1]
        if ext == 'pdf' or ext == 'webm':
            return uploads
        else:
            raise ValidationError("Not a valid upload file")


class AddCourseForm(ModelForm):
    """
    Add new Course
    """
    class Meta:
        model = Course
        exclude = ['date_deleted', 'user']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title'}),
            'code': TextInput(attrs={'placeholder': 'Course Code'}),
            'description': Textarea(attrs={'placeholder': 'Course Description', 'rows': 4}),
            'start_date': DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'end_date': DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }


class AddVideoForm(Form):
    """
    Add new Video
    """
    title = CharField(max_length=100)
    uploads = FileField(required = True)

    def clean_uploads(self):
        uploads = self.cleaned_data['uploads']
        ext = uploads.name.split('.')[-1]
        if ext == 'webm':
            return uploads
        else:
            raise ValidationError("Not a valid video file. Only .webm is accepted")


class AddPdfForm(Form):
    """
    Add new Video
    """
    title = CharField(max_length=100)
    uploads = FileField(required = True)

    def clean_uploads(self):
        uploads = self.cleaned_data['uploads']
        ext = uploads.name.split('.')[-1]
        if ext == 'pdf':
            return uploads
        else:
            raise ValidationError("Not a valid pdf file")
