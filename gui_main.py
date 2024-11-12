import tkinter as tk
from tkinter import ttk, messagebox
from card_draw import CardDrawSystem

class CardDrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("抽卡模拟器")
        self.root.geometry("800x600")
        self.system = CardDrawSystem()
        
        # 配置根窗口的网格权重，使其可扩展
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 创建主框架并配置权重
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # 让显示区域可扩展
        self.main_frame.grid_rowconfigure(2, weight=1)  # 让统计区域可扩展
        
        # 创建按钮区域
        self.create_buttons()
        
        # 创建显示区域
        self.create_display_area()
        
        # 创建统计区域
        self.create_stats_area()
        
    def create_buttons(self):
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=0, column=0, pady=10, sticky="ew")
        buttons_frame.grid_columnconfigure((0,1,2), weight=1)  # 使按钮均匀分布
        
        # 调整按钮样式和大小
        button_style = {'width': 15, 'padding': 5}
        ttk.Button(buttons_frame, text="抽一次", command=self.draw_single, **button_style).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="抽五次", command=self.draw_five, **button_style).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="查看统计", command=self.show_stats, **button_style).grid(row=0, column=2, padx=5)
        
    def create_display_area(self):
        self.display_frame = ttk.LabelFrame(self.main_frame, text="抽卡结果", padding="10")
        self.display_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        
        # 创建文本显示区域和滚动条的容器
        text_container = ttk.Frame(self.display_frame)
        text_container.grid(row=0, column=0, sticky="nsew")
        text_container.grid_columnconfigure(0, weight=1)
        text_container.grid_rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(text_container, height=10, width=60)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text['yscrollcommand'] = scrollbar.set
        
    def create_stats_area(self):
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="统计信息", padding="10")
        self.stats_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_rowconfigure(0, weight=1)
        
        self.stats_text = tk.Text(self.stats_frame, height=8, width=60)
        self.stats_text.grid(row=0, column=0, sticky="nsew")
        
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
        stats = self.system.generate_report()
        stats_window = tk.Toplevel(self.root)
        stats_window.title("统计报表")
        stats_window.geometry("400x500")
        
        # 使用Text组件显示统计信息
        text_widget = tk.Text(stats_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        stats_text = f"""
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
"""
        
        text_widget.insert('1.0', stats_text)
        text_widget.config(state='disabled')  # 设置为只读
        
        # 添加关闭按钮
        tk.Button(
            stats_window, 
            text="关闭", 
            command=stats_window.destroy
        ).pack(pady=10)

def main():
    root = tk.Tk()
    app = CardDrawGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 