from django.db import models


class SmsCsv(models.Model):
    file_name = models.FileField('File Name', upload_to='smscsv/')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'