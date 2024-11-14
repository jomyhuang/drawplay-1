import unittest
from card_draw import CardDrawSystem
from config import PackConfig

class TestCardDrawSystem(unittest.TestCase):
    def setUp(self):
        """每个测试用例前运行"""
        self.config = PackConfig(
            total_packs=10,
            cards_per_pack=5
        )
        self.system = CardDrawSystem(self.config)
    
    def test_draw_pack(self):
        """测试单次抽卡"""
        pack = self.system.draw_pack()
        self.assertIsNotNone(pack)
        self.assertEqual(len(pack['cards']), 5)
        self.assertIn('pack_id', pack)
        self.assertIn('pack_type', pack)
        self.assertIn(pack['pack_type'], ['A', 'B', 'C'])
    
    def test_shuffle_packs(self):
        """测试打乱卡包"""
        # 记录原始顺序
        original_order = [p['pack_id'] for p in self.system.card_pool.card_packs]
        
        # 抽取一些卡包
        self.system.draw_pack()
        self.system.draw_pack()
        
        # 打乱剩余卡包
        remaining = self.system.shuffle_packs()
        
        # 验证剩余数量
        self.assertEqual(remaining, 8)
        
        # 验证顺序已改变
        new_order = [p['pack_id'] for p in self.system.card_pool.card_packs]
        self.assertNotEqual(original_order, new_order)
    
    def test_statistics_report(self):
        """测试统计报告功能"""
        # 生成报告
        report = self.system.generate_report()
        
        # 验证基本字段
        basic_fields = ['total', 'drawn', 'remaining']
        for field in basic_fields:
            self.assertIn(field, report)
            self.assertIsInstance(report[field], int)
        
        # 验证卡包类型字段
        pack_types = ['A', 'B', 'C']
        for pack_type in pack_types:
            fields = [
                f'total_{pack_type}',
                f'drawn_{pack_type}',
                f'remaining_{pack_type}',
                f'drawn_{pack_type}_percent',
                f'remaining_{pack_type}_percent'
            ]
            for field in fields:
                self.assertIn(field, report)
        
        # 验证稀有度字段
        rarities = ['R', 'SR', 'SSR', 'AR', 'BP']
        for rarity in rarities:
            fields = [f'{rarity}_count', f'{rarity}_percent']
            for field in fields:
                self.assertIn(field, report)
        
        # 验证数值合理性
        self.assertEqual(
            report['total'],
            report['drawn'] + report['remaining']
        )
        
        self.assertEqual(
            report['total'],
            report['total_A'] + report['total_B'] + report['total_C']
        )
    
    def test_empty_pool(self):
        """测试卡池耗尽情况"""
        # 抽完所有卡包
        for _ in range(10):
            pack = self.system.draw_pack()
            self.assertIsNotNone(pack)
        
        # 验证卡池耗尽
        empty_pack = self.system.draw_pack()
        self.assertIsNone(empty_pack)
        
        # 验证统计
        report = self.system.generate_report()
        self.assertEqual(report['total'], 10)
        self.assertEqual(report['drawn'], 10)
        self.assertEqual(report['remaining'], 0)

class TestPackConfig(unittest.TestCase):
    def test_default_config(self):
        """测试默认配置"""
        config = PackConfig()
        
        # 验证基本配置
        self.assertEqual(config.total_packs, 10)
        self.assertEqual(config.cards_per_pack, 5)
        
        # 验证稀有度分布总和为1
        self.assertAlmostEqual(
            sum(config.rarity_rates.values()), 
            1.0, 
            places=7,
            msg="稀有度概率总和应为1"
        )
        
        # 验证卡包类型数量
        self.assertEqual(
            len(config.pack_types), 
            3,
            msg="应该有3种卡包类型"
        )
        
        # 验证卡包类型概率总和为1
        self.assertAlmostEqual(
            sum(config.pack_type_rates.values()), 
            1.0, 
            places=7,
            msg="卡包类型概率总和应为1"
        )

if __name__ == '__main__':
    unittest.main() 