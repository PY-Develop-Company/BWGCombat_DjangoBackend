from django.db import models


class LevelInfo(models.Model):
    level = models.IntegerField()
    name = models.CharField()

    def __str__(self) -> str:
        return f"level : {self.level} / name : {self.name}"


class GameResults(models.Model):
    tg_user_id = models.IntegerField()
    level = models.ForeignKey('LevelInfo', on_delete=models.SET_NULL, null=True)
    result = models.CharField(max_length=32)
    created_date = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.tg_user_id} : {self.level.name} : {self.result}"


class GameStarted(models.Model):
    tg_user_id = models.IntegerField()
    level_name = models.CharField()
    created_date = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return f"{self.tg_user_id} : {self.level_name} : {self.created_date}"
