from django.db import models


class Organisation(models.Model):
    organisation_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organisations'
