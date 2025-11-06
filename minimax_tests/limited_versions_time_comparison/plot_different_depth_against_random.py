import matplotlib.pyplot as plt
import numpy as np
import json


# CREATE TWO mean+SD PLOTS (TIME AND NUMBER OF MOVES) WITH WIN RATE TAGS
def plot_benchmark(results, save_path=None):
    # TWO PLOTS ON THE SAME FIGURE
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    depths = list(results.keys())
    x_pos = np.arange(len(depths))

    # PREPARE DATA
    avg_times = [results[d]['avg_time_per_ai_move'] for d in depths]
    std_times = [results[d]['std_time_per_ai_move'] for d in depths]
    avg_moves = [results[d]['avg_ai_moves_per_game'] for d in depths]
    std_moves = [results[d]['std_ai_moves_per_game'] for d in depths]
    win_rates = [results[d]['win_rate'] for d in depths]

    # PLOT 1: Computation Time
    ax1.errorbar(x_pos, avg_times, yerr=std_times, capsize=5, capthick=2,
                 color='darkred', alpha=0.8, linewidth=2.5, marker='o', markersize=8,
                 markerfacecolor='darkred', markeredgecolor='black', markeredgewidth=1)
    ax1.set_title('Computation Time per AI Move\n(Mean ± Standard Deviation)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Search Depth', fontsize=12)
    ax1.set_ylabel('Time (seconds)', fontsize=12)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f'Depth {d}' for d in depths])

    # ADD WIN RATE ABOVE (moved higher)
    for i, (x, y, win_rate) in enumerate(zip(x_pos, avg_times, win_rates)):
        ax1.text(x, y + std_times[i] + max(std_times) * 0.4,
                 f'{win_rate:.1f}% Win', ha='center', va='bottom', fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

    # PLOT 2: Number of Moves
    ax2.errorbar(x_pos, avg_moves, yerr=std_moves, capsize=5, capthick=2,
                 color='darkblue', alpha=0.8, linewidth=2.5, marker='s', markersize=8,
                 markerfacecolor='darkblue', markeredgecolor='black', markeredgewidth=2)
    ax2.set_title('AI Moves per Game\n(Mean ± Standard Deviation)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Search Depth', fontsize=12)
    ax2.set_ylabel('Number of Moves', fontsize=12)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f'Depth {d}' for d in depths])

    # ADD WIN RATE ABOVE (moved higher)
    for i, (x, y, win_rate) in enumerate(zip(x_pos, avg_moves, win_rates)):
        ax2.text(x, y + std_moves[i] + max(std_moves) * 0.4,
                 f'{win_rate:.1f}% Win', ha='center', va='bottom', fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

    # ADD VALUE LABELS BELOW the data points
    for i, (v, std) in enumerate(zip(avg_times, std_times)):
        ax1.text(i, v + std + max(std_times) * 0.2, f'{v:.3f}',
                 ha='center', va='top', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

    for i, (v, std) in enumerate(zip(avg_moves, std_moves)):
        ax2.text(i, v + std + max(std_moves) * 0.2, f'{v:.3f}',
                 ha='center', va='top', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

    # ADJUST x-LIMITS
    ax1.set_xlim(-0.3, len(depths) - 0.65)
    ax2.set_xlim(-0.3, len(depths) - 0.65)

    # ADJUST y-LIMITS
    ax1.set_ylim(min(avg_times) - max(std_times) * 0.3, max(avg_times) + max(std_times) + max(std_times) * 1.2)
    ax2.set_ylim(min(avg_moves) - max(std_moves) * 0.3, max(avg_moves) + max(std_moves) + max(std_moves) * 1.2)

    # ADD GRID
    ax1.grid(True, alpha=0.3, axis='y')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
    # LOAD RESULTS FROM JSON
    with open('output_files/game_results.json', 'r') as f:
        game_results = json.load(f)

    # CREATE AND SAVE PLOTS IN DIFFERENT FORMATS
    plot_benchmark(game_results, save_path='output_files/benchmark_results.png')
