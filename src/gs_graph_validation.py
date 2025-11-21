"""
Módulo de validação do grafo de habilidades
Detecta ciclos, nós órfãos e valida estrutura
"""

from typing import Dict, List, Set, Tuple
from collections import deque
from gs_config import SKILLS_DATABASE, print_header

class GraphValidator:
    """Classe para validação completa do grafo de habilidades"""
    
    def __init__(self, skills_db: Dict):
        """
        Inicializa o validador com o banco de dados de habilidades.
        
        Args:
            skills_db: Dicionário de habilidades
        """
        self.skills_db = skills_db
        self.all_skill_ids = set(skills_db.keys())
        
    def validate_graph(self, verbose: bool = True) -> Tuple[bool, Dict]:
        """
        Valida todo o grafo de habilidades.
        
        Args:
            verbose: Se True, imprime mensagens detalhadas
            
        Returns:
            Tuple[bool, Dict]: (é_válido, relatório_detalhado)
        """
        if verbose:
            print_header("🔍 VALIDAÇÃO DO GRAFO DE HABILIDADES")
        
        report = {
            'valid': True,
            'cycles': [],
            'orphan_nodes': [],
            'missing_prereqs': [],
            'topological_order': []
        }
        
        # 1. Verifica pré-requisitos inexistentes
        orphans = self._check_orphan_prereqs()
        if orphans:
            report['valid'] = False
            report['orphan_nodes'] = orphans
            if verbose:
                print("\n❌ ERRO: Pré-requisitos inexistentes detectados!")
                for skill_id, missing in orphans:
                    print(f"   • {skill_id} requer {missing} que não existe")
                return False, report
        
        if verbose:
            print("\n✅ Todos os pré-requisitos existem no banco de dados")
        
        # 2. Detecta ciclos usando DFS
        has_cycle, cycle_path = self._detect_cycles()
        if has_cycle:
            report['valid'] = False
            report['cycles'] = cycle_path
            if verbose:
                print(f"\n❌ ERRO: Ciclo detectado no grafo!")
                print(f"   Caminho do ciclo: {' → '.join(cycle_path)}")
                return False, report
        
        if verbose:
            print("✅ Nenhum ciclo detectado (grafo acíclico)")
        
        # 3. Ordenação topológica
        topo_order = self._topological_sort()
        report['topological_order'] = topo_order
        
        if verbose:
            print(f"\n✅ Ordenação topológica válida:")
            print(f"   {' → '.join(topo_order)}")
            
            # Estatísticas do grafo
            self._print_graph_statistics()
        
        return True, report
    
    def _check_orphan_prereqs(self) -> List[Tuple[str, str]]:
        """
        Verifica se há pré-requisitos que não existem no banco de dados.
        
        Returns:
            Lista de tuplas (skill_id, prereq_missing)
        """
        orphans = []
        
        for skill_id, skill_data in self.skills_db.items():
            prereqs = skill_data.get('Pre_Reqs', [])
            for prereq in prereqs:
                if prereq not in self.all_skill_ids:
                    orphans.append((skill_id, prereq))
        
        return orphans
    
    def _detect_cycles(self) -> Tuple[bool, List[str]]:
        """
        Detecta ciclos no grafo usando DFS.
        
        Returns:
            Tuple[bool, List[str]]: (tem_ciclo, caminho_do_ciclo)
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {skill: WHITE for skill in self.all_skill_ids}
        parent = {skill: None for skill in self.all_skill_ids}
        
        def dfs_visit(node: str) -> Tuple[bool, List[str]]:
            color[node] = GRAY
            
            prereqs = self.skills_db[node].get('Pre_Reqs', [])
            for prereq in prereqs:
                if color[prereq] == GRAY:
                    # Ciclo detectado! Reconstrói o caminho
                    cycle = [prereq, node]
                    current = node
                    while parent[current] and parent[current] != prereq:
                        current = parent[current]
                        cycle.insert(1, current)
                    cycle.append(prereq)  # Fecha o ciclo
                    return True, cycle
                
                if color[prereq] == WHITE:
                    parent[prereq] = node
                    has_cycle, path = dfs_visit(prereq)
                    if has_cycle:
                        return True, path
            
            color[node] = BLACK
            return False, []
        
        # Executa DFS em todos os nós não visitados
        for skill in self.all_skill_ids:
            if color[skill] == WHITE:
                has_cycle, cycle_path = dfs_visit(skill)
                if has_cycle:
                    return True, cycle_path
        
        return False, []
    
    def _topological_sort(self) -> List[str]:
        """
        Realiza ordenação topológica usando algoritmo de Kahn (BFS).
        
        Returns:
            Lista com ordem topológica das habilidades
        """
        # Calcula grau de entrada (in-degree) para cada nó
        in_degree = {skill: 0 for skill in self.all_skill_ids}
        
        for skill_id, skill_data in self.skills_db.items():
            prereqs = skill_data.get('Pre_Reqs', [])
            for prereq in prereqs:
                in_degree[skill_id] += 1
        
        # Fila com nós de grau 0
        queue = deque([skill for skill, degree in in_degree.items() if degree == 0])
        topo_order = []
        
        while queue:
            current = queue.popleft()
            topo_order.append(current)
            
            # Para cada habilidade que depende da atual
            for skill_id, skill_data in self.skills_db.items():
                if current in skill_data.get('Pre_Reqs', []):
                    in_degree[skill_id] -= 1
                    if in_degree[skill_id] == 0:
                        queue.append(skill_id)
        
        return topo_order
    
    def _print_graph_statistics(self):
        """Imprime estatísticas do grafo"""
        print("\n📊 ESTATÍSTICAS DO GRAFO:")
        
        n_nodes = len(self.all_skill_ids)
        n_edges = sum(len(skill['Pre_Reqs']) for skill in self.skills_db.values())
        
        # Calcula graus
        in_degree = {}
        out_degree = {skill: 0 for skill in self.all_skill_ids}
        
        for skill_id in self.all_skill_ids:
            prereqs = self.skills_db[skill_id].get('Pre_Reqs', [])
            in_degree[skill_id] = len(prereqs)
            for prereq in prereqs:
                out_degree[prereq] += 1
        
        # Nós fonte (sem pré-requisitos) e sorvedouros (ninguém depende)
        sources = [s for s, d in in_degree.items() if d == 0]
        sinks = [s for s, d in out_degree.items() if d == 0]
        
        print(f"   • Nós (habilidades): {n_nodes}")
        print(f"   • Arestas (dependências): {n_edges}")
        print(f"   • Nós fonte (básicos): {len(sources)} - {sources}")
        print(f"   • Nós sorvedouro (terminais): {len(sinks)} - {sinks}")
        print(f"   • Grau médio de entrada: {n_edges/n_nodes:.2f}")
        print(f"   • Densidade: {n_edges/(n_nodes*(n_nodes-1)):.3f}")

def validate_before_optimization(skills_db: Dict = None) -> bool:
    """
    Função auxiliar para validar o grafo antes de otimizar.
    
    Args:
        skills_db: Banco de dados de habilidades (usa padrão se None)
        
    Returns:
        bool: True se válido, False caso contrário (e levanta exceção)
    """
    if skills_db is None:
        skills_db = SKILLS_DATABASE
    
    validator = GraphValidator(skills_db)
    is_valid, report = validator.validate_graph(verbose=True)
    
    if not is_valid:
        error_msg = "\n🚫 VALIDAÇÃO FALHOU - Não é possível prosseguir!\n"
        
        if report['orphan_nodes']:
            error_msg += "   Pré-requisitos inexistentes detectados.\n"
        
        if report['cycles']:
            error_msg += "   Ciclos detectados no grafo.\n"
        
        raise ValueError(error_msg)
    
    return True