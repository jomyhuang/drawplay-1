import random
from datetime import datetime

class Card:
    def __init__(self, id, rarity):
        self.id = id
        self.rarity = rarity

class CardPool:
    def __init__(self):
        self.cards = []
        self.card_packs = []
        self._generate_cards()
        self._generate_card_packs()
    
    def _generate_cards(self):
        rarities = {
            'R': 30,
            'SR': 30,
            'SSR': 20,
            'AR': 10,
            'BP': 10
        }
        
        card_id = 1
        for rarity, count in rarities.items():
            for _ in range(count):
                self.cards.append(Card(card_id, rarity))
                card_id += 1
    
    def _is_special_card(self, card):
        return card.rarity in ['AR', 'BP']
    
    def _generate_card_packs(self):
        # 将卡片按稀有度分类
        normal_cards = [card for card in self.cards if not self._is_special_card(card)]
        special_cards = [card for card in self.cards if self._is_special_card(card)]
        
        pack_id = 1
        
        while len(normal_cards) >= 5:  # 确保有足够的普通卡
            pack_cards = []
            
            # 先选择5张普通卡
            selected_normal = random.sample(normal_cards, 5)
            for card in selected_normal:
                normal_cards.remove(card)
                pack_cards.append(card)
            
            # 如果还有特殊卡，50%概率用一张特殊卡替换一张普通卡
            if special_cards and random.random() < 0.5:
                special_card = random.choice(special_cards)
                special_cards.remove(special_card)
                
                # 随机替换一张普通卡
                replace_index = random.randint(0, 4)
                removed_card = pack_cards[replace_index]
                pack_cards[replace_index] = special_card
                # 将被替换的普通卡放回池子
                normal_cards.append(removed_card)
            
            self.card_packs.append({
                'pack_id': pack_id,
                'cards': pack_cards,
                'created_time': datetime.now()
            })
            pack_id += 1 
            