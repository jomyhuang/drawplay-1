import tkinter as tk
from tkinter import ttk, messagebox
from card_draw import CardDrawSystem

class CardDrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("抽卡模拟器")
        self.root.geometry("800x600")
        self.system = CardDrawSystem()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建按钮区域
        self.create_buttons()
        
        # 创建显示区域
        self.create_display_area()
        
        # 创建统计区域
        self.create_stats_area()
        
    def create_buttons(self):
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=0, column=0, pady=10)
        
        ttk.Button(buttons_frame, text="抽一次", command=self.draw_single).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="抽五次", command=self.draw_five).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="查看统计", command=self.show_stats).grid(row=0, column=2, padx=5)
        
    def create_display_area(self):
        self.display_frame = ttk.LabelFrame(self.main_frame, text="抽卡结果", padding="10")
        self.display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.result_text = tk.Text(self.display_frame, height=10, width=60)
        self.result_text.grid(row=0, column=0)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.display_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = scrollbar.set
        
    def create_stats_area(self):
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="统计信息", padding="10")
        self.stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.stats_text = tk.Text(self.stats_frame, height=8, width=60)
        self.stats_text.grid(row=0, column=0)
        
    def draw_single(self):
        pack = self.system.draw_pack()
        if pack:
            self.display_pack(pack)
        else:
            messagebox.showinfo("提示", "卡包已抽完！")
            
    def draw_five(self):
        self.result_text.delete(1.0, tk.END)
        for _ in range(5):
            pack = self.system.draw_pack()
            if pack:
                self.display_pack(pack)
            else:
                messagebox.showinfo("提示", "卡包已抽完！")
                break
                
    def display_pack(self, pack):
        cards_info = ' | '.join([f"{card.rarity}" for card in pack['cards']])
        self.result_text.insert(tk.END, f"卡包 #{pack['pack_id']} [{cards_info}]\n")
        self.result_text.see(tk.END)
        
    def show_stats(self):
        #try:
            self.stats_text.delete(1.0, tk.END)
            # 获取统计信息字符串
            stats = self.system.generate_report()
            stats_text = f"""=== 卡池分布报表 ===
卡池总卡包数: {stats['total']}
已抽取卡包数: {stats['drawn']}
剩余卡包数: {stats['remaining']}

卡包类型分布:
普通包(无特殊卡): {stats['normal']} 包 ({stats['normal_percent']:.1f}%)
AR包(含AR卡):    {stats['ar']} 包 ({stats['ar_percent']:.1f}%)
BP包(含BP卡):    {stats['bp']} 包 ({stats['bp_percent']:.1f}%)
其他组合:        {stats['other']} 包 ({stats['other_percent']:.1f}%)"""
            
            self.stats_text.insert(tk.END, stats_text)
        #except Exception as e:
        #    messagebox.showerror("错误", f"显示统计信息时出错：{str(e)}")

def main():
    root = tk.Tk()
    app = CardDrawGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 