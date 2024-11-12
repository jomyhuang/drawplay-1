from card_pool import CardPool
import tkinter as tk

class CardDrawSystem:
    def __init__(self):
        self.card_pool = CardPool()
        self.drawn_packs = []
    
    def draw_pack(self):
        if not self.card_pool.card_packs:
            return None
            
        pack = self.card_pool.card_packs.pop(0)
        self.drawn_packs.append(pack)
        return pack
    
    def display_pack(self, pack):
        cards_info = ' | '.join([f"{card.rarity}" for card in pack['cards']])
        print(f"卡包 #{pack['pack_id']} [{cards_info}]")
    
    def generate_report(self):
        total = len(self.card_pool.card_packs)
        drawn = len(self.drawn_packs)
        remaining = total - drawn
        
        # 统计各类型卡包数量
        normal = sum(1 for pack in self.card_pool.card_packs if self._is_normal_pack(pack))
        ar = sum(1 for pack in self.card_pool.card_packs if self._is_ar_pack(pack))
        bp = sum(1 for pack in self.card_pool.card_packs if self._is_bp_pack(pack))
        other = total - normal - ar - bp
        
        return {
            'total': total,
            'drawn': drawn,
            'remaining': remaining,
            'normal': normal,
            'ar': ar,
            'bp': bp,
            'other': other,
            'normal_percent': (normal/total*100) if total > 0 else 0,
            'ar_percent': (ar/total*100) if total > 0 else 0,
            'bp_percent': (bp/total*100) if total > 0 else 0,
            'other_percent': (other/total*100) if total > 0 else 0
        }
    
    def _is_normal_pack(self, pack):
        """判断是否为普通卡包"""
        for card in pack['cards']:
            if card.rarity in ['AR', 'BP']:
                return False
        return True
    
    def _is_ar_pack(self, pack):
        """判断是否为AR卡包"""
        for card in pack['cards']:
            if card.rarity == 'AR':
                return True
        return False
    
    def _is_bp_pack(self, pack):
        """判断是否为BP卡包"""
        for card in pack['cards']:
            if card.rarity == 'BP':
                return True
        return False