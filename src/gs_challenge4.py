"""
DESAFIO 4 — Trilhas Paralelas

Objetivo: ordenar as 12 habilidades por Complexidade C usando Merge Sort ou Quick Sort
implementado por você. Dividir o resultado em Sprint A (1–6) e Sprint B (7–12).

Exigências técnicas:
• Justificar a escolha do algoritmo e suas complexidades (melhor, médio, pior caso).
• Comparar tempos medidos entre a sua implementação e o sort nativo (apenas como baseline)
"""

import time
import random
from typing import List, Tuple, Dict

from gs_config import SKILLS_DATABASE, print_header, GLOBAL_SEED


class ImprovedSortingAlgorithms:
    """
    Implementações otimizadas com análise profunda.
    """

    @staticmethod
    def merge_sort(arr: List[Tuple], key_func=lambda x: x[1]) -> List[Tuple]:
        """
        Merge Sort - Estável e O(n log n) garantido.

        VANTAGENS:
        - Complexidade O(n log n) no pior caso
        - Estável (mantém ordem relativa)
        - Cache-friendly (acesso sequencial)

        DESVANTAGENS:
        - Usa O(n) memória extra

        Complexidade:
        - Tempo: O(n log n) todos os casos
        - Espaço: O(n)
        """
        if len(arr) <= 1:
            return arr

        # Divide
        mid = len(arr) // 2
        left = ImprovedSortingAlgorithms.merge_sort(arr[:mid], key_func)
        right = ImprovedSortingAlgorithms.merge_sort(arr[mid:], key_func)

        # Conquista (merge)
        return ImprovedSortingAlgorithms._merge(left, right, key_func)

    @staticmethod
    def _merge(left: List[Tuple], right: List[Tuple], key_func) -> List[Tuple]:
        """Merge de duas listas ordenadas."""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def quick_sort(arr: List[Tuple], key_func=lambda x: x[1]) -> List[Tuple]:
        """
        Quick Sort - List comprehension (não in-place).

        VANTAGENS:
        - Simples de implementar
        - O(n log n) caso médio
        - Cache-friendly com pivô mediana-de-três

        DESVANTAGENS:
        - O(n²) no pior caso
        - Não estável
        - Esta versão usa memória extra

        Complexidade:
        - Tempo: O(n log n) médio, O(n²) pior caso
        - Espaço: O(log n) devido à recursão
        """
        if len(arr) <= 1:
            return arr

        # Pivô aleatório
        pivot_idx = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_idx]
        pivot_val = key_func(pivot)

        # Particiona
        less = [x for x in arr if key_func(x) < pivot_val]
        equal = [x for x in arr if key_func(x) == pivot_val]
        greater = [x for x in arr if key_func(x) > pivot_val]

        return (ImprovedSortingAlgorithms.quick_sort(less, key_func) +
                equal +
                ImprovedSortingAlgorithms.quick_sort(greater, key_func))

    @staticmethod
    def quick_sort_inplace(arr: List[Tuple], key_func=lambda x: x[1]) -> List[Tuple]:
        """
        Complexidade:
        - Tempo: O(n log n) médio, O(n²) pior caso
        - Espaço: O(log n) para recursão
        """
        # Copia para não modificar original
        result = arr.copy()

        def partition(low: int, high: int) -> int:
            """Particiona e retorna posição do pivô."""
            # Pivô aleatório para evitar pior caso
            pivot_idx = random.randint(low, high)
            result[pivot_idx], result[high] = result[high], result[pivot_idx]

            pivot = key_func(result[high])
            i = low - 1

            for j in range(low, high):
                if key_func(result[j]) <= pivot:
                    i += 1
                    result[i], result[j] = result[j], result[i]

            result[i + 1], result[high] = result[high], result[i + 1]
            return i + 1

        def quick_sort_recursive(low: int, high: int):
            """Ordenação recursiva."""
            if low < high:
                pi = partition(low, high)
                quick_sort_recursive(low, pi - 1)
                quick_sort_recursive(pi + 1, high)

        quick_sort_recursive(0, len(result) - 1)
        return result


