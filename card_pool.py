import random
from datetime import datetime
from config import PackConfig
from card import Card
import math

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
        
        # 计算基础需求
        base_requirements = {
            'R': {
                'A': self.config.total_packs * 0.7 * 3,  # A包需要3张R
                'B': self.config.total_packs * 0.2 * 2,  # B包需要2张R
                'C': self.config.total_packs * 0.1 * 2   # C包需要2张R
            },
            'SR': {
                'all': self.config.total_packs  # 每包都需要1张SR
            },
            'SSR': {
                'all': self.config.total_packs  # 每包都需要1张SSR
            },
            'AR': {
                'B': self.config.total_packs * 0.2  # B包需要1张AR
            },
            'BP': {
                'C': self.config.total_packs * 0.1  # C包需要1张BP
            }
        }
        
        # 计算每种卡片的总需求
        total_requirements = {
            'R': sum(base_requirements['R'].values()),
            'SR': base_requirements['SR']['all'],
            'SSR': base_requirements['SSR']['all'],
            'AR': base_requirements['AR']['B'],
            'BP': base_requirements['BP']['C']
        }
        
        # 使用配置的安全系数和最小卡片数
        card_counts = {
            rarity: max(
                self.config.min_cards_per_rarity,
                int(math.ceil(count * self.config.safety_factor))
            )
            for rarity, count in total_requirements.items()
        }
        
        # 生成卡片并打印信息
        print("\n=== 生成卡片详情 ===")
        for rarity, count in card_counts.items():
            print(f"生成 {rarity} 卡片: {count}张 (基础需求: {total_requirements[rarity]:.1f}张)")
            for _ in range(count):
                self.cards.append(Card(card_id, rarity))
                card_id += 1
        
        # 验证生成的卡片数量
        rarity_counts = {}
        for card in self.cards:
            rarity_counts[card.rarity] = rarity_counts.get(card.rarity, 0) + 1
        
        print("\n=== 实际生成卡片数量 ===")
        for rarity, count in rarity_counts.items():
            print(f"{rarity}卡: {count}张")
    
    def _generate_card_packs(self):
        """生成卡包"""
        pack_id = 1
        cards_by_rarity = self._classify_cards()
        
        # 确保每种类型至少有1个包
        pack_counts = {
            'A': max(1, int(self.config.total_packs * 0.7)),  # 至少1包
            'B': max(1, int(self.config.total_packs * 0.2)),  # 至少1包
            'C': max(1, int(self.config.total_packs * 0.1))   # 至少1包
        }
        
        # 调整总数到配置的包数
        total = sum(pack_counts.values())
        if total > self.config.total_packs:
            # 如果总数超过，优先减少C包和B包
            excess = total - self.config.total_packs
            for pack_type in ['C', 'B', 'A']:
                while excess > 0 and pack_counts[pack_type] > 1:
                    pack_counts[pack_type] -= 1
                    excess -= 1
        elif total < self.config.total_packs:
            # 如果总数不足，补给A包
            pack_counts['A'] += (self.config.total_packs - total)
        
        print("\n=== 计划生成的卡包数量 ===")
        for pack_type, count in pack_counts.items():
            print(f"{pack_type}类型卡包: {count}个")
        
        # 生成各类型卡包
        for pack_type, count in pack_counts.items():
            print(f"\n尝试生成 {pack_type} 类型卡包 {count} 个")
            for _ in range(count):
                pack = self._create_pack(pack_id, pack_type, cards_by_rarity)
                if pack:
                    self.card_packs.append(pack)
                    pack_id += 1
                    print(f"成功创建 {pack_type} 类型卡包")
                else:
                    print(f"创建 {pack_type} 类型卡包失败")
            
            # 显示每种类型后的剩余卡片
            print("\n当前剩余卡片:")
            for rarity, cards in cards_by_rarity.items():
                print(f"{rarity}卡剩余: {len(cards)}")
    
    def _classify_cards(self):
        """将卡片按稀有度分类"""
        cards_by_rarity = {
            'R': [],
            'SR': [],
            'SSR': [],
            'AR': [],
            'BP': []
        }
        
        # 将所有卡片分类
        for card in self.cards:
            if card.rarity in cards_by_rarity:
                cards_by_rarity[card.rarity].append(card)
        
        return cards_by_rarity
    
    def _create_pack(self, pack_id, pack_type, cards_by_rarity):
        """创建一个卡包"""
        required_cards = self.config.pack_types[pack_type]
        
        # 检查卡片是否足够
        insufficient_cards = []
        for rarity, count in required_cards.items():
            if len(cards_by_rarity[rarity]) < count:
                insufficient_cards.append(
                    f"{rarity}卡不足(需要{count}张，剩余{len(cards_by_rarity[rarity])}张)"
                )
        
        if insufficient_cards:
            print(f"创建{pack_type}包失败: {', '.join(insufficient_cards)}")
            return None
        
        # 抽取卡片
        selected_cards = []
        try:
            for rarity, count in required_cards.items():
                available_cards = cards_by_rarity[rarity]
                if len(available_cards) < count:
                    raise ValueError(f"卡片不足: {rarity}卡只剩{len(available_cards)}张，需要{count}张")
                
                for _ in range(count):
                    card = available_cards.pop()
                    selected_cards.append(card)
            
            return {
                'pack_id': pack_id,
                'pack_type': pack_type,
                'cards': selected_cards,
                'created_time': datetime.now()
            }
        except Exception as e:
            print(f"创建卡包时发生错误: {str(e)}")
            # 发生错误时，将已抽取的卡片放回
            for card in selected_cards:
                cards_by_rarity[card.rarity].append(card)
            return None
    