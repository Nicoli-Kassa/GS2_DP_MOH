"""
Configuração Global e Base de Dados de Habilidades

Este módulo contém:
- Base de dados de habilidades com grafo de dependências
- Parâmetros de configuração para cada desafio
- Funções utilitárias de formatação
- Constantes para visualização
- Validação de integridade dos dados
"""

import numpy as np
import random
from typing import Dict, List, Set, Any, Tuple

# ============================================================================
# SEED GLOBAL PARA REPRODUTIBILIDADE
# ============================================================================
GLOBAL_SEED = 42
np.random.seed(GLOBAL_SEED)
random.seed(GLOBAL_SEED)

# ============================================================================
# BASE DE DADOS DE HABILIDADES
# ============================================================================
# Estrutura: {ID: {'Nome': str, 'Valor': int, 'Tempo': int, 
#                  'Complexidade': int, 'Pre_Reqs': List[str], 'Categoria': str}}
# 
# Valor: Importância no mercado (1-40)
# Tempo: Horas necessárias para aquisição (35-120)
# Complexidade: Dificuldade de aprendizado (2-9)
# Pre_Reqs: IDs de habilidades pré-requisito
# Categoria: Classificação da habilidade

SKILLS_DATABASE = {
    # ========================================================================
    # HABILIDADES BÁSICAS (sem pré-requisitos)
    # ========================================================================
    'H1': {
        'Nome': 'Lógica de Programação',
        'Valor': 10,
        'Tempo': 40,
        'Complexidade': 2,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H2': {
        'Nome': 'Estruturas de Dados',
        'Valor': 12,
        'Tempo': 50,
        'Complexidade': 3,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H3': {
        'Nome': 'Algoritmos',
        'Valor': 15,
        'Tempo': 60,
        'Complexidade': 4,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H4': {
        'Nome': 'Banco de Dados',
        'Valor': 11,
        'Tempo': 45,
        'Complexidade': 3,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H5': {
        'Nome': 'Redes',
        'Valor': 9,
        'Tempo': 35,
        'Complexidade': 2,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H6': {
        'Nome': 'Sistemas Operacionais',
        'Valor': 10,
        'Tempo': 40,
        'Complexidade': 3,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H7': {
        'Nome': 'Engenharia de Software',
        'Valor': 13,
        'Tempo': 55,
        'Complexidade': 4,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },

    # ========================================================================
    # HABILIDADES INTERMEDIÁRIAS
    # ========================================================================
    'S1': {
        'Nome': 'Python Avançado',
        'Valor': 18,
        'Tempo': 70,
        'Complexidade': 5,
        'Pre_Reqs': ['H1', 'H2'],
        'Categoria': 'Soft_Intermediaria'
    },
    'S2': {
        'Nome': 'Java Enterprise',
        'Valor': 20,
        'Tempo': 80,
        'Complexidade': 6,
        'Pre_Reqs': ['H1', 'H2', 'H7'],
        'Categoria': 'Soft_Intermediaria'
    },
    'S3': {
        'Nome': 'React',
        'Valor': 22,
        'Tempo': 65,
        'Complexidade': 5,
        'Pre_Reqs': ['H1'],
        'Categoria': 'Soft_Intermediaria'
    },
    'S4': {
        'Nome': 'Machine Learning',
        'Valor': 30,
        'Tempo': 100,
        'Complexidade': 8,
        'Pre_Reqs': ['H2', 'H3', 'S1'],
        'Categoria': 'Soft_Avancada'
    },
    'S5': {
        'Nome': 'Cybersecurity',
        'Valor': 25,
        'Tempo': 90,
        'Complexidade': 7,
        'Pre_Reqs': ['H5', 'H6'],
        'Categoria': 'Soft_Avancada'
    },

    # ========================================================================
    # HABILIDADES AVANÇADAS
    # ========================================================================
    'S6': {
        'Nome': 'IA Generativa',
        'Valor': 40,
        'Tempo': 120,
        'Complexidade': 9,
        'Pre_Reqs': ['S4'],
        'Categoria': 'Soft_Avancada'
    },
    'S7': {
        'Nome': 'Cloud Architecture',
        'Valor': 35,
        'Tempo': 110,
        'Complexidade': 8,
        'Pre_Reqs': ['H4', 'H5', 'H6'],
        'Categoria': 'Soft_Avancada'
    },
    'S8': {
        'Nome': 'Microservices',
        'Valor': 28,
        'Tempo': 85,
        'Complexidade': 7,
        'Pre_Reqs': ['S2', 'H4'],
        'Categoria': 'Soft_Avancada'
    },
    'S9': {
        'Nome': 'DevOps',
        'Valor': 26,
        'Tempo': 75,
        'Complexidade': 6,
        'Pre_Reqs': ['H6', 'H7'],
        'Categoria': 'Soft_Avancada'
    },

    # ========================================================================
    # HABILIDADES ESPECIALIZADAS
    # ========================================================================
    'H11': {
        'Nome': 'Big Data',
        'Valor': 32,
        'Tempo': 95,
        'Complexidade': 8,
        'Pre_Reqs': ['H4', 'S1'],
        'Categoria': 'Hard_Especializada'
    },
    'H12': {
        'Nome': 'Blockchain',
        'Valor': 29,
        'Tempo': 88,
        'Complexidade': 7,
        'Pre_Reqs': ['H4', 'S5'],
        'Categoria': 'Hard_Especializada'
    },
}

