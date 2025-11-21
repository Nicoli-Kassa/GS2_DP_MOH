"""
DESAFIO 2 — Verificação Crítica

Objetivo: considerando as 5 Habilidades Críticas (S3, S5, S7, S8, S9), enumerar as 120
permutações e calcular o custo total (Tempo de Aquisição + Espera por pré-reqs).

Exigências técnicas:
• Antes de calcular custos, validar o grafo: detectar ciclos e nós com pré-requisitos inexistentes.
• Se houver ciclo, reportar e interromper com mensagem de erro tratada.
• Comparar custo médio entre as três melhores ordens e justificar heurísticas observadas.
"""

import itertools
import time
from typing import Dict, List, Tuple, Set
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from gs_config import SKILLS_DATABASE, CRITICAL_SKILLS, print_header


class ImprovedCriticalSkillsAnalyzer:
    """
    Analisador melhorado com visualização e análise profunda.
    """

    def __init__(self, skills_db: Dict, critical_ids: List[str]):
        self.skills_db = skills_db
        self.critical_ids = critical_ids

        if len(critical_ids) != 5:
            raise ValueError(f"Esperadas 5 habilidades críticas, recebidas {len(critical_ids)}")

        self._precompute_dependencies()

    def _precompute_dependencies(self):
        """Pré-calcula todas as dependências."""
        self.all_prereqs = {}

        for skill_id in self.critical_ids:
            prereqs = set()
            to_process = [skill_id]

            while to_process:
                current = to_process.pop()
                for prereq in self.skills_db[current]['Pre_Reqs']:
                    if prereq not in prereqs:
                        prereqs.add(prereq)
                        to_process.append(prereq)

            self.all_prereqs[skill_id] = prereqs

    def calculate_acquisition_time(self, order: Tuple[str]) -> Dict:
        """
        Calcula tempo total considerando pré-requisitos. 
        """
        acquired_skills = set()
        total_time = 0
        timeline = []

        for skill_id in order:
            # Identifica pré-requisitos faltantes
            required_prereqs = self.all_prereqs[skill_id] - acquired_skills

            # Adquire pré-requisitos (tempo de espera)
            for prereq in required_prereqs:
                prereq_time = self.skills_db[prereq]['Tempo']
                total_time += prereq_time
                acquired_skills.add(prereq)
                timeline.append({
                    'skill': prereq,
                    'time': prereq_time,
                    'action': 'waiting',
                    'for_skill': skill_id
                })

            # Adquire habilidade crítica
            skill_time = self.skills_db[skill_id]['Tempo']
            total_time += skill_time
            acquired_skills.add(skill_id)
            timeline.append({
                'skill': skill_id,
                'time': skill_time,
                'action': 'acquire',
                'for_skill': skill_id
            })

        return {
            'order': order,
            'total_time': total_time,
            'timeline': timeline,
            'total_skills': len(acquired_skills)
        }

    def analyze_all_permutations(self) -> Dict:
        """Analisa todas as 120 permutações."""
        print("\n🔄 Analisando 120 permutações...")

        start = time.time()
        results = []

        for perm in itertools.permutations(self.critical_ids):
            result = self.calculate_acquisition_time(perm)
            results.append(result)

        elapsed = time.time() - start

        # Ordena por tempo
        results.sort(key=lambda x: x['total_time'])

        # Estatísticas
        times = [r['total_time'] for r in results]

        return {
            'all_results': results,
            'best': results[0],
            'worst': results[-1],
            'top3': results[:3],
            'statistics': {
                'mean': sum(times) / len(times),
                'std': (sum((t - sum(times)/len(times))**2 for t in times) / len(times))**0.5,
                'min': min(times),
                'max': max(times),
                'range': max(times) - min(times)
            },
            'execution_time': elapsed
        }

    def analyze_dependency_impact(self):
        """
         Análise do impacto de pré-requisitos compartilhados.
        """
        print("\n📊 ANÁLISE DE DEPENDÊNCIAS:")

        prereq_usage = defaultdict(list)

        for skill in self.critical_ids:
            for prereq in self.all_prereqs[skill]:
                prereq_usage[prereq].append(skill)

        # Pré-requisitos compartilhados
        shared = {p: deps for p, deps in prereq_usage.items() if len(deps) > 1}

        if shared:
            print("\n  🔗 PRÉ-REQUISITOS COMPARTILHADOS:")
            for prereq, dependents in sorted(shared.items(), 
                                            key=lambda x: len(x[1]), 
                                            reverse=True):
                skill_data = self.skills_db[prereq]
                print(f"    {prereq} ({skill_data['Nome']}):")
                print(f"      Usado por {len(dependents)} skills: {', '.join(dependents)}")
                print(f"      Tempo: {skill_data['Tempo']}h")
                print(f"      Impacto: Adquirir cedo economiza tempo!")
        else:
            print("  Nenhum pré-requisito compartilhado.")

        # Habilidades com mais dependências
        print("\n  📈 HABILIDADES POR COMPLEXIDADE DE DEPENDÊNCIAS:")
        for skill in sorted(self.critical_ids, 
                           key=lambda s: len(self.all_prereqs[s]), 
                           reverse=True):
            prereqs = self.all_prereqs[skill]
            print(f"    {skill}: {len(prereqs)} dependências → {sorted(prereqs)}")

    def identify_heuristics(self, top3: List[Dict]) -> List[str]:
        """Identifica heurísticas nos top 3."""
        heuristics = []

        # H1: Skills com menos dependências primeiro
        avg_prereqs_first = []
        for result in top3:
            order = result['order']
            prereqs_count = [len(self.all_prereqs[s]) for s in order[:2]]
            avg_prereqs_first.append(sum(prereqs_count) / len(prereqs_count))

        if all(x < 3 for x in avg_prereqs_first):
            heuristics.append("Iniciar com skills de MENOS dependências")

        # H2: Skills com pré-requisitos compartilhados cedo
        shared_prereqs = defaultdict(int)
        for skill in self.critical_ids:
            for prereq in self.all_prereqs[skill]:
                for other_skill in self.critical_ids:
                    if skill != other_skill and prereq in self.all_prereqs[other_skill]:
                        shared_prereqs[skill] += 1

        for result in top3:
            order = result['order']
            if order[0] in shared_prereqs and shared_prereqs[order[0]] > 0:
                heuristics.append("Priorizar skills com pré-requisitos compartilhados")
                break

        # H3: Ordenação por tempo de aquisição
        for result in top3:
            order = result['order']
            times = [self.skills_db[s]['Tempo'] for s in order[:3]]
            if times == sorted(times):
                heuristics.append("Ordenar por tempo CRESCENTE de aquisição")
                break

        return heuristics

    def plot_top3_comparison(self, top3: List[Dict], 
                            filename: str = 'desafio2_top3.png'):
        """
        Visualização gráfica das top 3 ordens.
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️ matplotlib não disponível - pulando gráfico")
            return

        fig, ax = plt.subplots(figsize=(14, 8))

        colors = {
            'waiting': '#F18F01',  # Laranja
            'acquire': '#06A77D'   # Verde
        }

        for i, result in enumerate(top3):
            y_pos = i
            cumulative = 0

            for event in result['timeline']:
                width = event['time']
                color = colors[event['action']]

                # Barra
                rect = ax.barh(y_pos, width, left=cumulative, 
                              color=color, alpha=0.8, edgecolor='black', linewidth=0.5)

                # Label se barra for grande o suficiente
                if width > 10:
                    label = event['skill']
                    ax.text(cumulative + width/2, y_pos, label, 
                           ha='center', va='center', fontsize=8, fontweight='bold')

                cumulative += width

        # Configuração dos eixos
        ax.set_yticks(range(3))
        labels = [
            f"#{i+1}: {r['order']} → {r['total_time']}h" 
            for i, r in enumerate(top3)
        ]
        ax.set_yticklabels(labels, fontsize=10)
        ax.set_xlabel('Tempo (horas)', fontsize=12)
        ax.set_title('Top 3 Ordens de Aquisição de Habilidades Críticas', 
                    fontsize=14, fontweight='bold')

        # Legenda
        waiting_patch = mpatches.Patch(color=colors['waiting'], label='Espera (pré-requisitos)')
        acquire_patch = mpatches.Patch(color=colors['acquire'], label='Aquisição (crítica)')
        ax.legend(handles=[acquire_patch, waiting_patch], loc='lower right')

        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo: {filename}")
        plt.close()

    def print_detailed_results(self, analysis: Dict):
        """Imprime resultados detalhados."""
        stats = analysis['statistics']
        top3 = analysis['top3']

        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"  Média: {stats['mean']:.2f}h")
        print(f"  Desvio Padrão: {stats['std']:.2f}h")
        print(f"  Mínimo: {stats['min']:.2f}h")
        print(f"  Máximo: {stats['max']:.2f}h")
        print(f"  Range: {stats['range']:.2f}h")
        print(f"  Tempo de execução: {analysis['execution_time']:.4f}s")

        print(f"\n🏆 TOP 3 ORDENS:")
        for i, result in enumerate(top3, 1):
            print(f"\n  #{i}: {' → '.join(result['order'])}")
            print(f"      Tempo Total: {result['total_time']}h")
            print(f"      Skills Adquiridas: {result['total_skills']}")

            # Breakdown
            waiting_time = sum(e['time'] for e in result['timeline'] if e['action'] == 'waiting')
            acquire_time = sum(e['time'] for e in result['timeline'] if e['action'] == 'acquire')
            print(f"      Breakdown: {waiting_time}h (espera) + {acquire_time}h (críticas)")

        # Heurísticas
        heuristics = self.identify_heuristics(top3)
        if heuristics:
            print(f"\n💡 HEURÍSTICAS IDENTIFICADAS:")
            for h in heuristics:
                print(f"  • {h}")


def run_challenge2():
    """Executa Desafio 2 completo com melhorias."""
    print_header("2️⃣ DESAFIO 2: VERIFICAÇÃO CRÍTICA (MELHORADO)")

    analyzer = ImprovedCriticalSkillsAnalyzer(SKILLS_DATABASE, CRITICAL_SKILLS)

    # Análise de dependências
    analyzer.analyze_dependency_impact()

    # Análise de permutações
    analysis = analyzer.analyze_all_permutations()

    # Resultados detalhados
    analyzer.print_detailed_results(analysis)

    # Visualização
    analyzer.plot_top3_comparison(analysis['top3'])

    return analysis


if __name__ == "__main__":
    run_challenge2()
