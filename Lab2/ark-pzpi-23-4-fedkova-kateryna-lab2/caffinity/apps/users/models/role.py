from django.db import models


class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'roles'
