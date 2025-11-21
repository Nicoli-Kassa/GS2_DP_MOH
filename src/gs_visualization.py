"""
VISUALIZAÇÃO COMPLETA - Gráficos Profissionais
VERSÃO FINAL - Todos os métodos incluídos

Gera gráficos de alta qualidade para o relatório técnico.
Otimizado para Jupyter/Colab - MOSTRA os gráficos automaticamente!
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Dict

# Configuração para Jupyter/Colab
try:
    from IPython import get_ipython
    ipython = get_ipython()
    if ipython is not None:
        ipython.run_line_magic('matplotlib', 'inline')
        print("✅ Modo inline ativado para Jupyter/Colab")
except:
    pass

try:
    import seaborn as sns
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
except ImportError:
    plt.style.use('default')

# Cores personalizadas
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'info': '#6A4C93',
    'neutral': '#6C757D',
    'acquire': '#06A77D',
    'waiting': '#F18F01'
}


class ImprovedVisualization:
    """Classe para criar visualizações profissionais."""

    @staticmethod
    def plot_monte_carlo_enhanced(simulations: List[float], 
                                  deterministic_value: float,
                                  filename: str = 'desafio1_monte_carlo_enhanced.png',
                                  show: bool = True): 
        plt.close('all')

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        mean_val = np.mean(simulations)
        std_val = np.std(simulations)
        median_val = np.median(simulations)

        # Subplot 1: Histograma com curva normal
        ax1 = axes[0]
        n, bins, patches = ax1.hist(simulations, bins=50, alpha=0.7, 
                                    color=COLORS['primary'], edgecolor='black',
                                    density=True, label='Distribuição Monte Carlo')

        mu, sigma = mean_val, std_val
        x = np.linspace(min(simulations), max(simulations), 100)
        normal_curve = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5*((x - mu)/sigma)**2)
        ax1.plot(x, normal_curve, 'r--', linewidth=2, label='Distribuição Normal Teórica')

        ax1.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'Média: {mean_val:.2f}')
        ax1.axvline(median_val, color='green', linestyle=':', linewidth=2,
                   label=f'Mediana: {median_val:.2f}')
        ax1.axvline(deterministic_value, color='purple', linestyle='-', linewidth=2,
                   label=f'Determinístico: {deterministic_value}')

        ci_lower = mean_val - 1.96 * std_val
        ci_upper = mean_val + 1.96 * std_val
        ax1.axvspan(ci_lower, ci_upper, alpha=0.2, color='orange',
                   label=f'IC 95%: [{ci_lower:.2f}, {ci_upper:.2f}]')

        ax1.set_xlabel('Valor Total', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Densidade de Probabilidade', fontsize=12, fontweight='bold')
        ax1.set_title('Distribuição de Valores - Simulação Monte Carlo (n=1000)',
                     fontsize=14, fontweight='bold', pad=20)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Subplot 2: Box plot
        ax2 = axes[1]
        parts = ax2.violinplot([simulations], positions=[1], widths=0.7,
                               showmeans=True, showmedians=True)

        for pc in parts['bodies']:
            pc.set_facecolor(COLORS['info'])
            pc.set_alpha(0.7)

        bp = ax2.boxplot([simulations], positions=[1], widths=0.3,
                         patch_artist=True, showfliers=True)

        for patch in bp['boxes']:
            patch.set_facecolor(COLORS['success'])
            patch.set_alpha(0.6)

        stats_text = f"""Estatísticas:

Média: {mean_val:.2f}
Mediana: {median_val:.2f}
Desvio Padrão: {std_val:.2f}
CV: {(std_val/mean_val)*100:.2f}%

Min: {min(simulations):.2f}
Q1: {np.percentile(simulations, 25):.2f}
Q3: {np.percentile(simulations, 75):.2f}
Max: {max(simulations):.2f}

