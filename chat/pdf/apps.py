from django.apps import AppConfig


class PdfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pdf"

    def ready(self):
        # Імпортуйте ваші крон-завдання тут і зареєструйте їх
        from pdf.cron import MyCronJob

        # Зареєструйте ваше крон-завдання
        MyCronJob()
