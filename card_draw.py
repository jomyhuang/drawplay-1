from card_pool import CardPool
import tkinter as tk

class CardDrawSystem:
    def __init__(self):
        self.card_pool = CardPool()
        self.drawn_packs = []
        self.drawn_pack_ids = set()
    
    def draw_pack(self):
        available_packs = [
            pack for pack in self.card_pool.card_packs 
            if pack['pack_id'] not in self.drawn_pack_ids
        ]
        
        if not available_packs:
            return None
            
        pack = available_packs[0]
        self.drawn_packs.append(pack)
        self.drawn_pack_ids.add(pack['pack_id'])
        return pack
    
    def display_pack(self, pack):
        cards_info = ' | '.join([f"{card.rarity}" for card in pack['cards']])
        print(f"卡包 #{pack['pack_id']} [{cards_info}]")
    
    def generate_report(self):
        # 获取所有卡包
        all_packs = self.card_pool.card_packs
        # 获取未抽取和已抽取的卡包
        undrawn_packs = [pack for pack in all_packs if pack['pack_id'] not in self.drawn_pack_ids]
        drawn_packs = [pack for pack in all_packs if pack['pack_id'] in self.drawn_pack_ids]
        
        # 基础统计
        total = len(all_packs)
        drawn = len(drawn_packs)
        remaining = len(undrawn_packs)
        
        # 统计未抽取卡包的各类型数量
        remaining_normal = sum(1 for pack in undrawn_packs if self._is_normal_pack(pack))
        remaining_ar = sum(1 for pack in undrawn_packs if self._is_ar_pack(pack))
        remaining_bp = sum(1 for pack in undrawn_packs if self._is_bp_pack(pack))
        remaining_other = remaining - remaining_normal - remaining_ar - remaining_bp
        
        # 统计已抽取卡包的各类型数量
        drawn_normal = sum(1 for pack in drawn_packs if self._is_normal_pack(pack))
        drawn_ar = sum(1 for pack in drawn_packs if self._is_ar_pack(pack))
        drawn_bp = sum(1 for pack in drawn_packs if self._is_bp_pack(pack))
        drawn_other = drawn - drawn_normal - drawn_ar - drawn_bp
        
        # 计算百分比
        remaining_total = remaining if remaining > 0 else 1  # 避免除以零
        drawn_total = drawn if drawn > 0 else 1  # 避免除以零
        
        return {
            'total': total,
            'drawn': drawn,
            'remaining': remaining,
            # 剩余卡包统计
            'remaining_normal': remaining_normal,
            'remaining_ar': remaining_ar,
            'remaining_bp': remaining_bp,
            'remaining_other': remaining_other,
            'remaining_normal_percent': (remaining_normal/remaining_total*100),
            'remaining_ar_percent': (remaining_ar/remaining_total*100),
            'remaining_bp_percent': (remaining_bp/remaining_total*100),
            'remaining_other_percent': (remaining_other/remaining_total*100),
            # 已抽取卡包统计
            'drawn_normal': drawn_normal,
            'drawn_ar': drawn_ar,
            'drawn_bp': drawn_bp,
            'drawn_other': drawn_other,
            'drawn_normal_percent': (drawn_normal/drawn_total*100),
            'drawn_ar_percent': (drawn_ar/drawn_total*100),
            'drawn_bp_percent': (drawn_bp/drawn_total*100),
            'drawn_other_percent': (drawn_other/drawn_total*100)
        }
    
    def _is_normal_pack(self, pack):
        """判断是否为普通卡包（不含特殊卡）"""
        return all(card.rarity not in ['AR', 'BP'] for card in pack['cards'])
        
    def _is_ar_pack(self, pack):
        """判断是否为AR卡包"""
        return any(card.rarity == 'AR' for card in pack['cards'])
        
    def _is_bp_pack(self, pack):
        """判断是否为BP卡包"""
        return any(card.rarity == 'BP' for card in pack['cards'])