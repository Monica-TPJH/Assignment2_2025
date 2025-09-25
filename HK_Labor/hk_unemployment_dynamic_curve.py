#!/usr/bin/env python3
"""
Hong Kong Unemployment Rate Particle Explosion Visualization
Focus on particle explosion effects, unemployment rate drives explosion intensity
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import math
import colorsys

# Set Chinese font support (for displaying Chinese characters if needed)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class Particle:
    def __init__(self, x, y, vx, vy, color, size=1, life=60):
        self.x = x  # X coordinate
        self.y = y  # Y coordinate
        self.vx = vx  # X velocity
        self.vy = vy  # Y velocity
        self.color = color  # Particle color
        self.size = size  # Particle size
        self.life = life  # Particle lifetime
        self.max_life = life  # Maximum lifetime
        self.gravity = -0.02  # Gravity effect

class HKUnemploymentCurveAnimator:
    def __init__(self, csv_file="hk_labor_enhanced.csv"):
        self.csv_file = csv_file
        self.df = None
        self.particles = []
        self.fig = None
        self.ax = None
        
        # Try to load data
        self.load_data()
        
    def load_data(self):
        """Load CSV data"""
        import os
        
        # Try multiple possible paths
        possible_paths = [
            self.csv_file,  # Current directory
            f"HK_Labor/{self.csv_file}",  # From parent directory
            os.path.join(os.path.dirname(__file__), self.csv_file),  # Same directory as script
        ]
        
        for path in possible_paths:
            try:
                print(f"Attempting to load file: {path}")
                if os.path.exists(path):
                    self.df = pd.read_csv(path)
                    self.df['年月'] = pd.to_datetime(self.df['年月'])
                    self.df['月份索引'] = range(len(self.df))
                    print(f"✅ Successfully loaded data: {len(self.df)} rows")
                    print(f"Unemployment rate range: {self.df['失业率_百分比'].min():.1f}% - {self.df['失业率_百分比'].max():.1f}%")
                    print(f"Time range: {self.df['年月'].min().strftime('%Y-%m')} to {self.df['年月'].max().strftime('%Y-%m')}")
                    return
                else:
                    print(f"❌ File not found: {path}")
            except Exception as e:
                print(f"❌ Failed to load path {path}: {e}")
                continue
        
        print(f"❌ All paths failed, current working directory: {os.getcwd()}")
        print("Please ensure the hk_labor_enhanced.csv file exists")
    
    def create_rainbow_colors(self, n_colors):
        """Create rainbow gradient colors"""
        colors = []
        for i in range(n_colors):
            hue = i / n_colors
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            colors.append(rgb)
        return colors
    
    def create_glow_effect(self, x, y, intensity=1.0, color='cyan'):
        """Create glow effect"""
        glow_sizes = [8, 6, 4, 2]
        glow_alphas = [0.1, 0.2, 0.3, 0.5]
        
        for size, alpha in zip(glow_sizes, glow_alphas):
            alpha *= intensity
            self.ax.scatter(x, y, s=size, c=[color], alpha=alpha, marker='o', edgecolors='none')
    
    def create_particle_explosion(self, x, y, unemployment_rate, frame):
        """Create enhanced particle explosion effect"""
        # Adjust explosion scale based on unemployment rate intensity
        explosion_intensity = (unemployment_rate - 3.0) / 1.5  # 归一化到0-1
        explosion_intensity = max(0.1, min(1.0, explosion_intensity))
        
        # Particle count increases with unemployment rate
        n_particles = int(20 + explosion_intensity * 30)
        
        # Create explosion particles
        for i in range(n_particles):
            # 径向分布
            angle = (i / n_particles) * 2 * np.pi
            radius = np.random.uniform(0.5, 3.0) * explosion_intensity
            
            # Particle initial position and velocity
            particle_x = x + radius * np.cos(angle) * 0.5
            particle_y = y + radius * np.sin(angle) * 0.2
            
            # 径向速度
            speed = np.random.uniform(0.3, 1.5) * explosion_intensity
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle)
            
            # Particle properties
            particle = {
                'x': particle_x,
                'y': particle_y,
                'vx': vx,
                'vy': vy,
                'life': 1.0,
                'max_life': 1.0,
                'size': np.random.uniform(20, 60) * explosion_intensity,
                'color': self.get_explosion_color(unemployment_rate, i / n_particles),
                'birth_frame': frame
            }
            self.particles.append(particle)
    
    def get_explosion_color(self, unemployment_rate, position_ratio):
        """Get explosion color based on unemployment rate and position"""
        if unemployment_rate < 3.2:
            # 低失业率：黄色到橙色
            colors = ['yellow', 'gold', 'orange']
        elif unemployment_rate < 3.8:
            # 中等失业率：橙色到红色
            colors = ['orange', 'darkorange', 'red']
        else:
            # 高失业率：红色到深红
            colors = ['red', 'darkred', 'crimson']
        
        # 根据位置选择颜色
        color_index = int(position_ratio * len(colors))
        return colors[min(color_index, len(colors)-1)]
    
    def update_particles(self):
        """Update particle system - Enhanced explosion effects"""
        active_particles = []
        
        for particle in self.particles:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Update life value
            particle['life'] -= 0.015  # Slightly slower dissipation
            
            # Physics effects
            particle['vy'] -= 0.008  # Light gravity
            particle['vx'] *= 0.99   # Air resistance
            particle['vy'] *= 0.99
            
            # Only keep alive particles
            if particle['life'] > 0:
                # Calculate transparency and size
                life_ratio = particle['life'] / particle['max_life']
                alpha = life_ratio * 0.8  # Transparency decreases with life
                size = particle['size'] * (0.5 + 0.5 * life_ratio)  # Size decreases with life
                
                # 添加闪烁效果
                flicker = 0.8 + 0.2 * np.random.random()
                alpha *= flicker
                
                # Draw particle
                self.ax.scatter(particle['x'], particle['y'], 
                               s=size, c=particle['color'], 
                               alpha=alpha, zorder=7, 
                               edgecolors='white', linewidth=0.5)
                
                # 为即将消失的粒子添加光晕效果
                if life_ratio < 0.3:
                    glow_size = size * 2
                    glow_alpha = alpha * 0.3
                    self.ax.scatter(particle['x'], particle['y'], 
                                   s=glow_size, c='white', 
                                   alpha=glow_alpha, zorder=6)
                
                active_particles.append(particle)
        
        self.particles = active_particles
    
    def create_simple_curve_with_explosion(self, frame):
        """创建简化的曲线 + 粒子爆炸效果"""
        if self.df is None or len(self.df) == 0:
            return
        
        # 当前显示到第几个数据点
        current_point = min(frame // 2, len(self.df) - 1)
        
        if current_point < 1:
            return
        
        # 基础数据
        x_data = self.df['月份索引'][:current_point + 1]
        y_data = self.df['失业率_百分比'][:current_point + 1]
        dates = self.df['年月'][:current_point + 1]
        
        # Draw clean main curve
        self.ax.plot(x_data, y_data, 'cyan', linewidth=3, alpha=0.8, zorder=4)
        
        # Draw data points
        self.ax.scatter(x_data, y_data, c='white', s=30, zorder=5, edgecolors='cyan')
        
        # 当前点的爆炸效果
        if current_point > 0:
            current_x = x_data.iloc[-1]
            current_y = y_data.iloc[-1]
            current_rate = y_data.iloc[-1]
            current_date = dates.iloc[-1]
            
            # 每5帧创建一次爆炸
            if frame % 5 == 0:
                self.create_particle_explosion(current_x, current_y, current_rate, frame)
            
            # 当前点的脉冲效果
            pulse_size = 150 + 50 * math.sin(frame * 0.3)
            pulse_alpha = 0.4 + 0.3 * math.sin(frame * 0.3)
            
            self.ax.scatter(current_x, current_y, s=pulse_size, 
                           c='red', alpha=pulse_alpha, zorder=6)
            
            # 当前值标注
            self.ax.annotate(f'{current_y:.1f}%\n{current_date.strftime("%Y-%m")}', 
                           xy=(current_x, current_y), 
                           xytext=(15, 25), textcoords='offset points',
                           fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.9),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                                         color='white', lw=2))
    
    def create_simple_background(self, frame):
        """创建简化的背景网格"""
        # 简洁的静态网格
        for i in np.arange(0, 130, 20):
            self.ax.axvline(i, color='gray', alpha=0.2, linewidth=0.5)
        
        for y in np.arange(3.0, 4.5, 0.2):
            self.ax.axhline(y, color='gray', alpha=0.2, linewidth=0.5)
    
    def setup_plot(self):
        """Set up plotting environment"""
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        
        # Set dark background
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        
        # Set axis range
        self.ax.set_xlim(-5, 135)
        self.ax.set_ylim(3.0, 4.5)
        
        # Set labels and title
        self.ax.set_xlabel('时间进度', fontsize=14, color='white')
        self.ax.set_ylabel('失业率 (%)', fontsize=14, color='white')
        
        # Set axis color
        self.ax.tick_params(colors='white', labelsize=12)
        for spine in self.ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(2)
        
        # Add time axis labels
        if self.df is not None:
            # 每12个月显示一个年份标签
            year_indices = []
            year_labels = []
            for i in range(0, len(self.df), 12):
                year_indices.append(i)
                year_labels.append(self.df.iloc[i]['年月'].strftime('%Y'))
            
            self.ax.set_xticks(year_indices)
            self.ax.set_xticklabels(year_labels)
        
        # 添加图例区域
        legend_text = """
