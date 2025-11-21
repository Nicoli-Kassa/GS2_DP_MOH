import sys
import time
import warnings
warnings.filterwarnings('ignore')

from gs_config import print_header, SKILLS_DATABASE

# ============================================================================
#   VALIDAÇÃO INLINE
# ============================================================================
def validate_database_inline():
    """Valida a base de dados inline."""
    all_skills = set(SKILLS_DATABASE.keys())
    print("\n🔍 Validando base de dados...")
    for skill_id, data in SKILLS_DATABASE.items():
        for prereq in data['Pre_Reqs']:
            if prereq not in all_skills:
                raise ValueError(f"Pré-requisito inválido: {skill_id} → {prereq}")
        if data['Valor'] <= 0 or data['Tempo'] <= 0 or data['Complexidade'] <= 0:
            raise ValueError(f"Valores inválidos em {skill_id}")
    print("✅ Base de dados validada com sucesso!")
    return True

# ============================================================================
# IMPORTAÇÕES DOS DESAFIOS
# ============================================================================
try:
    from gs_challenge1 import ImprovedMaxValuePathDP
    from gs_challenge2 import ImprovedCriticalSkillsAnalyzer
    from gs_challenge3 import ImprovedAdaptabilityOptimizer
    from gs_challenge4 import ImprovedSortingAlgorithms, SprintDivider, benchmark_sorting
    from gs_challenge5 import ImprovedSkillRecommender
    from gs_config import (TARGET_SKILL, MAX_TIME, MAX_COMPLEXITY, N_MONTE_CARLO,
                           CRITICAL_SKILLS, BASIC_SKILLS, MIN_ADAPTABILITY,
                           GLOBAL_SEED)
    import random
    import numpy as np
    CHALLENGES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar desafios: {e}")
    CHALLENGES_AVAILABLE = False

# ============================================================================
# IMPORTAÇÃO DE VISUALIZAÇÃO MELHORADA
# ============================================================================
try:
    from gs_visualization import ImprovedVisualization as ProfessionalVisualization
    IMPROVED_PLOTS = True
    print("✅ Módulo de visualização carregado")
except ImportError:
    IMPROVED_PLOTS = False
    print("⚠️ Visualizações desabilitadas")


# ============================================================================
# IMPORTAÇÃO DE TESTES
# ============================================================================
try:
    from gs_tests import run_tests_suite, validate_input_file
    TESTS_AVAILABLE = True
    print("✅ Módulo de testes carregado")
except ImportError:
    TESTS_AVAILABLE = False
    print("⚠️ Testes desabilitados")

# ============================================================================
# EXECUÇÃO DOS DESAFIOS COM VISUALIZAÇÃO
# ============================================================================
def run_challenge1_with_viz():
    """Executa Desafio 1 com visualização completa"""
    print_header("DESAFIO 1: CAMINHO DE VALOR MÁXIMO")
    solver = ImprovedMaxValuePathDP(SKILLS_DATABASE, TARGET_SKILL)
    is_feasible, msg = solver.check_feasibility(MAX_TIME, MAX_COMPLEXITY)
    print(f"\n📊 Viabilidade: {msg}")
    if not is_feasible:
        time_limit = solver.min_feasible_time + 50
        complexity_limit = solver.min_feasible_complexity + 6
        print(f"\n⚙️ Usando limites ajustados: T≤{time_limit}, C≤{complexity_limit}")
    else:
        time_limit = MAX_TIME
        complexity_limit = MAX_COMPLEXITY
    print(f"\n🎲 Executando {N_MONTE_CARLO} simulações Monte Carlo...")
    start = time.time()
    mc_result = solver.solve_with_uncertainty(time_limit, complexity_limit, N_MONTE_CARLO)
    elapsed = time.time() - start
    if mc_result['success']:
        print(f"\n✅ SOLUÇÃO ENCONTRADA (tempo: {elapsed:.2f}s):")
        print(f"  Caminho: {' → '.join(mc_result['path'])}")
        print(f"\n📊 RESULTADOS:")
        print(f"  Valor Determinístico: {mc_result['deterministic_value']}")
        print(f"  E[Valor]: {mc_result['expected_value']:.2f}")
        print(f"  σ(Valor): {mc_result['std_value']:.2f}")
        print(f"  Range: [{mc_result['min_value']:.2f}, {mc_result['max_value']:.2f}]")
        print(f"  CV: {(mc_result['std_value']/mc_result['expected_value'])*100:.2f}%")
        print(f"\n  Tempo Total: {mc_result['total_time']}h")
        print(f"  Complexidade Total: {mc_result['total_complexity']}")
        if IMPROVED_PLOTS:
            print("\n📈 Gerando visualização...")
            ProfessionalVisualization.plot_monte_carlo_enhanced(
                simulations=mc_result['simulations'],
                deterministic_value=mc_result['deterministic_value'],
                filename='desafio1_monte_carlo.png',
                show=True
            )
        return mc_result
    else:
        print(f"\n❌ Solução não encontrada")
        return None