# ============================================================================
# CONJUNTOS DE HABILIDADES
# ============================================================================
BASIC_SKILLS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7']
CRITICAL_SKILLS = ['S3', 'S5', 'S7', 'S8', 'S9']
ADVANCED_SKILLS = ['S4', 'S6', 'H11', 'H12']
ALL_SOFT_SKILLS = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
ALL_HARD_SKILLS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H11', 'H12']

# ============================================================================
# PARÂMETROS DOS DESAFIOS
# ============================================================================

# ---------------------------------------------------------------------------
# DESAFIO 1: Caminho de Valor Máximo
# ---------------------------------------------------------------------------
TARGET_SKILL = 'S6'                    # Habilidade alvo (IA Generativa)
MAX_TIME = 350                         # Tempo máximo permitido (horas)
MAX_COMPLEXITY = 30                    # Complexidade máxima permitida
N_MONTE_CARLO = 1000                   # Número de simulações Monte Carlo

# Limites mínimos viáveis (calculados automaticamente)
TEMPO_MIN = 300                        # Tempo mínimo para atingir S6
COMPLEXIDADE_MIN = 24                  # Complexidade mínima para S6
USE_RELAXED_CONSTRAINTS = True         # Ajustar limites automaticamente se inviável

# ---------------------------------------------------------------------------
# DESAFIO 2: Verificação Crítica
# ---------------------------------------------------------------------------
# CRITICAL_SKILLS já definido acima: ['S3', 'S5', 'S7', 'S8', 'S9']
# Total de permutações: 5! = 120

# ---------------------------------------------------------------------------
# DESAFIO 3: Pivô Mais Rápido
# ---------------------------------------------------------------------------
# BASIC_SKILLS já definido acima: ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7']
MIN_ADAPTABILITY = 15                  # Valor mínimo de adaptabilidade

# ---------------------------------------------------------------------------
# DESAFIO 4: Trilhas Paralelas
# ---------------------------------------------------------------------------
# Usa todas as skills da base de dados (18 skills)
# Divide em Sprint A (1-9) e Sprint B (10-18)

# ---------------------------------------------------------------------------
# DESAFIO 5: Recomendação de Habilidades
# ---------------------------------------------------------------------------
HORIZON_YEARS = 5                      # Horizonte de planejamento (anos)
DISCOUNT_FACTOR = 0.95                 # Fator de desconto temporal anual

# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def print_header(title: str, width: int = 80) -> None:
    """
    Imprime cabeçalho formatado.

    Args:
        title: Título do cabeçalho
        width: Largura total em caracteres
    """
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_section(title: str, width: int = 80) -> None:
    """
    Imprime seção formatada.

    Args:
        title: Título da seção
        width: Largura total em caracteres
    """
    print("\n" + "-" * width)
    print(f"  {title}")
    print("-" * width)


