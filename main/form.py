# -*- coding: utf-8 -*-
from django import forms


class UploadResume(forms.Form):
    path = forms.FileField(label='pdfでのアップロードをお願いします',
                           required=False)
