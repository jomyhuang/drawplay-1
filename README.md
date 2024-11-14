# 抽卡模拟器

## 项目描述
一个模拟抽卡的程序,支持GUI和CLI两种交互方式,可以模拟抽卡过程并记录结果。

## 功能特点
1. 支持单次抽卡和连续抽卡
2. 提供详细的统计报表
3. 支持导出Excel报表
4. 支持打乱卡包顺序
5. GUI与CLI两种交互方式
6. 可配置的卡包系统

## 系统设计

### 1. 卡牌系统
- 稀有度分级：R、SR、SSR、AR、BP
- 卡池构成可配置,默认配置:
  * R卡: 30%
  * SR卡: 30%
  * SSR卡: 20%
  * AR卡: 15%
  * BP卡: 5%

### 2. 卡包系统
- 每个卡包包含5张卡牌
- 卡包具有唯一编号
- 三种卡包类型(A/B/C)及其构成:
  * A包(70%): 3R + 1SR + 1SSR
  * B包(20%): 2R + 1SR + 1SSR + 1AR
  * C包(10%): 2R + 1SR + 1SSR + 1BP

### 3. 功能模块
- 抽卡功能
  * 单次抽取
  * 连续抽取5次
  * 打乱剩余卡包
- 统计功能
  * 卡池整体分布
  * 已抽取/未抽取统计
  * 卡包类型分布
- 数据导出
  * Excel格式
  * 包含卡包数据和统计信息

## 项目结构
.
├── gui_main.py # GUI界面入口
├── cli_main.py # CLI界面入口
├── card_draw.py # 抽卡系统核心
├── card_pool.py # 卡池管理模块
├── config.py # 配置管理模块
└── card.py # 卡片基础类

## 使用说明
1. GUI模式:
   ```bash
   python gui_main.py
   ```
2. CLI模式:
   ```bash
   python cli_main.py
   ```

## 依赖项
- Python 3.x
- tkinter (GUI界面)
- pandas (Excel导出)
- openpyxl (Excel支持)

## 配置说明
可通过修改 config.py 中的 PackConfig 类来自定义:
- 卡包总数
- 每包卡片数
- 稀有度分布
- 卡包类型配置
- 卡包类型概率

## 单元测试

### 测试范围
1. 抽卡系统 (TestCardDrawSystem)
   - 单次抽卡功能
   - 打乱卡包功能
   - 统计报告生成
   - 卡池耗尽处理
   
2. 配置系统 (TestPackConfig)
   - 默认配置验证
   - 配置参数验证

### 运行测试
1. 安装测试依赖：
```bash
pip install pytest pytest-cov
```

2. 使用 unittest 运行测试：
```bash
python -m unittest tests/test_card_draw.py
```

3. 使用 pytest 运行测试：
```bash
python -m pytest tests/
```

4. 生成测试覆盖率报告：
```bash
python -m pytest --cov=. tests/
```

### 测试用例说明

#### TestCardDrawSystem
1. `test_draw_pack`
   - 验证单次抽卡功能
   - 检查卡包结构完整性
   - 验证卡包类型是否符合预期

2. `test_shuffle_packs`
   - 验证卡包打乱功能
   - 确保已抽取卡包位置不变
   - 检查剩余卡包数量准确性

3. `test_statistics_report`
   - 检查统计报告所有必要字段
   - 验证数值计算准确性
   - 确认百分比统计正确

4. `test_empty_pool`
   - 测试卡池耗尽情况
   - 验证边界条件处理
   - 确保最终统计准确

#### TestPackConfig
1. `test_default_config`
   - 验证默认配置值
   - 检查概率总和为1
   - 确认卡包类型设置正确

### 注意事项
1. 浮点数比较使用 `assertAlmostEqual`
2. 测试用例保持独立性
3. 每次测试自动重置环境
4. 仅测试核心功能模块

### 测试文件结构
```
tests/
├── __init__.py
├── test_card_draw.py    # 主要测试文件
└── test_data/          # 测试数据目录（可选）
```

### 测试维护指南
1. 新功能需要配套测试用例
2. 功能修改时更新相关测试
3. 定期执行完整测试
4. 保持测试代码整洁




