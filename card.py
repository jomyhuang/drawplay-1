from dataclasses import dataclass
from datetime import datetime

@dataclass
class Card:
    """卡片类"""
    card_id: int
    rarity: str  # 稀有度：R, SR, SSR, AR, BP
    created_time: datetime = None
    
    def __post_init__(self):
        if self.created_time is None:
            self.created_time = datetime.now()
    
    def __str__(self):
        return f"Card(#{self.card_id}, {self.rarity})"
    
    def __repr__(self):
        return self.__str__() 