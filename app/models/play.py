from pydantic import BaseModel

class Play(BaseModel):
    id_user: int
    id_minigame: int
    score: int
    result: bool
    money_earned: int
    played_at: str