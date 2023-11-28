from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        #select key:model
        model = User
        #select model:fields
        fields = ('first_name', 'last_name', 'username', 'email')
