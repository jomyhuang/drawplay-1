from card_draw import CardDrawSystem
from config import PackConfig

def display_menu():
    print("\n=== 抽卡模拟器 ===")
    print("1. 抽一次")
    print("2. 抽五次")
    print("3. 查看统计")
    print("4. 显示配置信息")
    print("5. 导出Excel")
    print("0. 退出")
    print("================")

def display_config(config: PackConfig):
    print("\n=== 当前配置信息 ===")
    print(f"卡包总数: {config.total_packs}")
    print(f"每包卡牌数: {config.cards_per_pack}")
    
    print("\n稀有度分布:")
    for rarity, rate in config.rarity_rates.items():
        print(f"{rarity}: {rate*100:.1f}%")
    
    print("\n卡包类型配置:")
    for pack_type, contents in config.pack_types.items():
        print(f"\n{pack_type}型卡包:")
        print(f"生成概率: {config.pack_type_rates[pack_type]*100:.1f}%")
        print("卡牌组成:", end=" ")
        for rarity, count in contents.items():
            print(f"{rarity}×{count}", end=" ")
    print("\n================")

def display_stats(stats):
    print("\n=== 统计报告 ===")
    print(f"卡池总卡包数: {stats['total']}")
    print(f"已抽取卡包数: {stats['drawn']}")
    print(f"剩余卡包数: {stats['remaining']}")
    
    print("\n剩余卡包分布:")
    for pack_type in ['A', 'B', 'C']:
        print(f"{pack_type}型包: {stats[f'remaining_{pack_type}']} ({stats[f'remaining_{pack_type}_percent']:.1f}%)")
    
    print("\n已抽取卡包分布:")
    for pack_type in ['A', 'B', 'C']:
        print(f"{pack_type}型包: {stats[f'drawn_{pack_type}']} ({stats[f'drawn_{pack_type}_percent']:.1f}%)")
    
    print("\n稀有度分布:")
    for rarity in ['R', 'SR', 'SSR', 'AR', 'BP']:
        print(f"{rarity}: {stats[f'{rarity}_count']} ({stats[f'{rarity}_percent']:.1f}%)")

def main():
    system = CardDrawSystem()
    
    while True:
        display_menu()
        choice = input("请选择操作: ")
        
        if choice == '1':
            pack = system.draw_pack()
            if pack:
                system.display_pack(pack)
            else:
                print("卡包已抽完！")
                
        elif choice == '2':
            for _ in range(5):
                pack = system.draw_pack()
                if pack:
                    system.display_pack(pack)
                else:
                    print("卡包已抽完！")
                    break
                    
        elif choice == '3':
            stats = system.generate_report()
            display_stats(stats)
            
        elif choice == '4':
            display_config(system.config)
            
        elif choice == '5':
            filename = system.export_to_excel()
            print(f"数据已导出到：{filename}")
            
        elif choice == '0':
            print("感谢使用！")
            break
            
        else:
            print("无效的选择，请重试。")

if __name__ == "__main__":
    main() 