Determinístico: {deterministic_value}
Erro: {abs(mean_val - deterministic_value):.2f}"""

        ax2.text(1.5, mean_val, stats_text, fontsize=9, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                verticalalignment='center')

        ax2.set_ylabel('Valor Total', fontsize=12, fontweight='bold')
        ax2.set_title('Análise de Dispersão', fontsize=14, fontweight='bold', pad=20)
        ax2.set_xticks([1])
        ax2.set_xticklabels(['Monte Carlo'])
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")

        if show:
            plt.show()
        else:
            plt.close()

    @staticmethod
    def plot_top3_timeline_enhanced(top3: List[Dict],
                                    filename: str = 'desafio2_top3_enhanced.png',
                                    show: bool = True):
        """GRÁFICO MELHORADO: Timeline das top 3 ordens."""
        plt.close('all')

        fig = plt.figure(figsize=(18, 10))
        gs = fig.add_gridspec(2, 2, height_ratios=[2, 1], hspace=0.3, wspace=0.3)

        ax_main = fig.add_subplot(gs[0, :])

        colors = {'waiting': COLORS['waiting'], 'acquire': COLORS['acquire']}

        max_time = 0
        for i, result in enumerate(top3):
            y_pos = 2 - i
            cumulative = 0

            for event in result['timeline']:
                width = event['time']
                color = colors[event['action']]

                ax_main.barh(y_pos, width, left=cumulative, 
                           color=color, alpha=0.8, edgecolor='black', linewidth=1)

                if width > 15:
                    label = event['skill']
                    ax_main.text(cumulative + width/2, y_pos, label, 
                               ha='center', va='center', fontsize=9, 
                               fontweight='bold', color='white')

                cumulative += width

            max_time = max(max_time, cumulative)
            ax_main.text(cumulative + 10, y_pos, f"{cumulative}h",
                        va='center', fontweight='bold', fontsize=11)

        ax_main.set_yticks([0, 1, 2])
        labels = [f"#{i+1}: {' → '.join(r['order'])}" for i, r in enumerate(top3)]
        ax_main.set_yticklabels(labels[::-1], fontsize=10)
        ax_main.set_xlabel('Tempo (horas)', fontsize=12, fontweight='bold')
        ax_main.set_title('Top 3 Ordens de Aquisição - Timeline Detalhada',
                         fontsize=16, fontweight='bold', pad=20)
        ax_main.set_xlim(0, max_time + 50)

        waiting_patch = mpatches.Patch(color=colors['waiting'], label='Espera (pré-requisitos)')
        acquire_patch = mpatches.Patch(color=colors['acquire'], label='Aquisição (crítica)')
        ax_main.legend(handles=[acquire_patch, waiting_patch], loc='upper right', fontsize=11)
        ax_main.grid(axis='x', alpha=0.3)

        ax_comp = fig.add_subplot(gs[1, 0])

        orders = [f"Ordem #{i+1}" for i in range(3)]
        waiting_times = [sum(e['time'] for e in r['timeline'] if e['action'] == 'waiting') 
                        for r in top3]
        acquire_times = [sum(e['time'] for e in r['timeline'] if e['action'] == 'acquire')
                        for r in top3]

        x = np.arange(len(orders))
        width = 0.35

        bars1 = ax_comp.bar(x - width/2, waiting_times, width, 
                           label='Tempo de Espera', color=colors['waiting'])
        bars2 = ax_comp.bar(x + width/2, acquire_times, width,
                           label='Tempo de Aquisição', color=colors['acquire'])

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax_comp.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}h', ha='center', va='bottom', fontsize=9)

        ax_comp.set_xlabel('Ordem', fontsize=11, fontweight='bold')
        ax_comp.set_ylabel('Tempo (horas)', fontsize=11, fontweight='bold')
        ax_comp.set_title('Breakdown de Tempos', fontsize=12, fontweight='bold')
        ax_comp.set_xticks(x)
        ax_comp.set_xticklabels(orders)
        ax_comp.legend(fontsize=9)
        ax_comp.grid(axis='y', alpha=0.3)

        ax_stats = fig.add_subplot(gs[1, 1])
        ax_stats.axis('off')

        stats_text = f"""ESTATÍSTICAS TOP 3

Ordem #1:
• Tempo: {top3[0]['total_time']}h
• Espera: {waiting_times[0]}h ({waiting_times[0]/top3[0]['total_time']*100:.1f}%)
• Aquisição: {acquire_times[0]}h

Ordem #2:
• Tempo: {top3[1]['total_time']}h
• Espera: {waiting_times[1]}h ({waiting_times[1]/top3[1]['total_time']*100:.1f}%)

Ordem #3:
• Tempo: {top3[2]['total_time']}h
• Espera: {waiting_times[2]}h ({waiting_times[2]/top3[2]['total_time']*100:.1f}%)

