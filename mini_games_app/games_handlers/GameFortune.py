from rest_framework.response import Response
from mini_games_app.games_handlers.GameBase import GameBase
from random import shuffle, randint
from mini_games_app.models import GameStarted, LevelInfo, GameResults
from user_app.models import User, UserData


class GameFortune(GameBase):
    def __init__(self):
        super().__init__(1, "Fortune", 500)
        self.total_count: int = 8  # загальна кількість можливих варіантів
        self.win: float = 1000  # сума яку можна виграти
        self.win_count_min: int = 5  # мінімальна кількість сум виграш
        self.lost: float = 1000  # сума яку можна програти
        self.lost_count_min: int = 2  # мінімальна кількість сум прогаш
        self.if_not_enough: bool = False  # проставлення якщо не вистачає True - виграш, False - програш
        # for gnome
        self.gnome_chance: int = 1
        self.gnome_chance_max: int = 100

    def start(self, tg_user_id):
        user = User.objects.get(tg_id=tg_user_id)
        user_data = UserData.objects.get(user=user)
        if user_data.g_token < self.amount_attempted + self.lost:
            return Response({"type": "error", "error_code": "551"})
        user_data.remove_g_token_coins(self.amount_attempted)
        user_data.save()
        gamestarted = GameStarted.objects.create(
            tg_user_id=tg_user_id,
            level_name=self.name
        )
        return Response({"type": "ok", "id_game": f"{gamestarted.id}", "new_g_token": user_data.g_token})

    def get_game_result(self):
        randomlist: list[str] = []
        if randint(1, self.gnome_chance_max) <= self.gnome_chance:
            randomlist.append("*")
        randomlist += ["+" for _ in range(self.win_count_min)]
        randomlist += ["-" for _ in range(self.lost_count_min)]
        if self.total_count <= len(randomlist) + 1:
            randomlist += ["+" if self.if_not_enough else "-" for _ in range(0, self.total_count - len(randomlist))]

        shuffle(randomlist)
        return randomlist[randint(0, len(randomlist) - 1)]

    def apply_game_result(self, user, user_data, result_win: str):
        if result_win == "+":
            user_data.add_g_token_coins(self.win)
        elif result_win == "-":
            user_data.remove_g_token_coins(self.lost)
        elif result_win == "*":
            user_data.add_gnomes(1)
        user_data.save()

    def get(self, game_started_id):
        game: GameFortune = GameFortune()
        try:
            gamestarted = GameStarted.objects.get(pk=game_started_id)
        except:
            return Response({"type": "error", "error_code": "552"})
        level = LevelInfo.objects.get(name="Fortune")

        user = User.objects.get(tg_id=gamestarted.tg_user_id)
        user_data = UserData.objects.get(user=user)

        result_win: str = game.get_game_result()
        game.apply_game_result(user, user_data, result_win)

        gamestarted.delete()

        gameresult = GameResults.objects.create(tg_user_id=user.tg_id, level=level, result=result_win)
        gameresult.save()

        return Response({"type": "ok", "data": result_win})
