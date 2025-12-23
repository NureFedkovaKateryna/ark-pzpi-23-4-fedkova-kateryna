from django.db import models


class CommandType(models.Model):
    command_type_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'command_types'