def run_challenge2_with_viz():
    """Executa Desafio 2 com visualização"""
    print_header("DESAFIO 2: VERIFICAÇÃO CRÍTICA")
    analyzer = ImprovedCriticalSkillsAnalyzer(SKILLS_DATABASE, CRITICAL_SKILLS)
    print("\n🔗 Analisando dependências...")
    analyzer.analyze_dependency_impact()
    print(f"\n🔄 Analisando 120 permutações de {CRITICAL_SKILLS}...")
    analysis = analyzer.analyze_all_permutations()
    stats = analysis['statistics']
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  Média: {stats['mean']:.2f}h")
    print(f"  Desvio Padrão: {stats['std']:.2f}h")
    print(f"  Mínimo: {stats['min']:.2f}h")
    print(f"  Máximo: {stats['max']:.2f}h")
    print(f"  Range: {stats['range']:.2f}h")
    print(f"\n🏆 TOP 3 ORDENS:")
    for i, result in enumerate(analysis['top3'], 1):
        print(f"\n  #{i}: {' → '.join(result['order'])}")
        print(f"      Tempo Total: {result['total_time']}h")
        waiting = sum(e['time'] for e in result['timeline'] if e['action'] == 'waiting')
        acquire = sum(e['time'] for e in result['timeline'] if e['action'] == 'acquire')
        print(f"      Breakdown: {waiting}h (espera) + {acquire}h (críticas)")
    heuristics = analyzer.identify_heuristics(analysis['top3'])
    if heuristics:
        print(f"\n💡 HEURÍSTICAS IDENTIFICADAS:")
        for h in heuristics:
            print(f"  • {h}")
    if IMPROVED_PLOTS:
        print("\n📈 Gerando visualização...")
        ProfessionalVisualization.plot_top3_timeline_enhanced(
            top3=analysis['top3'],
            filename='desafio2_top3.png',
            show=True
        )
    return analysis

def run_challenge3_with_viz():
    """Executa Desafio 3 com visualização"""
    print_header("DESAFIO 3: PIVÔ MAIS RÁPIDO")
    optimizer = ImprovedAdaptabilityOptimizer(SKILLS_DATABASE, BASIC_SKILLS, MIN_ADAPTABILITY)
    print("\n🔬 COMPARAÇÃO DE SOLUÇÕES:")
    start = time.time()
    greedy = optimizer.greedy_solution(verbose=False)
    greedy_time = time.time() - start
    start = time.time()
    dp = optimizer.optimal_solution_dp(verbose=False)
    dp_time = time.time() - start
    print(f"\n  GULOSO (V/T):")
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
        if greedy['total_time'] == dp['total_time']:
            print(f"\n  ✅ Guloso encontrou solução ÓTIMA!")
        else:
            diff = greedy['total_time'] - dp['total_time']
            pct = (diff / dp['total_time']) * 100
            print(f"\n  ⚠️ Guloso subótimo: +{diff}h (+{pct:.1f}%)")
    print("\n" + "="*80)
    print("CONTRAEXEMPLO: GULOSO NEM SEMPRE É ÓTIMO")
    print("="*80)
    counter = optimizer.demonstrate_counterexample()
    print(f"\n{counter['explanation']}")
    print(f"\n  Guloso escolhe: {counter['greedy_solution']['choice']} → {counter['greedy_solution']['time']}h")
    print(f"  Ótimo é: {counter['optimal_solution']['choice']} → {counter['optimal_solution']['time']}h")
    print("\n📊 Análise empírica de complexidade...")
    empirical = optimizer.empirical_complexity_analysis(max_size=12)
    if IMPROVED_PLOTS:
        print("\n📈 Gerando visualização...")
        ProfessionalVisualization.plot_complexity_enhanced(
            empirical_data=empirical,
            filename='desafio3_complexity.png',
            show=True
        )
    return {'greedy': greedy, 'dp': dp, 'empirical': empirical}

