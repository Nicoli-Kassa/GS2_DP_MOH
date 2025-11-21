"""
DESAFIO 1 — Caminho de Valor Máximo

Objetivo: encontrar a sequência de habilidades (do estado atual até S6) que maximize o Valor
Esperado sob restrições T ≤ 350h e Cumulativo de Complexidade C ≤ 30.

Exigências técnicas:
• Modelar como DP (knapsack multidimensional: tempo e complexidade).
• Introduzir incerteza: simular V ~ Uniforme[V-10%, V+10%] em 1000 cenários (Monte Carlo).
• Maximizar E[Valor total] e relatar desvio-padrão dos resultados.
• Gerar também a solução determinística (sem incerteza) e comparar.
"""

import numpy as np
import time
import tracemalloc
from typing import Dict, List, Tuple, Any, Set, Optional
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib não disponível - gráficos desabilitados")

from gs_config import (SKILLS_DATABASE, MAX_TIME, MAX_COMPLEXITY,
                       TARGET_SKILL, N_MONTE_CARLO, print_header, GLOBAL_SEED,
                       TEMPO_MIN, COMPLEXIDADE_MIN, USE_RELAXED_CONSTRAINTS)


class ImprovedMaxValuePathDP:
    """
    Solver otimizado com DP para knapsack multidimensional.

    ALGORITMO DP - Knapsack Multidimensional:

    Estado: dp[(t, c)] = lista de {valor, skills, path}

    Transição:
    Para cada skill s em ordem topológica:
        Para cada estado (t, c):
            Se pré-requisitos satisfeitos:
                novo_estado = (t + T[s], c + C[s])
                Se novo_estado viável:
                    Adiciona {valor + V[s], skills ∪ {s}, path + [s]}

    Complexidade: O(n × T × C × k) onde k = estados por célula
    Espaço: O(T × C × k)
    """

    def __init__(self, skills_db: Dict, target: str, max_states_per_cell: int = 50):
        self.skills_db = skills_db
        self.target = target
        self.max_states_per_cell = max_states_per_cell
        self.required_skills = self._get_required_skills()
        self.min_feasible_time, self.min_feasible_complexity = self._calculate_minimum_path()

    def _get_required_skills(self) -> List[str]:
        """Obtém todas as habilidades necessárias para atingir o alvo."""
        required = set()
        to_process = [self.target]

        while to_process:
            skill = to_process.pop()
            if skill in required:
                continue
            required.add(skill)
            to_process.extend(self.skills_db[skill]['Pre_Reqs'])

        return list(required)

    def _topological_sort(self) -> List[str]:
        """Ordenação topológica das habilidades necessárias."""
        in_degree = {skill: 0 for skill in self.required_skills}

        for skill in self.required_skills:
            for prereq in self.skills_db[skill]['Pre_Reqs']:
                if prereq in in_degree:
                    in_degree[skill] += 1

        queue = [s for s in self.required_skills if in_degree[s] == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            for skill in self.required_skills:
                if current in self.skills_db[skill]['Pre_Reqs']:
                    in_degree[skill] -= 1
                    if in_degree[skill] == 0:
                        queue.append(skill)

        return result

    def _calculate_minimum_path(self) -> Tuple[int, int]:
        """Calcula caminho mínimo necessário (sem otimização de valor)."""
        acquired = set()
        total_time = 0
        total_complexity = 0

        topo_order = self._topological_sort()

        for skill_id in topo_order:
            if skill_id not in acquired:
                skill = self.skills_db[skill_id]
                total_time += skill['Tempo']
                total_complexity += skill['Complexidade']
                acquired.add(skill_id)

        return total_time, total_complexity

    def _prune_dominated_states(self, states: List[Dict]) -> List[Dict]:
        """
        Poda mais agressiva de estados dominados.

        MELHORIA: Mantém apenas top N estados por valor para economizar memória.
        """
        if len(states) <= self.max_states_per_cell:
            return states

        # Ordena por valor decrescente
        states.sort(key=lambda x: x['valor'], reverse=True)

        # Mantém apenas os melhores
        pruned = states[:self.max_states_per_cell]

        return pruned

    def solve_deterministic(self, max_time: int, max_complexity: int) -> Dict:
        """
        Resolve o problema de forma determinística usando DP.

        Returns:
            Dict com solução ótima ou mensagem de erro
        """
        print("\n   Executando DP determinístico...")

        # dp[(t, c)] = lista de estados não-dominados
        dp = defaultdict(list)
        dp[(0, 0)].append({'valor': 0, 'skills': frozenset(), 'path': []})

        topo_order = self._topological_sort()

        for skill_id in topo_order:
            skill = self.skills_db[skill_id]
            new_dp = defaultdict(list)

            # Copia estados antigos
            for key, states in dp.items():
                new_dp[key].extend(states)

            # Adiciona transições
            for (t, c), states in dp.items():
                for state in states:
                    # Verifica pré-requisitos
                    prereqs_satisfied = all(
                        p in state['skills'] for p in skill['Pre_Reqs']
                    )

                    if not prereqs_satisfied or skill_id in state['skills']:
                        continue

                    new_t = t + skill['Tempo']
                    new_c = c + skill['Complexidade']

                    if new_t <= max_time and new_c <= max_complexity:
                        new_state = {
                            'valor': state['valor'] + skill['Valor'],
                            'skills': state['skills'] | {skill_id},
                            'path': state['path'] + [skill_id]
                        }
                        new_dp[(new_t, new_c)].append(new_state)

            # Poda estados dominados
            for key in new_dp:
                new_dp[key] = self._prune_dominated_states(new_dp[key])

            dp = new_dp

        # Encontra melhor solução com target
        best_value = -1
        best_solution = None

        for states in dp.values():
            for state in states:
                if self.target in state['skills'] and state['valor'] > best_value:
                    best_value = state['valor']
                    best_solution = state

        if best_solution:
            return {
                'success': True,
                'path': best_solution['path'],
                'total_value': best_solution['valor'],
                'total_time': sum(self.skills_db[s]['Tempo'] for s in best_solution['path']),
                'total_complexity': sum(self.skills_db[s]['Complexidade'] for s in best_solution['path'])
            }

        return {
            'success': False,
            'message': f'Impossível atingir {self.target} com T≤{max_time}, C≤{max_complexity}'
        }

    def solve_with_uncertainty(self, max_time: int, max_complexity: int, 
                               n_simulations: int = 1000) -> Dict:
        """
        Resolve com incerteza usando Monte Carlo.

        MELHORIA: Adiciona análise estatística detalhada.
        """
        print(f"\n🏔️ Executando {n_simulations} simulações Monte Carlo...")

        # Primeiro obtém solução determinística
        det_solution = self.solve_deterministic(max_time, max_complexity)

        if not det_solution['success']:
            return det_solution

        path = det_solution['path']
        simulated_values = []

        np.random.seed(GLOBAL_SEED)

        for i in range(n_simulations):
            total_value = 0
            for skill_id in path:
                base_value = self.skills_db[skill_id]['Valor']
                # Valor varia ±10%
                simulated_value = base_value * np.random.uniform(0.9, 1.1)
                total_value += simulated_value

            simulated_values.append(total_value)

        return {
            'success': True,
            'path': path,
            'deterministic_value': det_solution['total_value'],
            'expected_value': np.mean(simulated_values),
            'std_value': np.std(simulated_values),
            'min_value': np.min(simulated_values),
            'max_value': np.max(simulated_values),
            'simulations': simulated_values,
            'total_time': det_solution['total_time'],
            'total_complexity': det_solution['total_complexity']
        }

    def plot_monte_carlo_distribution(self, simulations: List[float], 
                                      filename: str = 'desafio1_monte_carlo.png'):
        """
        MELHORIA: Visualiza distribuição Monte Carlo.
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️ matplotlib não disponível - pulando gráfico")
            return

        plt.figure(figsize=(10, 6))
        plt.hist(simulations, bins=50, alpha=0.7, color='#2E86AB', edgecolor='black')

        mean_val = np.mean(simulations)
        std_val = np.std(simulations)

        plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'Média: {mean_val:.2f}')
        plt.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=1.5,
                   label=f'±1σ: [{mean_val-std_val:.2f}, {mean_val+std_val:.2f}]')
        plt.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=1.5)

        plt.xlabel('Valor Total')
        plt.ylabel('Frequência')
        plt.title('Distribuição de Valores - Simulação Monte Carlo (n=1000)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        print(f"✅ Gráfico salvo: {filename}")
        plt.close()

    def check_feasibility(self, max_time: int, max_complexity: int) -> Tuple[bool, str]:
        """Verifica viabilidade das restrições."""
        if self.min_feasible_time <= max_time and self.min_feasible_complexity <= max_complexity:
            return True, "Restrições viáveis"

        return False, (f"Restrições muito rígidas! "
                      f"Mínimo necessário: T≥{self.min_feasible_time}, "
                      f"C≥{self.min_feasible_complexity}")


def run_challenge1():
    """Executa Desafio 1 completo com todas as melhorias."""
    print_header("1️⃣ DESAFIO 1: CAMINHO DE VALOR MÁXIMO")

    solver = ImprovedMaxValuePathDP(SKILLS_DATABASE, TARGET_SKILL)

    # Verifica viabilidade
    is_feasible, msg = solver.check_feasibility(MAX_TIME, MAX_COMPLEXITY)
    print(f"\n📊 Viabilidade: {msg}")

    # Usa limites ajustados se necessário
    if USE_RELAXED_CONSTRAINTS and not is_feasible:
        time_limit = solver.min_feasible_time + 50
        complexity_limit = solver.min_feasible_complexity + 6
        print(f"\n⚙️ Usando limites ajustados: T≤{time_limit}, C≤{complexity_limit}")
    else:
        time_limit = MAX_TIME
        complexity_limit = MAX_COMPLEXITY

    # Solução determinística
    start = time.time()
    det_result = solver.solve_deterministic(time_limit, complexity_limit)
    det_time = time.time() - start

    if det_result['success']:
        print(f"\n✅ SOLUÇÃO DETERMINÍSTICA (tempo: {det_time:.4f}s):")
        print(f"  Caminho: {' → '.join(det_result['path'])}")
        print(f"  Valor Total: {det_result['total_value']}")
        print(f"  Tempo: {det_result['total_time']}h")
        print(f"  Complexidade: {det_result['total_complexity']}")
    else:
        print(f"\n❌ {det_result['message']}")
        return

    # Monte Carlo
    start = time.time()
    mc_result = solver.solve_with_uncertainty(time_limit, complexity_limit, N_MONTE_CARLO)
    mc_time = time.time() - start

    print(f"\n🎲 ANÁLISE MONTE CARLO (tempo: {mc_time:.4f}s):")
    print(f"  E[Valor]: {mc_result['expected_value']:.2f}")
    print(f"  σ(Valor): {mc_result['std_value']:.2f}")
    print(f"  Range: [{mc_result['min_value']:.2f}, {mc_result['max_value']:.2f}]")
    print(f"  Coef. Variação: {mc_result['std_value']/mc_result['expected_value']*100:.2f}%")

    # Comparação
    diff = mc_result['expected_value'] - det_result['total_value']
    print(f"\n📊 COMPARAÇÃO:")
    print(f"  Determinístico: {det_result['total_value']}")
    print(f"  Estocástico E[V]: {mc_result['expected_value']:.2f}")
    print(f"  Diferença: {diff:+.2f} ({diff/det_result['total_value']*100:+.2f}%)")

    # Gera gráfico
    solver.plot_monte_carlo_distribution(mc_result['simulations'])

    return mc_result


if __name__ == "__main__":
    run_challenge1()
