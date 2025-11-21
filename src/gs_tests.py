#!/usr/bin/env python3
"""
SCRIPT DE TESTES CORRIGIDO - Global Solution MOH
"""

import sys
import unittest
import time

def print_banner():
    print("\n" + "="*80)
    print(" "*20 + "🧪 GLOBAL SOLUTION 2 - SUITE DE TESTES 🧪")
    print("="*80)

def validate_input_file():
    """Valida o arquivo gs_input_file.py"""
    print("\n📋 Validando gs_input_file.py...")
    try:
        from gs_input_file import (
            SKILLS_DATABASE,
            BASIC_SKILLS,
            CRITICAL_SKILLS,
            validate_database
        )
        print("✅ Módulo gs_input_file.py importado com sucesso")
        
        # Valida database
        is_valid, errors = validate_database(SKILLS_DATABASE)
        
        if is_valid:
            print("✅ Database validado com sucesso!")
            print(f"\n📊 Estatísticas:")
            print(f"   Total de skills: {len(SKILLS_DATABASE)}")
            print(f"   Skills básicas: {len(BASIC_SKILLS)}")
            print(f"   Skills críticas: {len(CRITICAL_SKILLS)}")
            return True
        else:
            print("❌ Erros encontrados no database:")
            for error in errors:
                print(f"   • {error}")
            return False
            
    except ImportError as e:
        print(f"❌ Erro ao importar gs_input_file.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

# ============================================================================
# TESTES UNITÁRIOS
# ============================================================================

class TestGraphValidation(unittest.TestCase):
    """Testes de validação do grafo"""
    
    def setUp(self):
        """Setup executado antes de cada teste"""
        from gs_input_file import SKILLS_DATABASE
        self.db = SKILLS_DATABASE
    
    def test_database_not_empty(self):
        """Verifica se o database não está vazio"""
        self.assertGreater(len(self.db), 0, "Database está vazio")
    
    def test_positive_values(self):
        """Verifica se todos os valores são positivos"""
        for skill_id, data in self.db.items():
            with self.subTest(skill=skill_id):
                self.assertGreater(data['Tempo'], 0, f"{skill_id}: Tempo deve ser > 0")
                self.assertGreater(data['Valor'], 0, f"{skill_id}: Valor deve ser > 0")
                self.assertGreater(data['Complexidade'], 0, f"{skill_id}: Complexidade deve ser > 0")
    
    def test_all_prereqs_exist(self):
        """Verifica se todos os pré-requisitos existem"""
        all_skills = set(self.db.keys())
        for skill_id, data in self.db.items():
            for prereq in data['Pre_Reqs']:
                with self.subTest(skill=skill_id, prereq=prereq):
                    self.assertIn(prereq, all_skills, 
                                f"{skill_id}: Pré-requisito {prereq} não existe")

class TestChallenges(unittest.TestCase):
    """Testes dos desafios"""
    
    def setUp(self):
        """Setup executado antes de cada teste"""
        from gs_input_file import SKILLS_DATABASE
        from gs_config import TARGET_SKILL, MAX_TIME, MAX_COMPLEXITY
        self.db = SKILLS_DATABASE
        self.target = TARGET_SKILL
        self.max_time = MAX_TIME
        self.max_complexity = MAX_COMPLEXITY
    
    def test_challenge1_imports(self):
        """Testa se o módulo do desafio 1 pode ser importado"""
        try:
            from gs_challenge1 import ImprovedMaxValuePathDP
            solver = ImprovedMaxValuePathDP(self.db, self.target)
            self.assertIsNotNone(solver)
        except ImportError as e:
            self.fail(f"Erro ao importar desafio 1: {e}")
    
    def test_challenge2_imports(self):
        """Testa se o módulo do desafio 2 pode ser importado"""
        try:
            from gs_challenge2 import ImprovedCriticalSkillsAnalyzer
            from gs_config import CRITICAL_SKILLS
            analyzer = ImprovedCriticalSkillsAnalyzer(self.db, CRITICAL_SKILLS)
            self.assertIsNotNone(analyzer)
        except ImportError as e:
            self.fail(f"Erro ao importar desafio 2: {e}")
    
    def test_challenge3_imports(self):
        """Testa se o módulo do desafio 3 pode ser importado"""
        try:
            from gs_challenge3 import ImprovedAdaptabilityOptimizer
            from gs_config import BASIC_SKILLS, MIN_ADAPTABILITY
            optimizer = ImprovedAdaptabilityOptimizer(self.db, BASIC_SKILLS, MIN_ADAPTABILITY)
            self.assertIsNotNone(optimizer)
        except ImportError as e:
            self.fail(f"Erro ao importar desafio 3: {e}")
    
    def test_challenge4_imports(self):
        """Testa se o módulo do desafio 4 pode ser importado"""
        try:
            from gs_challenge4 import SprintDivider, ImprovedSortingAlgorithms
            divider = SprintDivider(self.db)
            self.assertIsNotNone(divider)
        except ImportError as e:
            self.fail(f"Erro ao importar desafio 4: {e}")
    
    def test_challenge5_imports(self):
        """Testa se o módulo do desafio 5 pode ser importado"""
        try:
            from gs_challenge5 import ImprovedSkillRecommender
            recommender = ImprovedSkillRecommender(self.db)
            self.assertIsNotNone(recommender)
        except ImportError as e:
            self.fail(f"Erro ao importar desafio 5: {e}")

class TestDataStructures(unittest.TestCase):
    """Testes das estruturas de dados"""
    
    def setUp(self):
        """Setup executado antes de cada teste"""
        from gs_input_file import SKILLS_DATABASE, BASIC_SKILLS, CRITICAL_SKILLS
        self.db = SKILLS_DATABASE
        self.basic = BASIC_SKILLS
        self.critical = CRITICAL_SKILLS
    
    def test_basic_skills_exist(self):
        """Verifica se todas as skills básicas existem no database"""
        for skill_id in self.basic:
            with self.subTest(skill=skill_id):
                self.assertIn(skill_id, self.db, f"Skill básica {skill_id} não existe")
    
    def test_critical_skills_exist(self):
        """Verifica se todas as skills críticas existem no database"""
        for skill_id in self.critical:
            with self.subTest(skill=skill_id):
                self.assertIn(skill_id, self.db, f"Skill crítica {skill_id} não existe")
    
    def test_required_fields(self):
        """Verifica se todos os campos obrigatórios existem"""
        required_fields = ['Nome', 'Tempo', 'Valor', 'Complexidade', 'Pre_Reqs', 'Categoria']
        for skill_id, data in self.db.items():
            for field in required_fields:
                with self.subTest(skill=skill_id, field=field):
                    self.assertIn(field, data, f"{skill_id}: Campo {field} ausente")

# ============================================================================
# RUNNER
# ============================================================================

def run_tests_suite(verbosity=2):
    """Executa todos os testes"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona todos os testes
    suite.addTests(loader.loadTestsFromTestCase(TestGraphValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestChallenges))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStructures))
    
    # Executa
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result

def main():
    """Função principal"""
    print_banner()
    
    # Valida input file primeiro
    if not validate_input_file():
        print("\n❌ Validação do input file falhou!")
        sys.exit(1)
    
    result = run_tests_suite(verbosity=2)
    
    # Resumo
    print("\n" + "="*80)
    print("RESUMO")
    print("="*80)
    print(f"\nTotal de testes: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️ Erros: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        sys.exit(1)

if __name__ == "__main__":
    main()