💡 Melhor ordem minimiza espera!"""

        ax_stats.text(0.1, 0.5, stats_text, fontsize=10, 
                     verticalalignment='center', family='monospace',
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")

        if show:
            plt.show()
        else:
            plt.close()

    @staticmethod
    def plot_complexity_enhanced(empirical_data: Dict,
                                filename: str = 'desafio3_complexity_enhanced.png',
                                show: bool = True):
        """GRÁFICO MELHORADO: Análise de complexidade."""
        plt.close('all')

        sizes = empirical_data['sizes']
        greedy = empirical_data['greedy_times']
        dp = empirical_data['dp_times']
        bruteforce = [t for t in empirical_data['bruteforce_times'] if t is not None]

        fig = plt.figure(figsize=(18, 10))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

        # Guloso
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(sizes, greedy, 'o-', color=COLORS['primary'], linewidth=2.5,
                markersize=8, label='Guloso (medido)', markeredgecolor='black')
        theoretical = [n * np.log2(n) * 0.01 for n in sizes]
        ax1.plot(sizes, theoretical, '--', color='red', linewidth=2,
                alpha=0.7, label='O(n log n) teórico')
        ax1.fill_between(sizes, greedy, alpha=0.3, color=COLORS['primary'])
        ax1.set_xlabel('Tamanho (n)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Tempo (ms)', fontsize=11, fontweight='bold')
        ax1.set_title('Algoritmo Guloso\nO(n log n)', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # DP
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(sizes, dp, 's-', color=COLORS['success'], linewidth=2.5,
                markersize=8, label='DP (medido)', markeredgecolor='black')
        theoretical_dp = [n * 100 * 0.0001 for n in sizes]
        ax2.plot(sizes, theoretical_dp, '--', color='orange', linewidth=2,
                alpha=0.7, label='O(n×V) teórico')
        ax2.fill_between(sizes, dp, alpha=0.3, color=COLORS['success'])
        ax2.set_xlabel('Tamanho (n)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Tempo (ms)', fontsize=11, fontweight='bold')
        ax2.set_title('Programação Dinâmica\nO(n×V)', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        # Força Bruta
        ax3 = fig.add_subplot(gs[0, 2])
        if bruteforce:
            bf_sizes = sizes[:len(bruteforce)]
            ax3.plot(bf_sizes, bruteforce, '^-', color=COLORS['danger'], 
                    linewidth=2.5, markersize=8, label='Força Bruta',
                    markeredgecolor='black')
            theoretical_bf = [2**n * 0.0005 for n in bf_sizes]
            ax3.plot(bf_sizes, theoretical_bf, '--', color='purple', linewidth=2,
                    alpha=0.7, label='O(2^n) teórico')
            ax3.fill_between(bf_sizes, bruteforce, alpha=0.3, color=COLORS['danger'])
            ax3.set_yscale('log')
        ax3.set_xlabel('Tamanho (n)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Tempo (ms, log)', fontsize=11, fontweight='bold')
        ax3.set_title('Busca Exaustiva\nO(2^n)', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)

        # Comparação
        ax4 = fig.add_subplot(gs[1, :2])
        ax4.plot(sizes, greedy, 'o-', color=COLORS['primary'], 
                linewidth=2, markersize=6, label='Guloso')
        ax4.plot(sizes, dp, 's-', color=COLORS['success'],
                linewidth=2, markersize=6, label='DP')
        if bruteforce:
            bf_sizes = sizes[:len(bruteforce)]
            ax4.plot(bf_sizes, bruteforce, '^-', color=COLORS['danger'],
                    linewidth=2, markersize=6, label='Força Bruta')
        ax4.set_xlabel('Tamanho (n)', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Tempo (ms)', fontsize=12, fontweight='bold')
        ax4.set_title('Comparação Direta', fontsize=14, fontweight='bold')
        ax4.legend(fontsize=10, loc='upper left')
        ax4.grid(True, alpha=0.3)
        ax4.set_yscale('log')

        # Resumo
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.axis('off')

        table_text = f"""RESUMO

Guloso:
• O(n log n)
• {np.mean(greedy):.3f}ms
• Heurística

DP:
• O(n×V)
• {np.mean(dp):.3f}ms
• ÓTIMO

Força Bruta:
• O(2^n)
• Explosivo
• ÓTIMO

