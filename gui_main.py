import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from card_draw import CardDrawSystem
from datetime import datetime
from config import PackConfig
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题

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
        self.main_frame.grid_rowconfigure(1, weight=1)  # 让显示区���可扩展
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
        buttons_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)  # 增加一列
        
        # 调整按钮样式和大小
        button_style = {'width': 15, 'padding': 5}
        ttk.Button(buttons_frame, text="抽一次", command=self.draw_single, **button_style).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="抽五次", command=self.draw_five, **button_style).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="打乱卡包", command=self.shuffle_packs, **button_style).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="查看统计", command=self.show_stats, **button_style).grid(row=0, column=3, padx=5)
        ttk.Button(buttons_frame, text="查看配置", command=self.show_config, **button_style).grid(row=0, column=4, padx=5)
        ttk.Button(buttons_frame, text="导出Excel", command=self.export_to_excel, **button_style).grid(row=0, column=5, padx=5)
        
    def create_display_area(self):
        self.display_frame = ttk.LabelFrame(self.main_frame, text="抽卡结果", padding="10")
        self.display_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        
        # 建文本显示区域和滚动条的容器
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
        self.result_text.insert(tk.END, f"卡包 #{pack['pack_id']} [类型: {pack['pack_type']}] [{cards_info}]\n")
        self.result_text.see(tk.END)
        
    def show_stats(self):
        """显示统计报表"""
        stats = self.system.generate_report()
        
        # 创建统计窗口
        stats_window = tk.Toplevel(self.root)
        stats_window.title("统计报表")
        stats_window.geometry("800x600")
        
        # ��建notebook用于切换不同图表
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 基本统计标签页
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text='基本统计')
        self._create_basic_stats(basic_frame, stats)
        
        # 卡包类型分布图表
        pack_type_frame = ttk.Frame(notebook)
        notebook.add(pack_type_frame, text='卡包类型分布')
        self._create_pack_type_chart(pack_type_frame, stats)
        
        # 稀有度分布图表
        rarity_frame = ttk.Frame(notebook)
        notebook.add(rarity_frame, text='稀有度分布')
        self._create_rarity_chart(rarity_frame, stats)
        
        # 抽卡历史图表
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text='抽卡历史')
        self._create_history_chart(history_frame, stats)
    
    def _create_basic_stats(self, parent, stats):
        """创建基本统计信息"""
        # 使用Grid布局
        info_frame = ttk.LabelFrame(parent, text="基本信息", padding=10)
        info_frame.pack(fill='x', padx=5, pady=5)
        
        labels = [
            ("总卡包数:", stats['total']),
            ("已抽取数:", stats['drawn']),
            ("剩余数量:", stats['remaining']),
            ("抽取比例:", f"{(stats['drawn']/stats['total']*100):.1f}%" if stats['total'] > 0 else "0%")
        ]
        
        for i, (label, value) in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=2)
            ttk.Label(info_frame, text=str(value)).grid(row=i, column=1, sticky='w', padx=5, pady=2)
    
    def _create_pack_type_chart(self, parent, stats):
        """创建卡包类型分布图表"""
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # 准备数据
        types = ['A类型', 'B类型', 'C类型']  # 修改为中文标签
        values = [stats[f'total_{t}'] for t in 'ABC']
        colors = ['#FF9999', '#66B2FF', '#99FF99']
        
        # 创建饼图
        ax.pie(values, labels=types, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title('卡包类型分布')
        
        # 添加图表到窗口
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def _create_rarity_chart(self, parent, stats):
        """创建稀有度分布图表"""
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # 准备数据
        rarities = ['普通', '稀有', '超稀有', '特殊', '限定']  # 修改为中文标签
        values = [stats[f'{r}_count'] for r in ['R', 'SR', 'SSR', 'AR', 'BP']]
        colors = ['#CCCCCC', '#99FF99', '#66B2FF', '#FF99FF', '#FFB366']
        
        # 创建柱状图
        bars = ax.bar(rarities, values, color=colors)
        ax.set_title('稀有度分布')
        ax.set_ylabel('数量')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')
        
        # 添加图表到窗口
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def _create_history_chart(self, parent, stats):
        """创建抽卡历史图表"""
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # 准备数据
        drawn_data = [
            stats['drawn_A'],
            stats['drawn_B'],
            stats['drawn_C']
        ]
        remaining_data = [
            stats['remaining_A'],
            stats['remaining_B'],
            stats['remaining_C']
        ]
        
        # 设置数据
        labels = ['A类型包', 'B类型包', 'C类型包']  # 修改为中文标签
        x = range(len(labels))
        width = 0.35
        
        # 创建堆叠柱状图
        ax.bar(x, drawn_data, width, label='已抽取', color='#66B2FF')
        ax.bar(x, remaining_data, width, bottom=drawn_data, label='未抽取', color='#FF9999')
        
        # 设置图表
        ax.set_ylabel('数量')
        ax.set_title('抽卡历史')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        
        # 添加图表到窗口
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_config(self):
        """显示当前配置信息"""
        config_window = tk.Toplevel(self.root)
        config_window.title("当前配置")
        config_window.geometry("400x500")
        
        text_widget = tk.Text(config_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        config = self.system.card_pool.config
        
        # 生成稀有度分布文本
        rarity_text = ""
        for rarity, rate in config.rarity_rates.items():
            rarity_text += f"{rarity}: {rate*100:.1f}%\n"
            
        # 生成卡包类型配置文本
        pack_types_text = ""
        for pack_type, contents in config.pack_types.items():
            pack_types_text += f"{pack_type}包: {contents}\n"
            
        # 生成卡包类型概率文本
        pack_rates_text = ""
        for pack_type, rate in config.pack_type_rates.items():
            pack_rates_text += f"{pack_type}包: {rate*100:.1f}%\n"
        
        # 组合所有配置信息
        config_text = f"""=== 系统配置信息 ===

总卡包数量: {config.total_packs}
每包卡片数: {config.cards_per_pack}

稀有度分布:
{rarity_text}
卡包类型配置:
{pack_types_text}
卡包类型概率:
{pack_rates_text}"""
        
        text_widget.insert('1.0', config_text)
        text_widget.config(state='disabled')  # 设置为只读
        
        ttk.Button(
            config_window,
            text="关闭",
            command=config_window.destroy
        ).pack(pady=10)

    def export_to_excel(self):
        """导出数据到Excel"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f'card_packs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            )
            if filename:
                self.system.export_to_excel(filename)
                messagebox.showinfo("成功", f"数据已导出到：\n{filename}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{str(e)}")

    def shuffle_packs(self):
        """打乱卡包顺序"""
        remaining = self.system.shuffle_packs()
        messagebox.showinfo("提示", f"已打乱剩余{remaining}个卡包的顺序")

def main():
    root = tk.Tk()
    app = CardDrawGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 