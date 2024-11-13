import random
from datetime import datetime
from config import PackConfig
from card import Card

class CardPool:
    def __init__(self, config: PackConfig = None):
        if config is None:
            config = PackConfig()
        self.config = config
        self.cards = []
        self.card_packs = []
        self._generate_cards()
        self._generate_card_packs()
    
    def _generate_cards(self):
        """生成卡片池"""
        card_id = 1
        total_cards = self.config.total_packs * self.config.cards_per_pack * 1.2  # 生成120%的卡片数量
        
        for rarity, rate in self.config.rarity_rates.items():
            count = int(total_cards * rate)
            for _ in range(count):
                self.cards.append(Card(card_id, rarity))
                card_id += 1
    
    def _generate_card_packs(self):
        """生成卡包"""
        pack_id = 1
        cards_by_rarity = self._classify_cards()
        
        # 根据配置的包型概率生成卡包
        remaining_packs = self.config.total_packs
        for pack_type, rate in self.config.pack_type_rates.items():
            pack_count = int(self.config.total_packs * rate)
            if pack_type == list(self.config.pack_type_rates.keys())[-1]:
                pack_count = remaining_packs  # 最后一种包型补齐剩余数量
                
            for _ in range(pack_count):
                pack = self._create_pack(pack_id, pack_type, cards_by_rarity)
                if pack:
                    self.card_packs.append(pack)
                    pack_id += 1
                    remaining_packs -= 1
    
    def _classify_cards(self):
        """将卡片按稀有度分类"""
        cards_by_rarity = {}
        for rarity in self.config.rarity_rates.keys():
            cards_by_rarity[rarity] = [
                card for card in self.cards if card.rarity == rarity
            ]
        return cards_by_rarity
    
    def _create_pack(self, pack_id: int, pack_type: str, cards_by_rarity):
        """创建单个卡包"""
        pack_cards = []
        pack_config = self.config.pack_types[pack_type]
        
        # 按配置的稀有度和数量抽取卡片
        for rarity, count in pack_config.items():
            if len(cards_by_rarity[rarity]) < count:
                return None  # 卡片不足，无法生成卡包
                
            selected_cards = random.sample(cards_by_rarity[rarity], count)
            for card in selected_cards:
                cards_by_rarity[rarity].remove(card)
                pack_cards.append(card)
        
        return {
            'pack_id': pack_id,
            'pack_type': pack_type,
            'cards': pack_cards,
            'created_time': datetime.now()
        }
    