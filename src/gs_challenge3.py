"""
DESAFIO 3 — Pivô Mais Rápido

Objetivo: alcançar adaptabilidade mínima S ≥ 15 usando apenas habilidades de nível básico
(sem pré-reqs), escolhendo iterativamente pela razão V/T.

Exigências técnicas:
• Implementar seleção gulosa e demonstrar contraexemplo onde o guloso não é ótimo.
• Comparar com uma solução ótima por busca exaustiva em subconjuntos básicos.
• Discutir complexidade e quando a heurística é aceitável.

"""

import time as time_module
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from itertools import combinations

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from gs_config import SKILLS_DATABASE, BASIC_SKILLS, MIN_ADAPTABILITY, print_header


class ImprovedAdaptabilityOptimizer:
    """
    Otimizador com análise rigorosa e visualização.
    """

    def __init__(self, skills_db: Dict, basic_skills: List[str], min_adapt: int):
        self.skills_db = skills_db
        self.basic_skills = basic_skills
        self.min_adapt = min_adapt

        # Valida que skills são realmente básicas
        for skill_id in basic_skills:
            if self.skills_db[skill_id]['Pre_Reqs']:
                raise ValueError(f"{skill_id} não é básica!")

    def greedy_solution(self, verbose: bool = True) -> Dict:
        """
        Algoritmo guloso: seleciona por maior razão Valor/Tempo.

        Complexidade: O(n log n) devido à ordenação
        """
        # Ordena por V/T decrescente
        skills_sorted = sorted(
            self.basic_skills,
            key=lambda s: self.skills_db[s]['Valor'] / self.skills_db[s]['Tempo'],
            reverse=True
        )

        selected = []
        total_value = 0
        total_time = 0

        for skill_id in skills_sorted:
            skill = self.skills_db[skill_id]
            if total_value + skill['Valor'] >= self.min_adapt:
                selected.append(skill_id)
                total_value += skill['Valor']
                total_time += skill['Tempo']
                break
            selected.append(skill_id)
            total_value += skill['Valor']
            total_time += skill['Tempo']

        return {
            'algorithm': 'Guloso (V/T)',
            'selected': selected,
            'total_value': total_value,
            'total_time': total_time,
            'num_skills': len(selected)
        }

    def optimal_solution_bruteforce(self, verbose: bool = True) -> Optional[Dict]:
        """
        Busca exaustiva: testa todas as combinações.

        Complexidade: O(2^n)
        """
        best_time = float('inf')
        best_solution = None

        # Testa todos os tamanhos possíveis
        for size in range(1, len(self.basic_skills) + 1):
            for combo in combinations(self.basic_skills, size):
                total_value = sum(self.skills_db[s]['Valor'] for s in combo)

                if total_value >= self.min_adapt:
                    total_time = sum(self.skills_db[s]['Tempo'] for s in combo)

                    if total_time < best_time:
                        best_time = total_time
                        best_solution = list(combo)

        if best_solution is None:
            return None

        return {
            'algorithm': 'Ótimo (Força Bruta)',
            'selected': best_solution,
            'total_value': sum(self.skills_db[s]['Valor'] for s in best_solution),
            'total_time': best_time,
            'num_skills': len(best_solution)
        }

    def optimal_solution_dp(self, verbose: bool = True) -> Optional[Dict]:
        """
        Programação Dinâmica: otimiza valor vs tempo.

        DP: dp[v] = (tempo_mínimo, lista_skills) para atingir valor v

        Complexidade: O(n × V_max) onde V_max = soma de todos os valores
        """
        # Inicialização
        dp = {0: (0, [])}

        for skill_id in self.basic_skills:
            skill = self.skills_db[skill_id]
            new_dp = dp.copy()

            for current_value, (current_time, current_skills) in dp.items():
                new_value = current_value + skill['Valor']
                new_time = current_time + skill['Tempo']
                new_skills = current_skills + [skill_id]

                # Atualiza se for melhor
                if new_value not in new_dp or new_time < new_dp[new_value][0]:
                    new_dp[new_value] = (new_time, new_skills)

            dp = new_dp

        # Encontra menor tempo que atinge min_adapt
        best_time = float('inf')
        best_solution = None
        best_value = 0

        for value, (time, skills) in dp.items():
            if value >= self.min_adapt and time < best_time:
                best_time = time
                best_solution = skills
                best_value = value

        # CORREÇÃO: Retorna None se não encontrou solução
        if best_solution is None:
            return None

        return {
            'algorithm': 'Ótimo (DP)',
            'selected': best_solution,
            'total_value': best_value,
            'total_time': best_time,
            'num_skills': len(best_solution)
        }

    def demonstrate_counterexample(self) -> Dict:
        """
        Demonstra contraexemplo onde guloso falha.
        """
        counterexample = {
            'database': {
                'A': {'Valor': 16, 'Tempo': 10},
                'B': {'Valor': 12, 'Tempo': 7},
                'C': {'Valor': 8, 'Tempo': 4},
            },
            'min_adaptability': 16,
            'greedy_solution': {
                'choice': ['C', 'B'],  # V/T: C=2.0, B≈1.71
                'time': 11,
                'value': 20
            },
            'optimal_solution': {
                'choice': ['A'],
                'time': 10,
                'value': 16
            },
            'explanation': (
                "Guloso escolhe C (V/T=2.0) e B (V/T≈1.71) por terem maiores razões V/T, "
                "resultando em tempo total de 11h. "
                "Porém, a solução ÓTIMA escolhe apenas A (tempo=10h), "
                "que sozinha atinge o mínimo requerido."
            )
        }

        return counterexample

    def empirical_complexity_analysis(self, max_size: int = 15) -> Dict:
        """
        Análise empírica de complexidade.
        """
        print("\n📊 Análise Empírica de Complexidade...")

        results = {
            'sizes': [],
            'greedy_times': [],
            'dp_times': [],
            'bruteforce_times': []
        }

        for n in range(3, min(max_size + 1, len(self.basic_skills) + 1)):
            subset = self.basic_skills[:n]
            temp_optimizer = ImprovedAdaptabilityOptimizer(
                self.skills_db, subset, self.min_adapt
            )

            # Guloso
            start = time_module.time()
            temp_optimizer.greedy_solution(verbose=False)
            greedy_time = (time_module.time() - start) * 1000  # ms

            # DP
            start = time_module.time()
            dp_result = temp_optimizer.optimal_solution_dp(verbose=False)
            dp_time = (time_module.time() - start) * 1000

            # Força bruta (apenas para n pequeno)
            if n <= 12:
                start = time_module.time()
                bf_result = temp_optimizer.optimal_solution_bruteforce(verbose=False)
                bf_time = (time_module.time() - start) * 1000
            else:
                bf_time = None

            results['sizes'].append(n)
            results['greedy_times'].append(greedy_time)
            results['dp_times'].append(dp_time)
            results['bruteforce_times'].append(bf_time)

            print(f"  n={n}: Guloso={greedy_time:.3f}ms, DP={dp_time:.3f}ms" +
                  (f", BF={bf_time:.3f}ms" if bf_time else ""))

        return results

    def plot_complexity_analysis(self, empirical_data: Dict,
                                 filename: str = 'desafio3_complexity.png'):
        """
        MELHORIA: Gráfico empírico vs teórico.
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️ matplotlib não disponível - pulando gráfico")
            return

        sizes = empirical_data['sizes']
        greedy = empirical_data['greedy_times']
        dp = empirical_data['dp_times']
        bruteforce = [t for t in empirical_data['bruteforce_times'] if t is not None]

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # Guloso: O(n log n)
        ax1 = axes[0]
        ax1.plot(sizes, greedy, 'o-', color='#2E86AB', linewidth=2, 
                markersize=6, label='Guloso (medido)')
        theoretical_greedy = [n * np.log2(n) * 0.01 for n in sizes]
        ax1.plot(sizes, theoretical_greedy, '--', color='red', linewidth=1.5,
                label='O(n log n) teórico')
        ax1.set_xlabel('Tamanho (n)')
        ax1.set_ylabel('Tempo (ms)')
        ax1.set_title('Algoritmo Guloso')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # DP: O(n × V)
        ax2 = axes[1]
        ax2.plot(sizes, dp, 's-', color='#06A77D', linewidth=2,
                markersize=6, label='DP (medido)')
        theoretical_dp = [n * 100 * 0.0001 for n in sizes]
        ax2.plot(sizes, theoretical_dp, '--', color='orange', linewidth=1.5,
                label='O(n×V) teórico')
        ax2.set_xlabel('Tamanho (n)')
        ax2.set_ylabel('Tempo (ms)')
        ax2.set_title('Programação Dinâmica')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Força Bruta: O(2^n)
        ax3 = axes[2]
        if bruteforce:
            bf_sizes = sizes[:len(bruteforce)]
            ax3.plot(bf_sizes, bruteforce, '^-', color='#C73E1D', linewidth=2,
                    markersize=6, label='Força Bruta (medido)')
            theoretical_bf = [2**n * 0.0005 for n in bf_sizes]
            ax3.plot(bf_sizes, theoretical_bf, '--', color='purple', linewidth=1.5,
                    label='O(2^n) teórico')
            ax3.set_yscale('log')
            ax3.set_xlabel('Tamanho (n)')
            ax3.set_ylabel('Tempo (ms, escala log)')
            ax3.set_title('Busca Exaustiva')
            ax3.legend()
            ax3.grid(True, alpha=0.3)

        plt.suptitle('Análise de Complexidade Computacional', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")
        plt.close()

    def compare_solutions(self):
        """Compara as três abordagens."""
        print("\n🔬 COMPARAÇÃO DE SOLUÇÕES:")

        # Guloso
        start = time_module.time()
        greedy = self.greedy_solution(verbose=False)
        greedy_time = time_module.time() - start

        # DP
        start = time_module.time()
        dp = self.optimal_solution_dp(verbose=False)
        dp_time = time_module.time() - start

        # Força bruta (só se pequeno)
        if len(self.basic_skills) <= 12:
            start = time_module.time()
            bruteforce = self.optimal_solution_bruteforce(verbose=False)
            bf_time = time_module.time() - start
        else:
            bruteforce = None
            bf_time = None

        print(f"\n  GULOSO:")
        print(f"    Skills: {greedy['selected']}")
        print(f"    Tempo: {greedy['total_time']}h")
        print(f"    Valor: {greedy['total_value']}")
        print(f"    Execução: {greedy_time*1000:.3f}ms")

        if dp:
            print(f"\n  ÓTIMO (DP):")
            print(f"    Skills: {dp['selected']}")
            print(f"    Tempo: {dp['total_time']}h")
            print(f"    Valor: {dp['total_value']}")
            print(f"    Execução: {dp_time*1000:.3f}ms")
        else:
            print(f"\n  ÓTIMO (DP): Nenhuma solução encontrada")

        if bruteforce:
            print(f"\n  ÓTIMO (Força Bruta):")
            print(f"    Skills: {bruteforce['selected']}")
            print(f"    Tempo: {bruteforce['total_time']}h")
            print(f"    Valor: {bruteforce['total_value']}")
            print(f"    Execução: {bf_time*1000:.3f}ms")

        # Análise
        if dp and greedy['total_time'] == dp['total_time']:
            print(f"\n  ✅ Guloso encontrou solução ÓTIMA!")
        elif dp:
            diff = greedy['total_time'] - dp['total_time']
            pct = (diff / dp['total_time']) * 100
            print(f"\n  ⚠️ Guloso subótimo: +{diff}h (+{pct:.1f}%)")


def run_challenge3():
    """Executa Desafio 3 completo com melhorias."""
    print_header("3️⃣ DESAFIO 3: PIVÔ MAIS RÁPIDO (MELHORADO)")

    optimizer = ImprovedAdaptabilityOptimizer(SKILLS_DATABASE, BASIC_SKILLS, MIN_ADAPTABILITY)

    # Comparação de soluções
    optimizer.compare_solutions()

    # Contraexemplo
    print("\n" + "="*80)
    print("CONTRAEXEMPLO: GULOSO NEM SEMPRE É ÓTIMO")
    print("="*80)
    counter = optimizer.demonstrate_counterexample()
    print(f"\n{counter['explanation']}")

    # Análise empírica (com tratamento de erro)
    try:
        empirical = optimizer.empirical_complexity_analysis()
        optimizer.plot_complexity_analysis(empirical)
    except Exception as e:
        print(f"\n⚠️ Análise empírica pulada: {e}")

    return optimizer


if __name__ == "__main__":
    run_challenge3()