def print_skill_info(skill_id: str, indent: int = 2) -> None:
    """
    Imprime informações de uma habilidade.

    Args:
        skill_id: ID da habilidade
        indent: Número de espaços para indentação
    """
    if skill_id not in SKILLS_DATABASE:
        print(f"{' ' * indent}❌ Habilidade {skill_id} não encontrada!")
        return

    skill = SKILLS_DATABASE[skill_id]
    spaces = ' ' * indent

    print(f"{spaces}🎯 {skill_id}: {skill['Nome']}")
    print(f"{spaces}   Valor: {skill['Valor']} | "
          f"Tempo: {skill['Tempo']}h | "
          f"Complexidade: {skill['Complexidade']}")

    if skill['Pre_Reqs']:
        prereqs_str = ', '.join(skill['Pre_Reqs'])
        print(f"{spaces}   Pré-requisitos: {prereqs_str}")
    else:
        print(f"{spaces}   Pré-requisitos: Nenhum (skill básica)")


# ============================================================================
# CONFIGURAÇÕES DE VISUALIZAÇÃO
# ============================================================================

# Estilo para gráficos matplotlib
PLOT_STYLE = {
    'figure.figsize': (12, 6),
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'font.family': 'sans-serif'
}

# Paleta de cores para gráficos
COLORS = {
    'primary': '#2E86AB',      # Azul
    'secondary': '#A23B72',    # Rosa
    'success': '#06A77D',      # Verde
    'warning': '#F18F01',      # Laranja
    'danger': '#C73E1D',       # Vermelho
    'info': '#6A4C93',         # Roxo
    'neutral': '#6C757D'       # Cinza
}

# Símbolos para output
SYMBOLS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'target': '🎯',
    'time': '⏱️',
    'value': '💎',
    'complexity': '🧩',
    'path': '🛤️',
    'chart': '📊',
    'search': '🔍',
    'fire': '🔥',
    'star': '⭐',
    'rocket': '🚀'
}

# ============================================================================
# VALIDAÇÃO DE INTEGRIDADE
# ============================================================================

def validate_database() -> Tuple[bool, List[str]]:
    """
    Valida a integridade da base de dados de habilidades.

    Verificações:
    - Todos os pré-requisitos existem
    - Valores são positivos
    - Não há ciclos nas dependências
    - Campos obrigatórios estão presentes

    Returns:
        Tuple[bool, List[str]]: (is_valid, lista_de_erros)
    """
    all_skills = set(SKILLS_DATABASE.keys())
    errors = []

    # 1. Valida existência de pré-requisitos
    for skill_id, data in SKILLS_DATABASE.items():
        for prereq in data['Pre_Reqs']:
            if prereq not in all_skills:
                errors.append(
                    f"Pré-requisito inválido: {skill_id} → {prereq} (não existe)"
                )

    # 2. Valida valores positivos
    for skill_id, data in SKILLS_DATABASE.items():
        if data['Valor'] <= 0:
            errors.append(f"Valor inválido em {skill_id}: {data['Valor']}")
        if data['Tempo'] <= 0:
            errors.append(f"Tempo inválido em {skill_id}: {data['Tempo']}")
        if data['Complexidade'] <= 0:
            errors.append(f"Complexidade inválida em {skill_id}: {data['Complexidade']}")

    # 3. Valida campos obrigatórios
    required_fields = ['Nome', 'Valor', 'Tempo', 'Complexidade', 'Pre_Reqs']
    for skill_id, data in SKILLS_DATABASE.items():
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo obrigatório '{field}' faltando em {skill_id}")

    # 4. Detecta ciclos (DFS)
    def has_cycle(skill_id: str, visited: Set[str], rec_stack: Set[str]) -> bool:
        visited.add(skill_id)
        rec_stack.add(skill_id)

        for prereq in SKILLS_DATABASE[skill_id]['Pre_Reqs']:
            if prereq not in visited:
                if has_cycle(prereq, visited, rec_stack):
                    return True
            elif prereq in rec_stack:
                return True

        rec_stack.remove(skill_id)
        return False

    visited = set()
    for skill_id in SKILLS_DATABASE.keys():
        if skill_id not in visited:
            if has_cycle(skill_id, visited, set()):
                errors.append(f"Ciclo detectado envolvendo {skill_id}")

    return len(errors) == 0, errors


