"""
Desafio 5 — Recomendar Próximas Habilidades

Objetivo: dado um perfil atual e um horizonte de 5 anos, sugerir as próximas 2–3 habilidades
maximizando o valor esperado, considerando transições de mercado (probabilidades
fornecidas por você ou simuladas).

Sugestão técnica: usar DP em horizonte finito ou busca com “look ahead”, ponderando
probabilidades de cenário.
"""

import numpy as np
from typing import Dict, List, Set, Tuple
from collections import defaultdict

from gs_config import SKILLS_DATABASE, print_header, GLOBAL_SEED


class ImprovedSkillRecommender:
    """
    ALGORITMO DP:

    Estado: dp[t][frozenset(skills)] = (valor_esperado_máximo, path)

    Transição:
    Para cada tempo t:
        Para cada conjunto de skills:
            Para cada skill disponível h:
                novo_tempo = t + tempo[h]
                novo_skills = skills ∪ {h}
                novo_valor = valor_atual + E[V(h, cenário)] × desconto^(t/2000)

                Se melhor: dp[novo_tempo][novo_skills] = (novo_valor, path + [h])

    Complexidade: O(T × 2^n × n) onde T = horizonte em horas, n = número de skills
    """

    def __init__(self, skills_db: Dict):
        self.skills_db = skills_db
        self.market_scenarios = self._define_market_scenarios()

    def _define_market_scenarios(self) -> Dict:
        """Define cenários de mercado."""
        return {
            'scenarios': {
                'AI_Boom': {
                    'prob': 0.4,
                    'value_multiplier': {
                        'S6': 1.5,  # IA Generativa
                        'S4': 1.3,  # ML
                        'H11': 1.2  # Big Data
                    },
                    'description': 'Explosão de IA e ML'
                },
                'Cloud_Native': {
                    'prob': 0.35,
                    'value_multiplier': {
                        'S7': 1.4,  # Cloud
                        'S9': 1.3,  # DevOps
                        'S8': 1.2   # APIs
                    },
                    'description': 'Cloud-native dominante'
                },
                'Security_First': {
                    'prob': 0.25,
                    'value_multiplier': {
                        'S5': 1.6,  # Cybersecurity
                        'H12': 1.3  # Blockchain
                    },
                    'description': 'Foco em segurança'
                }
            },
            'horizon_years': 5,
            'discount_factor': 0.95  # Desconto anual
        }

    def _calculate_expected_value(self, skill_id: str, 
                                  current_skills: Set[str],
                                  years_ahead: int) -> float:
        """
        Calcula valor esperado de uma skill considerando cenários.

        E[V] = Σ P(cenário) × V × multiplicador[cenário]
        """
        base_value = self.skills_db[skill_id]['Valor']
        expected_value = 0

        for scenario_name, scenario_data in self.market_scenarios['scenarios'].items():
            prob = scenario_data['prob']
            multiplier = scenario_data['value_multiplier'].get(skill_id, 1.0)

            # Bônus por sinergia (skills relacionadas já adquiridas)
            synergy_bonus = 1.0
            for prereq in self.skills_db[skill_id]['Pre_Reqs']:
                if prereq in current_skills:
                    synergy_bonus += 0.05

            scenario_value = base_value * multiplier * synergy_bonus
            expected_value += prob * scenario_value

        # Desconto temporal
        discount = self.market_scenarios['discount_factor'] ** years_ahead

        return expected_value * discount

    def _get_available_skills(self, acquired: Set[str]) -> List[str]:
        """Retorna skills cujos pré-requisitos estão satisfeitos."""
        available = []

        for skill_id in self.skills_db.keys():
            if skill_id in acquired:
                continue

            prereqs = set(self.skills_db[skill_id]['Pre_Reqs'])
            if prereqs.issubset(acquired):
                available.append(skill_id)

        return available

    def recommend_greedy(self, current_profile: Set[str],
                        num_recommendations: int = 3) -> Dict:
        """
        Abordagem GULOSA (baseline para comparação).

        Seleciona skills com melhor score: E[V] / Tempo
        """
        available = self._get_available_skills(current_profile)

        # Calcula scores
        scores = []
        for skill_id in available:
            expected_val = self._calculate_expected_value(skill_id, current_profile, 1)
            time = self.skills_db[skill_id]['Tempo']
            score = expected_val / time

            scores.append({
                'skill_id': skill_id,
                'skill_name': self.skills_db[skill_id]['Nome'],
                'expected_value': expected_val,
                'time': time,
                'score': score
            })

        # Ordena por score
        scores.sort(key=lambda x: x['score'], reverse=True)

        return {
            'algorithm': 'Guloso (E[V]/T)',
            'recommendations': scores[:num_recommendations],
            'all_scores': scores
        }

    def recommend_with_dp(self, current_profile: Set[str],
                         max_time: int = 10000,
                         discretization: int = 10) -> Dict:
        """
        Args:
            current_profile: Skills já adquiridas
            max_time: Horizonte de tempo (horas)
            discretization: Passo de discretização (horas)

        Returns:
            Dict com path ótimo e recomendações
        """
        print(f"\n🧠 Executando DP verdadeiro (horizonte={max_time}h)...")

        horizon_hours = min(max_time, self.market_scenarios['horizon_years'] * 2000)

        # dp[tempo][frozenset(skills)] = (valor_esperado, path)
        dp = defaultdict(lambda: {})
        dp[0][frozenset(current_profile)] = (0, [])

        # DP forward
        processed_states = 0
        for t in range(0, horizon_hours + 1, discretization):
            if t not in dp:
                continue

            for skills_set, (current_value, path) in list(dp[t].items()):
                available = self._get_available_skills(skills_set)

                for skill_id in available:
                    skill = self.skills_db[skill_id]
                    new_t = t + skill['Tempo']

                    if new_t > horizon_hours:
                        continue

                    # Calcula valor esperado com desconto temporal
                    years_ahead = new_t / 2000
                    expected_value = self._calculate_expected_value(
                        skill_id, skills_set, int(years_ahead)
                    )

                    new_value = current_value + expected_value
                    new_skills = skills_set | {skill_id}
                    new_path = path + [skill_id]

                    # Atualiza se melhor
                    if (new_skills not in dp[new_t] or 
                        new_value > dp[new_t][new_skills][0]):
                        dp[new_t][new_skills] = (new_value, new_path)
                        processed_states += 1

        print(f"  Estados processados: {processed_states}")

        # Encontra melhor solução
        best_value = -1
        best_solution = None
        best_time = 0

        for t in dp:
            for skills_set, (value, path) in dp[t].items():
                if value > best_value:
                    best_value = value
                    best_solution = (skills_set, path)
                    best_time = t

        if best_solution:
            skills_set, path = best_solution
            # Recomenda apenas os próximos 2-3
            next_skills = [s for s in path if s not in current_profile][:3]

            recommendations = []
            for skill_id in next_skills:
                recommendations.append({
                    'skill_id': skill_id,
                    'skill_name': self.skills_db[skill_id]['Nome'],
                    'expected_value': self._calculate_expected_value(
                        skill_id, current_profile, 1
                    ),
                    'time': self.skills_db[skill_id]['Tempo']
                })

            return {
                'algorithm': 'DP Verdadeiro',
                'recommendations': recommendations,
                'optimal_path': path,
                'optimal_value': best_value,
                'optimal_time': best_time,
                'num_new_skills': len([s for s in path if s not in current_profile])
            }

        return {
            'algorithm': 'DP Verdadeiro',
            'recommendations': [],
            'message': 'Nenhuma solução encontrada'
        }

    def compare_approaches(self, current_profile: Set[str]):
        """
        Comparação entre Guloso e DP.
        """
        print("\n" + "="*80)
        print("COMPARAÇÃO: GULOSO vs DP VERDADEIRO")
        print("="*80)

        # Guloso
        print("\n🏃 Executando abordagem GULOSA...")
        greedy_result = self.recommend_greedy(current_profile, 3)

        # DP
        dp_result = self.recommend_with_dp(current_profile, max_time=5000)

        # Resultados
        print("\n📊 RESULTADOS:")

        print("\n  GULOSO (Score E[V]/T):")
        for i, rec in enumerate(greedy_result['recommendations'], 1):
            print(f"    {i}. {rec['skill_id']} ({rec['skill_name']})")
            print(f"       E[V]={rec['expected_value']:.2f}, "
                  f"T={rec['time']}h, Score={rec['score']:.4f}")

        print("\n  DP VERDADEIRO (Valor Esperado Ótimo):")
        if dp_result['recommendations']:
            for i, rec in enumerate(dp_result['recommendations'], 1):
                print(f"    {i}. {rec['skill_id']} ({rec['skill_name']})")
                print(f"       E[V]={rec['expected_value']:.2f}, T={rec['time']}h")

            print(f"\n  Path Ótimo Completo: {' → '.join(dp_result['optimal_path'])}")
            print(f"  Valor Total Ótimo: {dp_result['optimal_value']:.2f}")
            print(f"  Tempo Total: {dp_result['optimal_time']}h")
        else:
            print("    Nenhuma recomendação")

        # Análise
        print("\n💡 ANÁLISE:")

        greedy_ids = set(r['skill_id'] for r in greedy_result['recommendations'])
        dp_ids = set(r['skill_id'] for r in dp_result['recommendations'])

        if greedy_ids == dp_ids:
            print("  ✅ Guloso coincide com DP (neste caso)")
        else:
            overlap = greedy_ids & dp_ids
            print(f"  ⚠️ Abordagens diferem!")
            print(f"    Sobreposição: {overlap}")
            print(f"    Apenas Guloso: {greedy_ids - dp_ids}")
            print(f"    Apenas DP: {dp_ids - greedy_ids}")

        print("\n  📈 VANTAGENS DO DP:")
        print("    • Considera trajetórias completas (look-ahead)")
        print("    • Otimiza valor esperado TOTAL")
        print("    • Captura sinergias entre skills")

        print("\n  ⚡ VANTAGENS DO GULOSO:")
        print("    • Muito mais rápido")
        print("    • Simples de implementar")
        print("    • Bom para decisões imediatas")

        return {'greedy': greedy_result, 'dp': dp_result}

    def print_market_scenarios(self):
        """Imprime cenários de mercado."""
        print("\n🌐 CENÁRIOS DE MERCADO:")

        for name, data in self.market_scenarios['scenarios'].items():
            print(f"\n  {name} (P={data['prob']}):")
            print(f"    {data['description']}")
            print(f"    Multiplicadores:")
            for skill_id, mult in data['value_multiplier'].items():
                skill_name = self.skills_db[skill_id]['Nome']
                print(f"      • {skill_id} ({skill_name}): ×{mult}")

        print(f"\n  Horizonte: {self.market_scenarios['horizon_years']} anos")
        print(f"  Desconto anual: {self.market_scenarios['discount_factor']}")


def run_challenge5():
    """Executa Desafio 5 completo com DP verdadeiro."""
    print_header("5️⃣ DESAFIO 5: RECOMENDAÇÃO DE HABILIDADES (MELHORADO)")

    recommender = ImprovedSkillRecommender(SKILLS_DATABASE)

    # Cenários de mercado
    recommender.print_market_scenarios()

    # Perfil inicial (exemplo: habilidades básicas)
    current_profile = {'H1', 'H2', 'H3'}

    print(f"\n👤 PERFIL ATUAL: {sorted(current_profile)}")

    # Comparação de abordagens
    results = recommender.compare_approaches(current_profile)

    # Teste com perfil avançado
    print("\n" + "="*80)
    print("TESTE COM PERFIL AVANÇADO")
    print("="*80)

    advanced_profile = {'H1', 'H2', 'H3', 'H4', 'S1'}
    print(f"\n👤 PERFIL AVANÇADO: {sorted(advanced_profile)}")

    results_adv = recommender.compare_approaches(advanced_profile)

    return results


if __name__ == "__main__":
    np.random.seed(GLOBAL_SEED)
    run_challenge5()
