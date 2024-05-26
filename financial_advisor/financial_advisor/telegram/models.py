from django.db import models


class TelegramMessage(models.Model):
    chat_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)  # noqa: DJ001
    voice_url = models.URLField(null=True, blank=True)  # noqa: DJ001
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.chat_id} - {self.message_id}"


class LastUpdate(models.Model):
    update_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.update_id)