粒子爆炸效果:
💥 失业率越高爆炸越强
🔴 红色: 高失业率爆炸
🟠 橙色: 中等失业率爆炸  
� 黄色: 低失业率爆炸
✨ 粒子带光晕消散效果
"""
        self.ax.text(0.02, 0.98, legend_text, transform=self.ax.transAxes,
                    fontsize=10, color='cyan', va='top',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='black', 
                             edgecolor='cyan', alpha=0.8))
    
    def animate_frame(self, frame):
        """Animation frame update function"""
        if self.df is None:
            return []
        
        # Clear canvas content (preserve axes)
        self.ax.clear()
        
        # Reset axes
        self.ax.set_facecolor('black')
        self.ax.set_xlim(-5, 135)
        self.ax.set_ylim(3.0, 4.5)
        
        # Set labels and colors
        self.ax.set_xlabel('时间进度', fontsize=14, color='white')
        self.ax.set_ylabel('失业率 (%)', fontsize=14, color='white')
        self.ax.tick_params(colors='white', labelsize=12)
        
        for spine in self.ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(2)
        
        # 当前数据点
        current_point = min(frame // 2, len(self.df) - 1)
        current_data = self.df.iloc[current_point] if current_point < len(self.df) else self.df.iloc[-1]
        
        # Dynamic title
        title = f'香港失业率粒子爆炸可视化 - {current_data["年月"].strftime("%Y年%m月")}\n'
        title += f'当前失业率: {current_data["失业率_百分比"]:.1f}% | 粒子数量: {len(self.particles)}'
        
        self.ax.set_title(title, fontsize=16, fontweight='bold', 
                         color='white', pad=20)
        
        # 创建简化背景
        self.create_simple_background(frame)
        
        # 创建简化曲线和粒子爆炸
        self.create_simple_curve_with_explosion(frame)
        
        # 更新粒子系统
        self.update_particles()
        
        # 添加统计信息
        if current_point > 0:
            stats_text = f"""当前统计:
