from card_pool import CardPool
import tkinter as tk
import pandas as pd
from datetime import datetime
from config import PackConfig
import random

class CardDrawSystem:
    def __init__(self, config: PackConfig = None):
        if config is None:
            config = PackConfig()
        self.card_pool = CardPool(config)
        self.drawn_packs = []
        self.drawn_pack_ids = set()
    
    def draw_pack(self):
        """抽取一个卡包"""
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
    
    def shuffle_packs(self):
        """打乱卡包顺序"""
        # 获取未抽取的卡包
        available_packs = [
            pack for pack in self.card_pool.card_packs 
            if pack['pack_id'] not in self.drawn_pack_ids
        ]
        
        # 打乱顺序
        random.shuffle(available_packs)
        
        # 更新卡池中的卡包顺序
        drawn_packs = [
            pack for pack in self.card_pool.card_packs 
            if pack['pack_id'] in self.drawn_pack_ids
        ]
        
        self.card_pool.card_packs = drawn_packs + available_packs
        
        return len(available_packs)  # 返回剩余可抽取的卡包数量
    
    def generate_report(self):
        """生成统计报告"""
        # 获取所有卡包
        all_packs = self.card_pool.card_packs
        # 获取未抽取和已抽取的卡包
        undrawn_packs = [pack for pack in all_packs if pack['pack_id'] not in self.drawn_pack_ids]
        drawn_packs = [pack for pack in all_packs if pack['pack_id'] in self.drawn_pack_ids]
        
        # 基础统计
        total = len(all_packs)
        drawn = len(drawn_packs)
        remaining = len(undrawn_packs)
        
        # 统计各类型卡包数量
        total_by_type = {'A': 0, 'B': 0, 'C': 0}
        remaining_by_type = {'A': 0, 'B': 0, 'C': 0}
        drawn_by_type = {'A': 0, 'B': 0, 'C': 0}
        
        # 统计稀有度
        rarity_count = {'R': 0, 'SR': 0, 'SSR': 0, 'AR': 0, 'BP': 0}
        
        # 计算各种统计
        for pack in all_packs:
            pack_type = pack['pack_type']
            total_by_type[pack_type] += 1
            
            if pack['pack_id'] in self.drawn_pack_ids:
                drawn_by_type[pack_type] += 1
            else:
                remaining_by_type[pack_type] += 1
            
            # 统计卡片稀有度
            for card in pack['cards']:
                rarity_count[card.rarity] += 1
        
        # 计算百分比
        total_cards = sum(rarity_count.values())
        
        return {
            'total': total,
            'drawn': drawn,
            'remaining': remaining,
            
            # 各类型卡包总数
            'total_A': total_by_type['A'],
            'total_B': total_by_type['B'],
            'total_C': total_by_type['C'],
            
            # 剩余卡包统计
            'remaining_A': remaining_by_type['A'],
            'remaining_B': remaining_by_type['B'],
            'remaining_C': remaining_by_type['C'],
            'remaining_A_percent': (remaining_by_type['A']/total*100) if total > 0 else 0,
            'remaining_B_percent': (remaining_by_type['B']/total*100) if total > 0 else 0,
            'remaining_C_percent': (remaining_by_type['C']/total*100) if total > 0 else 0,
            
            # 已抽取卡包统计
            'drawn_A': drawn_by_type['A'],
            'drawn_B': drawn_by_type['B'],
            'drawn_C': drawn_by_type['C'],
            'drawn_A_percent': (drawn_by_type['A']/total*100) if total > 0 else 0,
            'drawn_B_percent': (drawn_by_type['B']/total*100) if total > 0 else 0,
            'drawn_C_percent': (drawn_by_type['C']/total*100) if total > 0 else 0,
            
            # 稀有度统计
            'R_count': rarity_count['R'],
            'SR_count': rarity_count['SR'],
            'SSR_count': rarity_count['SSR'],
            'AR_count': rarity_count['AR'],
            'BP_count': rarity_count['BP'],
            'R_percent': (rarity_count['R']/total_cards*100) if total_cards > 0 else 0,
            'SR_percent': (rarity_count['SR']/total_cards*100) if total_cards > 0 else 0,
            'SSR_percent': (rarity_count['SSR']/total_cards*100) if total_cards > 0 else 0,
            'AR_percent': (rarity_count['AR']/total_cards*100) if total_cards > 0 else 0,
            'BP_percent': (rarity_count['BP']/total_cards*100) if total_cards > 0 else 0
        }
    
    def export_to_excel(self, filename=None):
        """导出卡包数据到Excel文件"""
        if filename is None:
            filename = f'card_packs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
        # 准备卡包数据
        packs_data = []
        for pack in self.card_pool.card_packs:
            pack_data = {
                '卡包ID': pack['pack_id'],
                '卡包类型': pack['pack_type'],
                '生成时间': pack['created_time'],
                '抽取状态': '已抽取' if pack['pack_id'] in self.drawn_pack_ids else '未抽取'
            }
            
            # 添加卡片信息
            for i, card in enumerate(pack['cards'], 1):
                pack_data[f'卡片{i}'] = card.rarity
                
            packs_data.append(pack_data)
            
        # 创建DataFrame
        df_packs = pd.DataFrame(packs_data)
        
        # 准备统计数据
        stats = self.generate_report()
        stats_data = {
            '统计项': [
                '总卡包数', '已抽取数', '剩余数量',
                'A型卡包数', 'B型卡包数', 'C型卡包数',
                'R卡数量', 'SR卡数量', 'SSR卡数量',
                'AR卡数量', 'BP卡数量'
            ],
            '数值': [
                stats['total'], stats['drawn'], stats['remaining'],
                stats['total_A'], stats['total_B'], stats['total_C'],
                stats['R_count'], stats['SR_count'], stats['SSR_count'],
                stats['AR_count'], stats['BP_count']
            ],
            '百分比': [
                '100%',
                f"{(stats['drawn']/stats['total']*100):.1f}%" if stats['total'] > 0 else '0%',
                f"{(stats['remaining']/stats['total']*100):.1f}%" if stats['total'] > 0 else '0%',
                f"{(stats['total_A']/stats['total']*100):.1f}%" if stats['total'] > 0 else '0%',
                f"{(stats['total_B']/stats['total']*100):.1f}%" if stats['total'] > 0 else '0%',
                f"{(stats['total_C']/stats['total']*100):.1f}%" if stats['total'] > 0 else '0%',
                f"{stats['R_percent']:.1f}%",
                f"{stats['SR_percent']:.1f}%",
                f"{stats['SSR_percent']:.1f}%",
                f"{stats['AR_percent']:.1f}%",
                f"{stats['BP_percent']:.1f}%"
            ]
        }
        df_stats = pd.DataFrame(stats_data)
        
        # 创建Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df_packs.to_excel(writer, sheet_name='卡包数据', index=False)
            df_stats.to_excel(writer, sheet_name='统计数据', index=False)
            
            # 调整列宽
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
                    
        return filename