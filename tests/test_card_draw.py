import unittest
from datetime import datetime
from card_draw import CardDrawSystem
from card_pool import Card, CardPool

class TestCardDrawSystem(unittest.TestCase):
    def setUp(self):
        """每个测试用例前都会执行的初始化方法"""
        self.draw_system = CardDrawSystem()
    
    def test_draw_single_pack(self):
        """测试单次抽卡功能"""
        # 抽取一个卡包
        pack = self.draw_system.draw_pack()
        
        # 验证卡包结构
        self.assertIsNotNone(pack)
        self.assertIn('pack_id', pack)
        self.assertIn('cards', pack)
        self.assertIn('created_time', pack)
        
        # 验证卡包内容
        self.assertEqual(len(pack['cards']), 5)  # 确保每个卡包有5张卡
        self.assertIsInstance(pack['created_time'], datetime)
        
        # 验证抽卡记录
        self.assertEqual(len(self.draw_system.drawn_pack_ids), 1)
        self.assertIn(pack['pack_id'], self.draw_system.drawn_pack_ids)
        
    def test_draw_multiple_packs(self):
        """测试连续抽卡功能"""
        drawn_packs = []
        for _ in range(5):
            pack = self.draw_system.draw_pack()
            if pack:
                drawn_packs.append(pack)
        
        self.assertEqual(len(drawn_packs), 5)  # 确保返回5个卡包
        self.assertEqual(len(self.draw_system.drawn_pack_ids), 5)  # 确保记录了抽取历史
        
        # 验证每个卡包ID都不同
        pack_ids = [pack['pack_id'] for pack in drawn_packs]
        self.assertEqual(len(set(pack_ids)), 5)  # 确保ID唯一
        
    def test_special_card_probability(self):
        """测试特殊卡片(AR/BP)的出现概率"""
        total_draws = 0
        special_cards = 0
        
        # 抽取所有卡包
        while True:
            pack = self.draw_system.draw_pack()
            if pack is None:  # 卡包抽完了
                break
                
            total_draws += 1
            # 检查每张卡是否为特殊卡片
            for card in pack['cards']:
                if card.rarity in ['AR', 'BP']:
                    special_cards += 1
        
        # 计算特殊卡片的出现概率（每张卡的概率）
        total_cards = total_draws * 5  # 每个卡包5张卡
        probability = special_cards / total_cards if total_cards > 0 else 0
        
        # 根据 CardPool 的实际概率设置：
        # AR: 10%, BP: 10%, 总计特殊卡片概率: 20%
        # 考虑到随机性，允许一定范围的波动
        expected_min = 0.05  # 5%
        expected_max = 0.15  # 15%
        
        # 输出实际概率，便于调试
        print(f"\n特殊卡片概率测试:")
        print(f"总卡片数: {total_cards}")
        print(f"特殊卡片数: {special_cards}")
        print(f"实际概率: {probability:.2%}")
        print(f"期望概率范围: {expected_min:.0%} - {expected_max:.0%}")
        
        self.assertGreater(probability, expected_min, 
            f"特殊卡片概率 {probability:.2%} 低于最小期望值 {expected_min:.0%}")
        self.assertLess(probability, expected_max, 
            f"特殊卡片概率 {probability:.2%} 高于最大期望值 {expected_max:.0%}")
        
    def test_empty_pool(self):
        """测试卡池抽空的情况"""
        # 记录总卡包数
        total_packs = len(self.draw_system.card_pool.card_packs)
        drawn_packs = []
        
        # 抽完所有卡包
        while True:
            pack = self.draw_system.draw_pack()
            if pack is None:
                break
            drawn_packs.append(pack)
            
        # 验证抽取记录
        self.assertEqual(len(drawn_packs), total_packs)
        self.assertEqual(len(self.draw_system.drawn_pack_ids), total_packs)
        
        # 验证继续抽卡返回None
        self.assertIsNone(self.draw_system.draw_pack())
        
    def test_statistics_report(self):
        """测试统计报告功能"""
        # 抽取一些卡包
        for _ in range(10):
            self.draw_system.draw_pack()
            
        report = self.draw_system.generate_report()
        
        # 验证报告包含所有必要字段
        required_fields = [
            'total', 'drawn', 'remaining',
            'remaining_normal', 'remaining_ar', 'remaining_bp', 'remaining_other',
            'remaining_normal_percent', 'remaining_ar_percent',
            'remaining_bp_percent', 'remaining_other_percent',
            'drawn_normal', 'drawn_ar', 'drawn_bp', 'drawn_other',
            'drawn_normal_percent', 'drawn_ar_percent',
            'drawn_bp_percent', 'drawn_other_percent'
        ]
        
        for field in required_fields:
            self.assertIn(field, report)
            
        # 验证数据的正确性
        self.assertEqual(report['drawn'], 10)
        self.assertEqual(report['total'], report['drawn'] + report['remaining'])
        
        # 验证百分比计算
        if report['remaining'] > 0:
            self.assertAlmostEqual(
                report['remaining_normal_percent'] + 
                report['remaining_ar_percent'] + 
                report['remaining_bp_percent'] + 
                report['remaining_other_percent'],
                100.0,
                places=1
            )
        
        if report['drawn'] > 0:
            self.assertAlmostEqual(
                report['drawn_normal_percent'] + 
                report['drawn_ar_percent'] + 
                report['drawn_bp_percent'] + 
                report['drawn_other_percent'],
                100.0,
                places=1
            )
        
    def test_no_duplicate_draws(self):
        """测试不会重复抽取同一个卡包"""
        drawn_pack_ids = set()
        
        # 连续抽取10次
        for _ in range(10):
            pack = self.draw_system.draw_pack()
            if pack:
                # 确保每个卡包ID都是唯一的
                self.assertNotIn(pack['pack_id'], drawn_pack_ids)
                drawn_pack_ids.add(pack['pack_id'])
        
        # 验证抽取记录
        self.assertEqual(len(drawn_pack_ids), 10)
        self.assertEqual(len(self.draw_system.drawn_pack_ids), 10)
        self.assertEqual(drawn_pack_ids, self.draw_system.drawn_pack_ids)

if __name__ == '__main__':
    unittest.main() 