def run_challenge4_with_viz():
    """Executa Desafio 4 com visualização"""
    print_header("DESAFIO 4: TRILHAS PARALELAS")
    divider = SprintDivider(SKILLS_DATABASE)
    data = divider.prepare_data()
    print(f"\n📊 Total de habilidades: {len(data)}")
    print("\n🔄 Ordenando com Merge Sort...")
    sorted_data = ImprovedSortingAlgorithms.merge_sort(data)
    print("\n✅ Habilidades ordenadas por Complexidade:")
    for i, (skill_id, complexity) in enumerate(sorted_data, 1):
        skill = SKILLS_DATABASE[skill_id]
        print(f"  {i:2d}. {skill_id} ({skill['Nome']:30s}) - C={complexity}")
    sprints = divider.divide_sprints(sorted_data)
    print("\n📦 DIVISÃO EM SPRINTS:")
    print(f"\n  Sprint A (Skills 1-6):")
    for skill_id in sprints['sprint_a']['skills']:
        print(f"    • {skill_id}: {SKILLS_DATABASE[skill_id]['Nome']}")
    print(f"\n  Sprint B (Skills 7-12):")
    for skill_id in sprints['sprint_b']['skills']:
        print(f"    • {skill_id}: {SKILLS_DATABASE[skill_id]['Nome']}")
    divider.analyze_sprint_balance(sprints)
    print("\n⏱️ Executando benchmark (100 rodadas)...")
    bench_results = benchmark_sorting(100)
    print("\n📊 RESULTADOS DO BENCHMARK:")
    for algo, metrics in bench_results.items():
        print(f"  {algo:20s}: {metrics['mean']:.4f}ms "
              f"(min={metrics['min']:.4f}, max={metrics['max']:.4f})")
    divider.print_algorithm_justification()
    if IMPROVED_PLOTS:
        print("\n📈 Gerando visualização...")
        try:
            ProfessionalVisualization.plot_sorting_comparison(
                benchmark_results=bench_results,
                filename='desafio4_sorting.png',
                show=True
            )
        except AttributeError:
            print("⚠️ Método plot_sorting_comparison não disponível na classe de visualização")
    return {'sprints': sprints, 'benchmark': bench_results}

def run_challenge5_with_viz():
    """Executa Desafio 5 com visualização"""
    print_header("DESAFIO 5: RECOMENDAÇÃO DE HABILIDADES")
    recommender = ImprovedSkillRecommender(SKILLS_DATABASE)
    recommender.print_market_scenarios()
    current_profile = {'H1', 'H2', 'H3'}
    print(f"\n👤 PERFIL ATUAL: {sorted(current_profile)}")
    print("\n🔬 Comparando abordagens: Guloso vs DP Verdadeiro...")
    greedy_result = recommender.recommend_greedy(current_profile, 3)
    dp_result = recommender.recommend_with_dp(current_profile, max_time=5000)
    print("\n📊 RESULTADOS:")
    print("\n  GULOSO (E[V]/T):")
    for i, rec in enumerate(greedy_result['recommendations'], 1):
        print(f"    {i}. {rec['skill_id']} ({rec['skill_name']})")
        print(f"       E[V]={rec['expected_value']:.2f}, T={rec['time']}h, Score={rec['score']:.4f}")
    print("\n  DP VERDADEIRO:")
    if dp_result.get('recommendations'):
        for i, rec in enumerate(dp_result['recommendations'], 1):
            print(f"    {i}. {rec['skill_id']} ({rec['skill_name']})")
            print(f"       E[V]={rec['expected_value']:.2f}, T={rec['time']}h")
        if 'optimal_path' in dp_result:
            print(f"\n  Path Ótimo: {' → '.join(dp_result['optimal_path'][:5])}...")
            print(f"  Valor Total: {dp_result.get('optimal_value', 0):.2f}")
            print(f"  Tempo Total: {dp_result.get('optimal_time', 0)}h")
    else:
        print("    Nenhuma recomendação")
    greedy_ids = set(r['skill_id'] for r in greedy_result['recommendations'])
    dp_ids = set(r['skill_id'] for r in dp_result.get('recommendations', []))
    print("\n💡 ANÁLISE:")
    if greedy_ids == dp_ids:
        print("  ✅ Guloso coincide com DP (neste caso)")
    else:
        overlap = greedy_ids & dp_ids
        print(f"  ⚠️ Abordagens diferem")
        print(f"    Sobreposição: {overlap}")
        print(f"    Apenas Guloso: {greedy_ids - dp_ids}")
        print(f"    Apenas DP: {dp_ids - greedy_ids}")
    if IMPROVED_PLOTS:
        print("\n📈 Gerando visualização...")
        try:
            ProfessionalVisualization.plot_recommendation_analysis(
                greedy_result=greedy_result,
                dp_result=dp_result,
                filename='desafio5_recommendation.png',
                show=True
            )
        except AttributeError:
            print("⚠️ Método plot_recommendation_analysis não disponível na classe de visualização")
    return {'greedy': greedy_result, 'dp': dp_result}

