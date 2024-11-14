from dataclasses import dataclass
from typing import Dict

@dataclass
class PackConfig:
    """卡包配置类"""
    # 基础配置
    total_packs: int = 10  # 总卡包数
    cards_per_pack: int = 5  # 每包卡片数
    safety_factor: float = 1.3  # 卡片生成安全系数
    min_cards_per_rarity: int = 10  # 每种稀有度的最小卡片数
    
    # 稀有度分布配置
    rarity_rates: Dict[str, float] = None
    
    # 包型配置 (每种包型包含的各稀有度卡片数量)
    pack_types: Dict[str, Dict[str, int]] = None
    
    # 包型概率配置
    pack_type_rates: Dict[str, float] = None
    
    def __post_init__(self):
        """初始化默认配置"""
        if self.rarity_rates is None:
            self.rarity_rates = {
                'R': 0.4,    # 增加到40%
                'SR': 0.3,   # 30%
                'SSR': 0.2,  # 20%
                'AR': 0.07,  # 7%
                'BP': 0.03   # 3%
            }
            
        if self.pack_types is None:
            self.pack_types = {
                'A': {'R': 3, 'SR': 1, 'SSR': 1},
                'B': {'R': 2, 'SR': 1, 'SSR': 1, 'AR': 1},
                'C': {'R': 2, 'SR': 1, 'SSR': 1, 'BP': 1}
            }
            
        if self.pack_type_rates is None:
            self.pack_type_rates = {
                'A': 0.7,  # 70%
                'B': 0.2,  # 20%
                'C': 0.1   # 10%
            }