DP = melhor!"""

        ax5.text(0.1, 0.5, table_text, fontsize=9,
                verticalalignment='center', family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

        plt.suptitle('Análise de Complexidade Computacional',
                    fontsize=16, fontweight='bold', y=0.995)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")

        if show:
            plt.show()
        else:
            plt.close()

    @staticmethod
    def plot_sorting_comparison(benchmark_results: Dict,
                               filename: str = 'desafio4_sorting_comparison.png',
                               show: bool = True):
        """
        Comparação de algoritmos de ordenação.
        
        Args:
            benchmark_results: Dict com formato:
                {
                    'algo_name': {'mean': float, 'min': float, 'max': float},
                    ...
                }
        """
        plt.close('all')

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Extrai dados
        algo_names = list(benchmark_results.keys())
        means = [benchmark_results[algo]['mean'] for algo in algo_names]
        mins = [benchmark_results[algo]['min'] for algo in algo_names]
        maxs = [benchmark_results[algo]['max'] for algo in algo_names]
        
        # Subplot 1: Tempos médios com barras de erro
        ax1 = axes[0, 0]
        x_pos = np.arange(len(algo_names))
        colors_list = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['info']]
        
        bars = ax1.bar(x_pos, means, color=colors_list[:len(algo_names)], 
                      alpha=0.7, edgecolor='black')
        
        # Adiciona barras de erro (min-max range)
        errors = [[means[i] - mins[i] for i in range(len(means))],
                  [maxs[i] - means[i] for i in range(len(means))]]
        ax1.errorbar(x_pos, means, yerr=errors, fmt='none', 
                    ecolor='black', capsize=5, capthick=2)
        
        ax1.set_xlabel('Algoritmo', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Tempo (ms)', fontsize=11, fontweight='bold')
        ax1.set_title('Tempo Médio de Execução (n=12, 100 rodadas)', 
                     fontsize=12, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(algo_names, rotation=15, ha='right')
        ax1.grid(axis='y', alpha=0.3)
        
        # Adiciona valores nas barras
        for bar, mean in zip(bars, means):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{mean:.4f}ms', ha='center', va='bottom', fontsize=8)

        # Subplot 2: Comparação min/mean/max
        ax2 = axes[0, 1]
        x = np.arange(len(algo_names))
        width = 0.25
        
        bars1 = ax2.bar(x - width, mins, width, label='Mínimo', 
                       color=COLORS['success'], alpha=0.7)
        bars2 = ax2.bar(x, means, width, label='Média',
                       color=COLORS['primary'], alpha=0.7)
        bars3 = ax2.bar(x + width, maxs, width, label='Máximo',
                       color=COLORS['danger'], alpha=0.7)
        
        ax2.set_xlabel('Algoritmo', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Tempo (ms)', fontsize=11, fontweight='bold')
        ax2.set_title('Min / Média / Max', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(algo_names, rotation=15, ha='right')
        ax2.legend(fontsize=9)
        ax2.grid(axis='y', alpha=0.3)

        # Subplot 3: Comparação relativa (normalizado pelo mais rápido)
        ax3 = axes[1, 0]
        fastest = min(means)
        relative_times = [m / fastest for m in means]
        
        bars = ax3.barh(algo_names, relative_times, 
                       color=colors_list[:len(algo_names)], 
                       alpha=0.7, edgecolor='black')
        
        ax3.axvline(1.0, color='red', linestyle='--', linewidth=2, 
                   label='Referência (mais rápido)')
        ax3.set_xlabel('Tempo Relativo (normalizado)', fontsize=11, fontweight='bold')
        ax3.set_title('Performance Relativa', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(axis='x', alpha=0.3)
        
        # Adiciona valores
        for bar, rel_time in zip(bars, relative_times):
            width = bar.get_width()
            ax3.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{rel_time:.2f}x', ha='left', va='center', 
                    fontsize=9, fontweight='bold')

        # Subplot 4: Resumo estatístico
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        summary_text = "RESUMO DOS ALGORITMOS\n\n"
        for i, algo_name in enumerate(algo_names):
            metrics = benchmark_results[algo_name]
            rel_speed = means[i] / fastest
            
            summary_text += f"{algo_name}:\n"
            summary_text += f"  Média: {metrics['mean']:.4f}ms\n"
            summary_text += f"  Min: {metrics['min']:.4f}ms\n"
            summary_text += f"  Max: {metrics['max']:.4f}ms\n"
            summary_text += f"  Variação: {metrics['max']-metrics['min']:.4f}ms\n"
            summary_text += f"  Velocidade: {rel_speed:.2f}x\n\n"
        
        fastest_algo = algo_names[means.index(fastest)]
        summary_text += f"🏆 Mais rápido: {fastest_algo}\n"
        summary_text += f"📊 Dataset: n=12 skills\n"
        summary_text += f"🔄 Rodadas: 100 execuções"
        
        ax4.text(0.1, 0.5, summary_text, fontsize=8,
                verticalalignment='center', family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

        plt.suptitle('Análise Comparativa de Algoritmos de Ordenação',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")

        if show:
            plt.show()
        else:
            plt.close()

    @staticmethod
    def plot_recommendation_analysis(greedy_result: Dict = None,
                                    optimal_result: Dict = None,
                                    dp_result: Dict = None,
                                    filename: str = 'desafio5_recommendation_analysis.png',
                                    show: bool = True):
        """
        Análise do sistema de recomendação (Desafio 5).
        
        Args:
            greedy_result: Resultado do algoritmo guloso
            optimal_result: Resultado do algoritmo ótimo (DP) - alternativa
            dp_result: Resultado do DP - alternativa
        """
        plt.close('all')
        
        # Normaliza os nomes (dp_result e optimal_result são a mesma coisa)
        if dp_result and not optimal_result:
            optimal_result = dp_result

        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

        # Subplot 1: Comparação de valores
        ax1 = fig.add_subplot(gs[0, 0])
        
        algorithms = []
        values = []
        colors_bar = []
        
        if greedy_result and 'recommendations' in greedy_result:
            # Calcula valor total das recomendações greedy
            greedy_value = sum(r.get('expected_value', 0) 
                             for r in greedy_result.get('recommendations', []))
            algorithms.append('Guloso')
            values.append(greedy_value)
            colors_bar.append(COLORS['warning'])
        
        if optimal_result and 'optimal_value' in optimal_result:
            algorithms.append('Ótimo (DP)')
            values.append(optimal_result['optimal_value'])
            colors_bar.append(COLORS['success'])
        
        if algorithms:
            bars = ax1.bar(algorithms, values, color=colors_bar, alpha=0.7, edgecolor='black')
            ax1.set_ylabel('Valor Esperado Total', fontsize=11, fontweight='bold')
            ax1.set_title('Comparação de Valores Esperados', fontsize=12, fontweight='bold')
            ax1.grid(axis='y', alpha=0.3)
            
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{val:.1f}', ha='center', va='bottom', 
                        fontsize=10, fontweight='bold')

        # Subplot 2: Skills recomendadas
        ax2 = fig.add_subplot(gs[0, 1])
        
        if greedy_result and 'recommendations' in greedy_result:
            recs = greedy_result['recommendations'][:5]  # Top 5
            skill_names = [f"{r['skill_id']}" for r in recs]
            skill_values = [r.get('expected_value', 0) for r in recs]
            
            bars = ax2.barh(skill_names, skill_values, color=COLORS['primary'], alpha=0.7)
            ax2.set_xlabel('Valor Esperado', fontsize=11, fontweight='bold')
            ax2.set_title(f'Top {len(recs)} Recomendações (Guloso)', 
                         fontsize=12, fontweight='bold')
            ax2.grid(axis='x', alpha=0.3)
            
            for bar, val in zip(bars, skill_values):
                width = bar.get_width()
                ax2.text(width, bar.get_y() + bar.get_height()/2.,
                        f' {val:.1f}', ha='left', va='center', fontsize=8)

        # Subplot 3: Comparação de scores
        ax3 = fig.add_subplot(gs[0, 2])
        
        if greedy_result and 'recommendations' in greedy_result:
            recs = greedy_result['recommendations'][:8]
            scores = [r.get('score', 0) for r in recs]
            skill_ids = [r['skill_id'] for r in recs]
            
            bars = ax3.barh(skill_ids, scores, color=COLORS['info'], alpha=0.7)
            ax3.set_xlabel('Score (E[V]/Tempo)', fontsize=11, fontweight='bold')
            ax3.set_title('Scores de Eficiência', fontsize=12, fontweight='bold')
            ax3.grid(axis='x', alpha=0.3)
            
            for bar, score in zip(bars, scores):
                width = bar.get_width()
                ax3.text(width, bar.get_y() + bar.get_height()/2.,
                        f' {score:.3f}', ha='left', va='center', fontsize=7)

        # Subplot 4: Path Ótimo (se disponível)
        ax4 = fig.add_subplot(gs[1, 0])
        
        if optimal_result and 'optimal_path' in optimal_result:
            path = optimal_result['optimal_path'][:10]  # Primeiros 10
            path_positions = list(range(len(path)))
            
            ax4.plot(path_positions, [1]*len(path), 'o-', 
                    color=COLORS['success'], linewidth=3, markersize=10)
            
            for i, skill in enumerate(path):
                ax4.text(i, 1.05, skill, ha='center', va='bottom', 
                        fontsize=8, rotation=45)
            
            ax4.set_ylim(0.8, 1.3)
            ax4.set_xlabel('Posição no Path', fontsize=11, fontweight='bold')
            ax4.set_title(f'Path Ótimo (DP) - {len(path)} skills', 
                         fontsize=12, fontweight='bold')
            ax4.set_yticks([])
            ax4.grid(axis='x', alpha=0.3)
        else:
            ax4.axis('off')
            ax4.text(0.5, 0.5, 'Path ótimo\nnão disponível', 
                    ha='center', va='center', fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))

        # Subplot 5: Comparação de tempos
        ax5 = fig.add_subplot(gs[1, 1])
        
        if optimal_result and 'optimal_time' in optimal_result:
            time_data = {'DP': optimal_result['optimal_time']}
            
            if greedy_result and 'recommendations' in greedy_result:
                greedy_time = sum(r.get('time', 0) 
                                for r in greedy_result['recommendations'])
                time_data['Guloso'] = greedy_time
            
            algorithms_time = list(time_data.keys())
            times = list(time_data.values())
            colors_time = [COLORS['warning'] if 'Guloso' in a else COLORS['success'] 
                          for a in algorithms_time]
            
            bars = ax5.bar(algorithms_time, times, color=colors_time, 
                          alpha=0.7, edgecolor='black')
            ax5.set_ylabel('Tempo Total (horas)', fontsize=11, fontweight='bold')
            ax5.set_title('Comparação de Tempo', fontsize=12, fontweight='bold')
            ax5.grid(axis='y', alpha=0.3)
            
            for bar, t in zip(bars, times):
                height = bar.get_height()
                ax5.text(bar.get_x() + bar.get_width()/2., height,
                        f'{t}h', ha='center', va='bottom', fontsize=9)
        else:
            ax5.axis('off')

        # Subplot 6: Resumo
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.axis('off')
        
        summary = "RESUMO DA RECOMENDAÇÃO\n\n"
        
        if greedy_result and 'recommendations' in greedy_result:
            n_recs = len(greedy_result['recommendations'])
            total_ev = sum(r.get('expected_value', 0) 
                          for r in greedy_result['recommendations'])
            total_time = sum(r.get('time', 0) 
                           for r in greedy_result['recommendations'])
            
            summary += f"Algoritmo Guloso:\n"
            summary += f"• Recomendações: {n_recs}\n"
            summary += f"• Valor esperado: {total_ev:.1f}\n"
            summary += f"• Tempo total: {total_time}h\n"
            if total_time > 0:
                summary += f"• Eficiência: {total_ev/total_time:.2f}\n"
            summary += "\n"
        
        if optimal_result:
            if 'optimal_value' in optimal_result:
                summary += f"Algoritmo DP:\n"
                summary += f"• Valor ótimo: {optimal_result['optimal_value']:.1f}\n"
                summary += f"• Tempo: {optimal_result.get('optimal_time', 0)}h\n"
                summary += f"• Path length: {len(optimal_result.get('optimal_path', []))}\n"
                summary += f"• Novas skills: {optimal_result.get('num_new_skills', 0)}\n\n"
            
            if greedy_result and 'recommendations' in greedy_result:
                greedy_val = sum(r.get('expected_value', 0) 
                               for r in greedy_result['recommendations'])
                opt_val = optimal_result.get('optimal_value', 0)
                
                if greedy_val > 0:
                    diff_pct = ((opt_val - greedy_val) / greedy_val * 100)
                    summary += f"Comparação:\n"
                    summary += f"• DP melhor em: {diff_pct:.1f}%\n"
        
        ax6.text(0.1, 0.5, summary, fontsize=9,
                verticalalignment='center', family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

        plt.suptitle('Análise do Sistema de Recomendação de Skills',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")

        if show:
            plt.show()
        else:
            plt.close()


__all__ = ['ImprovedVisualization']