最大值: {self.df['失业率_百分比'][:current_point+1].max():.1f}%
最小值: {self.df['失业率_百分比'][:current_point+1].min():.1f}%
平均值: {self.df['失业率_百分比'][:current_point+1].mean():.2f}%
变化趋势: {"📈" if current_point > 0 and self.df.iloc[current_point]['失业率_百分比'] > self.df.iloc[current_point-1]['失业率_百分比'] else "📉"}"""
            
            self.ax.text(0.98, 0.98, stats_text, transform=self.ax.transAxes,
                        fontsize=10, color='yellow', va='top', ha='right',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='black', 
                                 edgecolor='yellow', alpha=0.8))
        
        return []
    
    def create_animation(self, interval=50, frames=None):
        """Create animation"""
        if self.df is None:
            print("Data not loaded, cannot create animation")
            return None
        
        if frames is None:
            frames = len(self.df) * 2 + 50  # 多一些帧用于结尾效果
        
        print(f"Creating animation: {frames} frames, {interval}ms interval")
        
        # Set up plotting environment
        self.setup_plot()
        
        # Create animation
        anim = FuncAnimation(self.fig, self.animate_frame, frames=frames,
                           interval=interval, blit=False, repeat=True)
        
        return anim
    
    def save_animation(self, filename="hk_unemployment_dynamic_curve.gif", 
                      fps=20, dpi=100):
        """Save animation as GIF"""
        print("Starting to create dynamic curve animation...")
        anim = self.create_animation(interval=1000//fps)
        
        if anim is None:
            return None
        
        print("Saving animation...")
        writer = PillowWriter(fps=fps)
        anim.save(filename, writer=writer, dpi=dpi)
        print(f"Animation saved as: {filename}")
        
        return anim
    
    def show_preview(self):
        """Show animation preview"""
        if self.df is None:
            return
        
        print("Showing animation preview...")
        anim = self.create_animation(interval=50)
        
        if anim is None:
            return
        
        plt.show()

def main():
    """Main function"""
    print("💥 香港失业率粒子爆炸可视化")
    print("=" * 40)
    
    # Create animator
    animator = HKUnemploymentCurveAnimator()
    
    if animator.df is None:
        print("❌ Data loading failed, program exiting")
        return
    
    print("\n✨ 粒子爆炸特效:")
    print("💥 失业率数据驱动的粒子爆炸")  
    print("� 爆炸强度随失业率变化")
    print("✨ 粒子带光晕消散效果")
    print("� 简洁清晰的曲线展示")
    print("📊 实时统计信息")
    
    print("\n选择功能:")
    print("1. Create high-quality GIF animation")
    print("2. Show real-time animation preview")
    print("3. 创建快速预览GIF")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        print("\n🎬 Creating high-quality GIF animation...")
        print("⚠️  This may take a few minutes...")
        animator.save_animation("hk_unemployment_dynamic_curve.gif", fps=15, dpi=150)
        print("✅ High-quality animation creation completed!")
        
    elif choice == "2":
        print("\n👀 Showing real-time animation preview...")
        print("💡 Close window to stop animation")
        animator.show_preview()
        
    elif choice == "3":
        print("\n⚡ Creating quick preview GIF...")
        animator.save_animation("hk_unemployment_preview.gif", fps=10, dpi=100)
        print("✅ Preview animation creation completed!")
    
    else:
        print("❌ 无效选择，显示实时预览...")
        animator.show_preview()

if __name__ == "__main__":
    main()