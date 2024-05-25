from django.db import models


class TelegramMessage(models.Model):
    chat_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.chat_id} - {self.message_id}"
