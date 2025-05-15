from pydantic import BaseModel

class Play(BaseModel):
    id_user: int
    id_minigame: int
    score: int
    money_earned: int