# ============================================================================
# FUNÇÃO PARA EXECUTAR TESTES
# ============================================================================
def run_tests():
    """Executa a suite de testes"""
    if not TESTS_AVAILABLE:
        print("\n⚠️ Módulo de testes não disponível")
        return None
    print("\n📋 Validando gs_input_file...")
    if hasattr(validate_input_file, '__call__'):
        try:
            if not validate_input_file():
                print("❌ Validação falhou")
                return None
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return None
    print("\n🧪 Executando suite de testes...")
    try:
        result = run_tests_suite(verbosity=2)
    except Exception as e:
        print(f"❌ Erro na suíte de testes: {e}")
        return None
    print("\n📊 RESUMO DOS TESTES:")
    try:
        print(f"  Total: {result.testsRun}")
        print(f"  ✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"  ❌ Falhas: {len(result.failures)}")
        print(f"  ⚠️ Erros: {len(result.errors)}")
        if result.wasSuccessful():
            print("\n🎉 TODOS OS TESTES PASSARAM!")
        else:
            print("\n⚠️ ALGUNS TESTES FALHARAM")
    except Exception:
        print("⚠️ Resumo dos testes indisponível")
    return result

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================
def print_intro():
    """Imprime introdução"""
    print("\n" + "="*80+ "\n")
    print(" "*15 + "GLOBAL SOLUTION - MOTOR DE ORIENTAÇÃO DE HABILIDADES")
    print(" "*25 + "Engenharia de Software")
    print(" "*20 + "Programação Dinâmica - Novembro 2025\n")
    print("="*80)
    print("\n⏱️ Tempo estimado: 30-90 segundos")
    print("-"*80)

def run_all_with_visualizations():
    """Executa todos os desafios COM visualizações e TESTES"""
    start_time = time.time()
    results = {}
    try:
        random.seed(GLOBAL_SEED)
        np.random.seed(GLOBAL_SEED)
        # DESAFIO 1
        results['challenge1'] = run_challenge1_with_viz()
        # DESAFIO 2
        results['challenge2'] = run_challenge2_with_viz()
        # DESAFIO 3
        results['challenge3'] = run_challenge3_with_viz()
        # DESAFIO 4
        results['challenge4'] = run_challenge4_with_viz()
        # DESAFIO 5
        results['challenge5'] = run_challenge5_with_viz()
        # TESTES
        print("\n" + "="*80)
        print_header("EXECUTANDO TESTES")
        results['tests'] = run_tests()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    total_time = time.time() - start_time
    # SUMÁRIO FINAL
    print("\n" + "="*80)
    print_header("SUMÁRIO DE EXECUÇÃO")
    print(f"\n✅ {len(results)-1} desafio(s) executado(s) com sucesso!")  # -1 para não contar os testes
    print(f"⏱️ Tempo total: {total_time:.2f}s")
    print("\n📊 GRÁFICOS GERADOS:")
    if IMPROVED_PLOTS:
        print("  - desafio1_monte_carlo.png - Análise Monte Carlo completa")
        print("  - desafio2_top3.png - Timeline detalhada (120 permutações)")
        print("  - desafio3_complexity.png - Análise empírica de complexidade")
        print("  - desafio4_sorting.png - Comparação de algoritmos de ordenação")
        print("  - desafio5_recommendation.png - Análise de recomendações")
    else:
        print("  ⚠️ Visualizações desabilitadas") 
    return results

def main():
    """Função principal"""
    # Validação
    try:
        validate_database_inline()
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        sys.exit(1)
    if not CHALLENGES_AVAILABLE:
        print("❌ Desafios não disponíveis!")
        sys.exit(1)
    print_intro()
    print("\n🚀 Iniciando execução automática...")
    print("   (Os gráficos serão exibidos E salvos automaticamente)")
    print("\n" + "⏳"*40 + "\n")
    results = run_all_with_visualizations()
    return results

if __name__ == "__main__":
    main()