class SprintDivider:
    """
    Divisor de sprints com análise de balanceamento.
    """

    def __init__(self, skills_db: Dict):
        self.skills_db = skills_db

    def prepare_data(self) -> List[Tuple]:
        """Prepara dados para ordenação."""
        return [(sid, self.skills_db[sid]['Complexidade']) 
                for sid in self.skills_db.keys()]

    def divide_sprints(self, sorted_skills: List[Tuple]) -> Dict:
        """
        Divide em dois sprints.

        Sprint A: 1-6 (primeiros)
        Sprint B: 7-12 (últimos)
        """
        sprint_a = sorted_skills[:6]
        sprint_b = sorted_skills[6:12]

        # Calcula métricas
        a_time = sum(self.skills_db[s[0]]['Tempo'] for s in sprint_a)
        a_value = sum(self.skills_db[s[0]]['Valor'] for s in sprint_a)
        a_complexity = [s[1] for s in sprint_a]

        b_time = sum(self.skills_db[s[0]]['Tempo'] for s in sprint_b)
        b_value = sum(self.skills_db[s[0]]['Valor'] for s in sprint_b)
        b_complexity = [s[1] for s in sprint_b]

        return {
            'sprint_a': {
                'skills': [s[0] for s in sprint_a],
                'complexities': a_complexity,
                'total_time': a_time,
                'total_value': a_value,
                'complexity_range': (min(a_complexity), max(a_complexity))
            },
            'sprint_b': {
                'skills': [s[0] for s in sprint_b],
                'complexities': b_complexity,
                'total_time': b_time,
                'total_value': b_value,
                'complexity_range': (min(b_complexity), max(b_complexity))
            }
        }

    def analyze_sprint_balance(self, sprints: Dict):
        """
        Análise detalhada do balanceamento.
        """
        a = sprints['sprint_a']
        b = sprints['sprint_b']

        time_ratio = a['total_time'] / b['total_time'] if b['total_time'] > 0 else 0
        value_ratio = a['total_value'] / b['total_value'] if b['total_value'] > 0 else 0
        complexity_gap = abs(a['complexity_range'][1] - b['complexity_range'][0])

        print("\n⚖️ ANÁLISE DE BALANCEAMENTO:")
        print(f"\n  Sprint A:")
        print(f"    Tempo total: {a['total_time']}h")
        print(f"    Valor total: {a['total_value']}")
        print(f"    Range complexidade: {a['complexity_range']}")

        print(f"\n  Sprint B:")
        print(f"    Tempo total: {b['total_time']}h")
        print(f"    Valor total: {b['total_value']}")
        print(f"    Range complexidade: {b['complexity_range']}")

        print(f"\n  Métricas:")
        print(f"    Razão de Tempo (A/B): {time_ratio:.2f}:1")
        print(f"    Razão de Valor (A/B): {value_ratio:.2f}:1")
        print(f"    Gap de Complexidade: {complexity_gap}")

        # Avaliação
        if 0.8 <= time_ratio <= 1.2:
            print(f"    ✅ Sprints bem balanceados em tempo")
        else:
            print(f"    ⚠️ Desbalanceamento de tempo detectado")

        if complexity_gap <= 1:
            print(f"    ✅ Transição suave de complexidade")
        else:
            print(f"    ℹ️ Gap de complexidade = {complexity_gap}")

    def print_algorithm_justification(self):
        """
        Justificativa detalhada da escolha.
        """
        print("\n" + "="*80)
        print("         JUSTIFICATIVA DA ESCOLHA DO ALGORITMO")
        print("="*80)

        print("\n📚 MERGE SORT foi escolhido pelos seguintes motivos:")

        print("\n1. GARANTIAS DE COMPLEXIDADE:")
        print("   • Merge Sort: O(n log n) SEMPRE (melhor, médio e pior caso)")
        print("   • Quick Sort: O(n log n) médio, mas O(n²) no pior caso")
        print("   • Para n=12: diferença prática é mínima, mas Merge é PREVISÍVEL")

        print("\n2. ESTABILIDADE:")
        print("   • Merge Sort: ESTÁVEL (mantém ordem de elementos iguais)")
        print("   • Quick Sort: NÃO estável (nossa implementação)")
        print("   • Importância: Se duas skills têm mesma Complexidade,")
        print("     a ordem alfabética/original é preservada")

        print("\n3. CARACTERÍSTICAS DE CACHE:")
        print("   • Merge Sort: acesso sequencial aos dados (cache-friendly)")
        print("   • Quick Sort: acesso mais aleatório (cache misses)")
        print("   • Para n pequeno: diferença é negligível")
        print("   • Para n grande: Merge pode ser mais rápido na prática")

        print("\n4. IMPLEMENTAÇÃO:")
        print("   • Merge Sort: código mais simples e claro")
        print("   • Quick Sort in-place: requer cuidado com índices e particionamento")
        print("   • Merge Sort: menos propenso a bugs")

        print("\n5. CONTEXTO DO PROBLEMA:")
        print("   • Dataset: apenas 12 skills")
        print("   • Frequência: operação executada poucas vezes")
        print("   • Conclusão: CONFIABILIDADE > pequeno ganho de performance")

        print("\n💡 DECISÃO FINAL:")
        print("   Merge Sort é a escolha mais ADEQUADA para este problema,")
        print("   priorizando previsibilidade, estabilidade e clareza.")


