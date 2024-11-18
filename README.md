# 抽卡模拟器

一个功能完整的抽卡模拟系统,支持GUI和命令行两种操作方式。

## 功能特点

### 1. 多样化的抽卡系统
- 支持单抽和五连抽
- 三种不同类型的卡包(A/B/C)
- 五个稀有度等级(R/SR/SSR/AR/BP)
- 智能的卡池管理系统

### 2. 丰富的统计功能
- 实时显示卡池剩余情况
- 详细的抽卡记录
- 可视化的数据统计图表
- 支持导出Excel报表

### 3. 双重界面
- 图形界面(GUI)：基于tkinter开发
- 命令行界面(CLI)：适合脚本操作

## 系统设计

### 卡牌系统
稀有度分布：
- R卡：40% (普通卡)
- SR卡：30% (稀有卡)
- SSR卡：20% (超稀有卡)
- AR卡：7% (限定卡)
- BP卡：3% (特殊卡)

### 卡包类型
1. A类型卡包 (70%概率)
   - 3张R卡
   - 1张SR卡
   - 1张SSR卡

2. B类型卡包 (20%概率)
   - 2张R卡
   - 1张SR卡
   - 1张SSR卡
   - 1张AR卡

3. C类型卡包 (10%概率)
   - 2张R卡
   - 1张SR卡
   - 1张SSR卡
   - 1张BP卡

## 安装说明

1. 环境要求
   - Anaconda 或 Miniconda
   - Python 3.9+

2. 创建环境
   ```bash
   # 创建新环境
   conda create -n drawplay python=3.9
   
   # 激活环境
   conda activate drawplay
   ```

3. 安装依赖
   ```bash
   # 安装主要依赖
   conda install matplotlib pandas openpyxl pytest
   
   # 安装开发工具
   conda install black flake8
   ```

## 使用说明

### GUI模式
```bash
python gui_main.py
```

### 命令行模式
```bash
python cli_main.py
```

## 主要功能说明

### 1. 抽卡功能
- 单次抽卡：抽取一个卡包
- 五连抽：连续抽取5个卡包
- 卡包打乱：随机调整剩余卡包顺序

### 2. 统计功能
- 查看卡池剩余情况
- 显示已抽取卡包统计
- 生成数据分析图表

### 3. 数据导出
- 支持导出Excel格式
- 包含详细的抽卡记录
- 自动生成统计报表

## 项目结构
```
抽卡模拟器/
├── main.py          # 程序入口
├── gui_main.py      # GUI界面
├── cli_main.py      # 命令行界面
├── card_pool.py     # 卡池管理
├── card_draw.py     # 抽卡系统
├── card.py          # 卡片类
├── config.py        # 配置管理
└── requirements.txt # 依赖清单
```

## 开发相关

### 测试运行
```bash
# 运行单元测试
python -m pytest tests/

# 生成测试覆盖率报告
python -m pytest --cov=. tests/
```

### 代码规范
- 使用black进行代码格式化
- 使用flake8进行代码检查

## 注意事项
1. 首次运行前请确保安装所有依赖
2. GUI模式需要支持图形界面的环境
3. 导出功能需要足够的磁盘权限

## 更新日志
- v1.0.0: 初始版本发布
  - 实现基础抽卡功能
  - 添加GUI和CLI双界面
  - 支持数据导出和统计

## 测试指南

### 测试框架结构
```
tests/
├── __init__.py
├── test_card_draw.py    # 抽卡系统测试
├── test_card_pool.py    # 卡池管理测试
└── test_config.py       # 配置测试
```

### 运行测试

1. 运行所有测试
```bash
# 使用测试脚本
python run_tests.py

# 或使用 unittest
python -m unittest discover tests
```

2. 运行特定测试文件
```bash
# 运行抽卡系统测试
python -m unittest tests/test_card_draw.py
```

3. 运行特定测试用例
```bash
# 运行抽卡测试中的特定方法
python -m unittest tests.test_card_draw.TestCardDrawSystem.test_draw_pack
```


### 主要测试内容

1. 卡片系统测试
- 卡片创建与属性验证
- 稀有度检查
- 字符串表示测试

2. 抽卡系统测试
- 初始状态验证
- 单次抽卡功能
- 五连抽功能
- 卡包打乱验证
- 统计报告生成

3. 卡池管理测试
- 卡池初始化
- 剩余卡包统计
- 卡包分布验证

### 编写新测试

1. 创建测试文件
```python
import unittest

class TestYourFeature(unittest.TestCase):
    def setUp(self):
        # 测试准备
        pass
        
    def test_your_function(self):
        # 测试代码
        self.assertEqual(expected, actual)
```

2. 测试命名规范
- 测试文件名：`test_*.py`
- 测试类名：`Test*`
- 测试方法名：`test_*`

### 持续集成

本项目支持通过 CI/CD 自动运行测试：

1. 提交代码时自动运行测试
2. 生成测试覆盖率报告
3. 测试失败时发送通知

### 常见问题

1. 测试无法发现
- 确保测试文件名以 `test_` 开头
- 确保测试类继承 `unittest.TestCase`
- 确保测试方法名以 `test_` 开头

2. 导入错误
- 检查 PYTHONPATH 设置
- 确保在正确的虚拟环境中
- 检查依赖是否完整安装

3. 测试超时
- 检查测试中的耗时操作
- 考虑使用 mock 对象
- 优化测试逻辑

### 最佳实践

1. 测试原则
- 每个测试只测试一个功能点
- 保持测试简单明了
- 避免测试间的依赖

2. 代码覆盖
- 保持测试覆盖率在 80% 以上
- 关注核心功能的测试覆盖
- 定期检查未覆盖的代码

3. 测试维护
- 及时更新测试用例
- 删除过时的测试
- 保持测试代码整洁


