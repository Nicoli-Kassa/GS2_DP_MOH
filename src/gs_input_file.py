"""
CONFIGURAÇÃO DE DADOS PARA TESTES - Global Solution MOH

Arquivo centralizado com todas as estruturas de dados usadas nos testes
"""

import random
import numpy as np

# ============================================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================================
GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)
np.random.seed(GLOBAL_SEED)

# Constantes globais
MIN_ADAPTABILITY = 100
MAX_TIME_HOURS = 10000
MAX_COMPLEXITY = 100

# ============================================================================
# DATABASE COMPLETO DE HABILIDADES (ALINHADO COM gs_config.py)
# ============================================================================
SKILLS_DATABASE = {
    # HARD SKILLS BÁSICAS (H1-H7) - SEM PRÉ-REQUISITOS
    'H1': {
        'Nome': 'Lógica de Programação',
        'Tempo': 40,
        'Valor': 10,
        'Complexidade': 2,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H2': {
        'Nome': 'Estruturas de Dados',
        'Tempo': 50,
        'Valor': 12,
        'Complexidade': 3,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H3': {
        'Nome': 'Algoritmos',
        'Tempo': 60,
        'Valor': 15,
        'Complexidade': 4,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H4': {
        'Nome': 'Banco de Dados',
        'Tempo': 45,
        'Valor': 11,
        'Complexidade': 3,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H5': {
        'Nome': 'Redes',
        'Tempo': 35,
        'Valor': 9,
        'Complexidade': 2,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H6': {
        'Nome': 'Sistemas Operacionais',
        'Tempo': 40,
        'Valor': 10,
        'Complexidade': 3,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    'H7': {
        'Nome': 'Engenharia de Software',
        'Tempo': 55,
        'Valor': 13,
        'Complexidade': 4,
        'Pre_Reqs': [],
        'Categoria': 'Hard_Basica'
    },
    
    # SOFT SKILLS INTERMEDIÁRIAS (S1-S3)
    'S1': {
        'Nome': 'Python Avançado',
        'Tempo': 70,
        'Valor': 18,
        'Complexidade': 5,
        'Pre_Reqs': ['H1', 'H2'],
        'Categoria': 'Soft_Intermediaria'
    },
    'S2': {
        'Nome': 'Java Enterprise',
        'Tempo': 80,
        'Valor': 20,
        'Complexidade': 6,
        'Pre_Reqs': ['H1', 'H2', 'H7'],
        'Categoria': 'Soft_Intermediaria'
    },
    'S3': {
        'Nome': 'React',
        'Tempo': 65,
        'Valor': 22,
        'Complexidade': 5,
        'Pre_Reqs': ['H1'],
        'Categoria': 'Soft_Intermediaria'
    },
    
    # SOFT SKILLS AVANÇADAS (S4-S9)
    'S4': {
        'Nome': 'Machine Learning',
        'Tempo': 100,
        'Valor': 30,
        'Complexidade': 8,
        'Pre_Reqs': ['H2', 'H3', 'S1'],
        'Categoria': 'Soft_Avancada'
    },
    'S5': {
        'Nome': 'Cybersecurity',
        'Tempo': 90,
        'Valor': 25,
        'Complexidade': 7,
        'Pre_Reqs': ['H5', 'H6'],
        'Categoria': 'Soft_Avancada'
    },
    'S6': {
        'Nome': 'IA Generativa',
        'Tempo': 120,
        'Valor': 40,
        'Complexidade': 9,
        'Pre_Reqs': ['S4'],
        'Categoria': 'Soft_Avancada'
    },
    'S7': {
        'Nome': 'Cloud Architecture',
        'Tempo': 110,
        'Valor': 35,
        'Complexidade': 8,
        'Pre_Reqs': ['H4', 'H5', 'H6'],
        'Categoria': 'Soft_Avancada'
    },
    'S8': {
        'Nome': 'Microservices',
        'Tempo': 85,
        'Valor': 28,
        'Complexidade': 7,
        'Pre_Reqs': ['S2', 'H4'],
        'Categoria': 'Soft_Avancada'
    },
    'S9': {
        'Nome': 'DevOps',
        'Tempo': 75,
        'Valor': 26,
        'Complexidade': 6,
        'Pre_Reqs': ['H6', 'H7'],
        'Categoria': 'Soft_Avancada'
    },
    
    # HABILIDADES ESPECIALIZADAS (H11-H12)
    'H11': {
        'Nome': 'Big Data',
        'Tempo': 95,
        'Valor': 32,
        'Complexidade': 8,
        'Pre_Reqs': ['H4', 'S1'],
        'Categoria': 'Hard_Especializada'
    },
    'H12': {
        'Nome': 'Blockchain',
        'Tempo': 88,
        'Valor': 29,
        'Complexidade': 7,
        'Pre_Reqs': ['H4', 'S5'],
        'Categoria': 'Hard_Especializada'
    }
}

# ============================================================================
# CONJUNTOS DE HABILIDADES (ALINHADO COM gs_config.py)
# ============================================================================
BASIC_SKILLS = {'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7'}
CRITICAL_SKILLS = {'S3', 'S5', 'S7', 'S8', 'S9'}
ADVANCED_SKILLS = {'S4', 'S6', 'H11', 'H12'}
ALL_SOFT_SKILLS = {'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9'}
ALL_HARD_SKILLS = {'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H11', 'H12'}

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def print_header(title: str):
    print("\n" + "="*80)
    print(f"{title}")
    print("="*80)

def validate_database(db: dict):
    """Valida o database"""
    errors = []
    
    # Campos obrigatórios
    required_fields = ['Nome', 'Tempo', 'Valor', 'Complexidade', 'Pre_Reqs']
    
    for skill_id, skill_data in db.items():
        # Verifica campos
        for field in required_fields:
            if field not in skill_data:
                errors.append(f"{skill_id}: campo '{field}' faltando")
        
        # Verifica pré-requisitos
        if 'Pre_Reqs' in skill_data:
            for prereq in skill_data['Pre_Reqs']:
                if prereq not in db:
                    errors.append(f"{skill_id}: pré-requisito '{prereq}' não existe")
        
        # Verifica valores positivos
        if 'Valor' in skill_data and skill_data['Valor'] <= 0:
            errors.append(f"{skill_id}: Valor deve ser positivo")
        if 'Tempo' in skill_data and skill_data['Tempo'] <= 0:
            errors.append(f"{skill_id}: Tempo deve ser positivo")
        if 'Complexidade' in skill_data and skill_data['Complexidade'] <= 0:
            errors.append(f"{skill_id}: Complexidade deve ser positiva")
    
    return len(errors) == 0, errors

# ============================================================================
# FIXTURES PARA TESTES
# ============================================================================
class TestFixtures:
    """Cenários de teste para cada desafio"""
    
    # Desafio 1
    CHALLENGE1_SCENARIOS = {
        'basic': {
            'target': 'S6',
            'max_time': 600,
            'max_complexity': 50,
            'expected_feasible': True
        }
    }
    
    # Desafio 2
    CHALLENGE2_TEST_ORDERS = {
        'optimal_candidate': ['S3', 'S5', 'S7', 'S8', 'S9']
    }
    
    # Desafio 3
    CHALLENGE3_SCENARIOS = {
        'standard': {
            'basic_skills': BASIC_SKILLS,
            'min_adaptability': MIN_ADAPTABILITY,
            'expected_success': True
        }
    }
    
    # Desafio 4
    CHALLENGE4_TEST_DATA = {
        'medium': [f'S{i+1}' for i in range(9)]
    }
    
    # Desafio 5
    CHALLENGE5_PROFILES = {
        'basic': {'H1', 'H2', 'H3'}
    }

# ============================================================================
# EXPORTS
# ============================================================================
__all__ = [
    'SKILLS_DATABASE',
    'BASIC_SKILLS',
    'CRITICAL_SKILLS',
    'ADVANCED_SKILLS',
    'ALL_SOFT_SKILLS',
    'ALL_HARD_SKILLS',
    'MIN_ADAPTABILITY',
    'MAX_TIME_HOURS',
    'MAX_COMPLEXITY',
    'GLOBAL_SEED',
    'validate_database',
    'TestFixtures',
    'print_header'
]
