from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect
from flask_admin import AdminIndexView
from werkzeug.security import generate_password_hash

class CustomModelView(ModelView):
   
    def on_model_change(self, form, model, is_created):
        """For hashing password from admin panel"""
        model.password = generate_password_hash(model.password)


    def is_accessible(self):
        # can_delete = False
        return current_user.is_authenticated and current_user.has_role("admin")
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')
    
class AdminModelView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')