from card_draw import CardDrawSystem


def main():
    system = CardDrawSystem()
    
    while True:
        print("\n=== 抽卡模拟器 ===")
        print("1. 抽一个卡包")
        print("2. 连续抽5个卡包")
        print("3. 查看统计报表")
        print("4. 退出")
        
        choice = input("请选择操作: ")
        
        if choice == '1':
            pack = system.draw_pack()
            if pack:
                system.display_pack(pack)
            else:
                print("卡包已抽完！")
        
        elif choice == '2':
            print("\n=== 连续抽取结果 ===")
            for _ in range(5):
                pack = system.draw_pack()
                if pack:
                    system.display_pack(pack)
                else:
                    print("卡包已抽完！")
                    break
        
        elif choice == '3':
            stats = system.generate_report()
            print(f"""
=== 卡池分布报表 ===
卡池总卡包数: {stats['total']}
已抽取卡包数: {stats['drawn']}
剩余卡包数: {stats['remaining']}

剩余卡包类型分布:
普通包(无特殊卡): {stats['remaining_normal']} 包 ({stats['remaining_normal_percent']:.1f}%)
AR包(含AR卡):    {stats['remaining_ar']} 包 ({stats['remaining_ar_percent']:.1f}%)
BP包(含BP卡):    {stats['remaining_bp']} 包 ({stats['remaining_bp_percent']:.1f}%)
其他组合:        {stats['remaining_other']} 包 ({stats['remaining_other_percent']:.1f}%)

已抽取卡包类型分布:
普通包(无特殊卡): {stats['drawn_normal']} 包 ({stats['drawn_normal_percent']:.1f}%)
AR包(含AR卡):    {stats['drawn_ar']} 包 ({stats['drawn_ar_percent']:.1f}%)
BP包(含BP卡):    {stats['drawn_bp']} 包 ({stats['drawn_bp_percent']:.1f}%)
其他组合:        {stats['drawn_other']} 包 ({stats['drawn_other_percent']:.1f}%)
""")
        
        elif choice == '4':
            break
        else:
            print("无效的选择，请重试")

if __name__ == "__main__":
    main() 