def benchmark_sorting(n_runs: int = 100) -> Dict:
    """Benchmark dos algoritmos."""
    print(f"\n🔬 Executando benchmark ({n_runs} rodadas)...")

    data = [(sid, SKILLS_DATABASE[sid]['Complexidade']) 
            for sid in SKILLS_DATABASE.keys()]

    # Merge Sort
    merge_times = []
    for _ in range(n_runs):
        start = time.time()
        ImprovedSortingAlgorithms.merge_sort(data.copy())
        merge_times.append((time.time() - start) * 1000)

    # Quick Sort (list comprehension)
    quick_times = []
    for _ in range(n_runs):
        start = time.time()
        ImprovedSortingAlgorithms.quick_sort(data.copy())
        quick_times.append((time.time() - start) * 1000)

    # Quick Sort (in-place)
    quick_inplace_times = []
    for _ in range(n_runs):
        start = time.time()
        ImprovedSortingAlgorithms.quick_sort_inplace(data.copy())
        quick_inplace_times.append((time.time() - start) * 1000)

    # Sort nativo
    native_times = []
    for _ in range(n_runs):
        start = time.time()
        sorted(data.copy(), key=lambda x: x[1])
        native_times.append((time.time() - start) * 1000)

    return {
        'merge_sort': {
            'mean': sum(merge_times) / len(merge_times),
            'min': min(merge_times),
            'max': max(merge_times)
        },
        'quick_sort': {
            'mean': sum(quick_times) / len(quick_times),
            'min': min(quick_times),
            'max': max(quick_times)
        },
        'quick_sort_inplace': {
            'mean': sum(quick_inplace_times) / len(quick_inplace_times),
            'min': min(quick_inplace_times),
            'max': max(quick_inplace_times)
        },
        'native_sort': {
            'mean': sum(native_times) / len(native_times),
            'min': min(native_times),
            'max': max(native_times)
        }
    }


def run_challenge4():
    """Executa Desafio 4 completo com melhorias."""
    print_header("4️⃣ DESAFIO 4: TRILHAS PARALELAS (MELHORADO)")

    divider = SprintDivider(SKILLS_DATABASE)

    # Prepara dados
    data = divider.prepare_data()
    print(f"\n📊 Total de habilidades: {len(data)}")

    # Ordena com Merge Sort
    print("\n🔄 Ordenando com Merge Sort...")
    sorted_data = ImprovedSortingAlgorithms.merge_sort(data)

    print("\n✅ Habilidades ordenadas por Complexidade:")
    for i, (skill_id, complexity) in enumerate(sorted_data, 1):
        skill = SKILLS_DATABASE[skill_id]
        print(f"  {i:2d}. {skill_id} ({skill['Nome']:30s}) - C={complexity}")

    # Divide em sprints
    sprints = divider.divide_sprints(sorted_data)

    print("\n📦 DIVISÃO EM SPRINTS:")
    print(f"\n  Sprint A (Skills 1-6):")
    for skill_id in sprints['sprint_a']['skills']:
        print(f"    • {skill_id}: {SKILLS_DATABASE[skill_id]['Nome']}")

    print(f"\n  Sprint B (Skills 7-12):")
    for skill_id in sprints['sprint_b']['skills']:
        print(f"    • {skill_id}: {SKILLS_DATABASE[skill_id]['Nome']}")

    # Análise de balanceamento
    divider.analyze_sprint_balance(sprints)

    # Benchmark
    bench_results = benchmark_sorting(100)
    print("\n📊 BENCHMARK (100 execuções):")
    for algo, metrics in bench_results.items():
        print(f"  {algo:20s}: {metrics['mean']:.4f}ms "
              f"(min={metrics['min']:.4f}, max={metrics['max']:.4f})")

    # Justificativa
    divider.print_algorithm_justification()

    return sprints


if __name__ == "__main__":
    random.seed(GLOBAL_SEED)
    run_challenge4()
