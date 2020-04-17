from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
import datetime as d
# from courses.models import Faculty,Department
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save


# def validate_matric_num(value):
#     if len(str(value)) > 9 or len(str(value)) < 9 :
#         raise ValidationError(
#             _('%(value)s is not a valid registration/matric number'),
#             params={'value': value},
#         )



class UserManager(BaseUserManager):
    def create_user(self,username,first_name,last_name,email,password=None):
        if not username:
            raise ValueError('users must have a  username')
        user = self.model(first_name=first_name,last_name=last_name,username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,first_name,last_name,password):
        user = self.create_user(username,email,first_name,last_name,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, help_text='Please make sure your username is correct')
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    class Meta(object):
        unique_together = ('email',)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    REQUIRED_FIELDS = ['first_name','last_name','email']





    # def get_enroll_year(self):
    #     matric = str(self.matric_number)
    #     year_entered = str(matric[:2])
    #     '''this function isnt really full fledged as it only gets the year within the 20's'''
    #     return '20'+year_entered

    # def get_current_level_year(self):
    #     current_year = int(d.datetime.now().year)
    #     year_enrolled = int(self.get_enroll_year())
    #     '''this function isnt really full fledged because if the perso forfietes a semester , it isnt avvounted for'''
    #     level = current_year - year_enrolled
    #     return level

    # def get_faculty(self):
    #     matric = str(self.matric_number)
    #     if matric[4:6] == '11':
    #         return 'ECE'
    #     elif matric[4:6] == '21':
    #         return 'MEE'
    #     elif matric[4:6] == '31':
    #         return 'CPE' 
    #     else:
    #         return 'Department Not Found'

 

    # def get_level(self):
    #     current_level = self.get_current_level_year()
    #     if current_level == 5:
    #         return '500'
    #     elif current_level == 4:
    #         return '400'
    #     elif current_level == 3:
    #         return '300'
    #     elif current_level == 2:
    #         return '200'
    #     elif current_level == 1:
    #         return '100'
    #     else:
    #         return 'Level Not Found Maybe Extra_year Student'


    # def get_full_name(self):
    #     return '{} {}'.format(self.first_name,self.last_name)

    # def __str__(self):
    #     return str(self.matric_number)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Avi = models.ImageField(upload_to='profile_images',blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.CharField(max_length = 30, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)  

    def __str__(self):
        return self.user.first_name


def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=Profile.objects.get_or_create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)