def get_statistics() -> Dict[str, Any]:
    """
    Retorna estatísticas da base de dados.

    Returns:
        Dict com estatísticas agregadas (total, min, max, mean)
    """
    values = [s['Valor'] for s in SKILLS_DATABASE.values()]
    times = [s['Tempo'] for s in SKILLS_DATABASE.values()]
    complexities = [s['Complexidade'] for s in SKILLS_DATABASE.values()]

    return {
        'total_skills': len(SKILLS_DATABASE),
        'valor': {
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / len(values),
            'total': sum(values)
        },
        'tempo': {
            'min': min(times),
            'max': max(times),
            'mean': sum(times) / len(times),
            'total': sum(times)
        },
        'complexidade': {
            'min': min(complexities),
            'max': max(complexities),
            'mean': sum(complexities) / len(complexities),
            'total': sum(complexities)
        }
    }


def print_statistics() -> None:
    """Imprime estatísticas da base de dados de forma formatada."""
    stats = get_statistics()

    print_header("ESTATÍSTICAS DA BASE DE DADOS")

    print(f"\n📊 Total de habilidades: {stats['total_skills']}")

    print(f"\n💎 Valor:")
    print(f"   Range: [{stats['valor']['min']}, {stats['valor']['max']}]")
    print(f"   Média: {stats['valor']['mean']:.2f}")
    print(f"   Total: {stats['valor']['total']}")

    print(f"\n⏱️ Tempo (horas):")
    print(f"   Range: [{stats['tempo']['min']}, {stats['tempo']['max']}]")
    print(f"   Média: {stats['tempo']['mean']:.2f}")
    print(f"   Total: {stats['tempo']['total']}")

    print(f"\n🧩 Complexidade:")
    print(f"   Range: [{stats['complexidade']['min']}, {stats['complexidade']['max']}]")
    print(f"   Média: {stats['complexidade']['mean']:.2f}")


# ============================================================================
# EXPORTAÇÕES
# ============================================================================
__all__ = [
    # Database
    'SKILLS_DATABASE',
    'BASIC_SKILLS',
    'CRITICAL_SKILLS',
    'ADVANCED_SKILLS',
    'ALL_SOFT_SKILLS',
    'ALL_HARD_SKILLS',

    # Parâmetros dos desafios
    'TARGET_SKILL',
    'MAX_TIME',
    'MAX_COMPLEXITY',
    'N_MONTE_CARLO',
    'MIN_ADAPTABILITY',
    'HORIZON_YEARS',
    'DISCOUNT_FACTOR',

    # Configurações
    'GLOBAL_SEED',
    'PLOT_STYLE',
    'COLORS',
    'SYMBOLS',

    # Funções
    'print_header',
    'print_section',
    'print_skill_info',
    'validate_database',
    'get_statistics',
    'print_statistics'
]

# ============================================================================
# EXECUÇÃO COMO SCRIPT
# ============================================================================

if __name__ == "__main__":
    print_header("GS_CONFIG - CONFIGURAÇÃO GLOBAL")

    # Valida base de dados
    print("\n🔍 Validando base de dados...")
    is_valid, errors = validate_database()

    if is_valid:
        print("✅ Base de dados validada com sucesso!")

        # Estatísticas
        basic_count = sum(1 for s in SKILLS_DATABASE.values() if not s['Pre_Reqs'])
        total_count = len(SKILLS_DATABASE)

        print(f"   Total de habilidades: {total_count}")
        print(f"   Habilidades básicas: {basic_count}")
        print(f"   Habilidades avançadas: {total_count - basic_count}")
    else:
        print(f"\n❌ {len(errors)} erro(s) encontrado(s):")
        for error in errors[:10]:
            print(f"  • {error}")

    # Exibe estatísticas
    print_statistics()

    # Lista todas as habilidades
    print_section("LISTA DE HABILIDADES")

    print("\n📚 Habilidades Básicas:")
    for skill_id, data in SKILLS_DATABASE.items():
        if not data['Pre_Reqs']:
            print_skill_info(skill_id)

    print("\n🎓 Habilidades Avançadas:")
    for skill_id, data in SKILLS_DATABASE.items():
        if data['Pre_Reqs']:
            print_skill_info(skill_id)

    print("\n" + "="*80)
    print("✅ Configuração carregada com sucesso!")
    print("="*80)
