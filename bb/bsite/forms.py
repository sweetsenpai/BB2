from django import forms


class SettingsForm(forms.Form):
    name = forms.CharField(label='name')
    phone = forms.CharField(label='phone')
    address = forms.CharField(label='address')
    tg = forms.CharField(label='tg')
    wa = forms.CharField(label='wa')
    ig = forms.CharField(label='ig')
    vk = forms.CharField(label='vk')
    info = forms.CharField(widget=forms.Textarea)



