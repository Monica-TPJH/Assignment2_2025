#!/usr/bin/env python3
"""
Hong Kong Labor Statistics Data Analysis and Visualization Script
"""

import pandas as pd
import matplotlib.pyplot as plt

# Set Chinese font support (for displaying Chinese characters if needed)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class HKLaborAnalyzer:
    def __init__(self, csv_file="HK_Labor/hk_labor_enhanced.csv"):
        self.csv_file = csv_file
        self.df = None
        self.load_data()
        
    def load_data(self):
        """加载CSV数据"""
        try:
            self.df = pd.read_csv(self.csv_file)
            self.df['年月'] = pd.to_datetime(self.df['年月'])
            print(f"成功加载数据: {len(self.df)} 行, {len(self.df.columns)} 列")
            print(f"数据时间范围: {self.df['年月'].min()} 到 {self.df['年月'].max()}")
        except Exception as e:
            print(f"加载数据失败: {e}")
            
    def basic_statistics(self):
        """基本统计分析"""
        if self.df is None:
            return
            
        print("\n=== 基本统计信息 ===")
        key_columns = ['劳动人口_千人', '就业人数_千人', '失业人数_千人', '失业率_百分比']
        
        for col in key_columns:
            if col in self.df.columns:
                stats = self.df[col].describe()
                print(f"\n{col}:")
                print(f"  平均值: {stats['mean']:.2f}")
                print(f"  最大值: {stats['max']:.2f}")
                print(f"  最小值: {stats['min']:.2f}")
                print(f"  标准差: {stats['std']:.2f}")
                
    def plot_trends(self):
        """绘制趋势图"""
        if self.df is None:
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('香港劳动力市场趋势分析 (2015-2025)', fontsize=16, fontweight='bold')
        
        # 劳动人口趋势
        axes[0, 0].plot(self.df['年月'], self.df['劳动人口_千人'], 'b-', linewidth=2)
        axes[0, 0].set_title('劳动人口趋势')
        axes[0, 0].set_ylabel('千人')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 就业人数趋势
        axes[0, 1].plot(self.df['年月'], self.df['就业人数_千人'], 'g-', linewidth=2)
        axes[0, 1].set_title('就业人数趋势')
        axes[0, 1].set_ylabel('千人')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 失业率趋势
        axes[1, 0].plot(self.df['年月'], self.df['失业率_百分比'], 'r-', linewidth=2)
        axes[1, 0].set_title('失业率趋势')
        axes[1, 0].set_ylabel('百分比 (%)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 劳动参与率趋势
        axes[1, 1].plot(self.df['年月'], self.df['劳动人口参与率_百分比'], 'orange', linewidth=2)
        axes[1, 1].set_title('劳动人口参与率趋势')
        axes[1, 1].set_ylabel('百分比 (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 调整布局
        plt.tight_layout()
        plt.savefig('hk_labor_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("趋势图已保存为: hk_labor_trends.png")
        
    def generate_summary_report(self):
        """生成简化的摘要报告"""
        if self.df is None:
            return
            
        print("\n" + "="*50)
        print("香港劳动人口、就业及失业数据分析报告")
        print("="*50)
        
        # 基本统计
        self.basic_statistics()
        
        # 关键发现
        print("\n=== 关键发现 ===")
        latest_data = self.df.iloc[-1]
        earliest_data = self.df.iloc[0]
        
        labor_growth = ((latest_data['劳动人口_千人'] - earliest_data['劳动人口_千人']) / 
                       earliest_data['劳动人口_千人'] * 100)
        
        print(f"1. 劳动人口增长: {labor_growth:.1f}% ({earliest_data['年月'].strftime('%Y-%m')} 到 {latest_data['年月'].strftime('%Y-%m')})")
        
        avg_unemployment = self.df['失业率_百分比'].mean()
        print(f"2. 平均失业率: {avg_unemployment:.2f}%")
        
        max_unemployment = self.df['失业率_百分比'].max()
        min_unemployment = self.df['失业率_百分比'].min()
        print(f"3. 失业率范围: {min_unemployment:.1f}% - {max_unemployment:.1f}%")
        
        if '男性劳动人口_千人' in self.df.columns:
            male_ratio = (latest_data['男性劳动人口_千人'] / 
                         (latest_data['男性劳动人口_千人'] + latest_data['女性劳动人口_千人']) * 100)
            print(f"4. 当前男性劳动人口占比: {male_ratio:.1f}%")
        
        print(f"5. 当前劳动参与率: {latest_data['劳动人口参与率_百分比']:.1f}%")
        
        # 生成趋势图
        print("\n=== 生成可视化图表 ===")
        self.plot_trends()
        
        print("\n=== 报告完成 ===")
        print("图表已保存为PNG文件")

def main():
    """主函数"""
    print("香港劳动统计数据分析器")
    print("=" * 30)
    
    # 创建分析器实例
    analyzer = HKLaborAnalyzer()
    
    # 生成报告
    analyzer.generate_summary_report()

if __name__ == "__main__":
    main()