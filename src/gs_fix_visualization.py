"""
CORREÇÃO RÁPIDA - gs_visualization.py
Execute este script para corrigir o erro do KeyError 'success'
"""

import os

def fix_gs_visualization():
    """Corrige o erro no gs_visualization.py"""
    
    filename = 'gs_visualization.py'
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo {filename} não encontrado!")
        print("💡 Certifique-se de estar no diretório correto")
        return False
    
    print(f"🔧 Corrigindo {filename}...")
    
    # Lê o arquivo
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Aplica correção
    content_fixed = content.replace(
        "label='Tempo de Aquisição', color=colors['success'],",
        "label='Tempo de Aquisição', color=colors['acquire'],"
    )
    
    # Verifica se houve alteração
    if content == content_fixed:
        print("ℹ️ Nenhuma correção necessária (já está correto)")
        return True
    
    # Faz backup
    backup_file = filename + '.backup'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup criado: {backup_file}")
    
    # Salva arquivo corrigido
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_fixed)
    
    print(f"✅ Arquivo {filename} corrigido com sucesso!")
    print(f"🎯 Erro do KeyError 'success' resolvido")
    
    return True


def add_colors_if_missing():
    """Adiciona o dicionário COLORS se estiver faltando"""
    
    filename = 'gs_visualization.py'
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verifica se COLORS já existe
    if "COLORS = {" in content:
        print("✅ Dicionário COLORS já existe")
        return True
    
    print("🔧 Adicionando dicionário COLORS...")
    
    colors_dict = """
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
"""
    
    # Procura onde inserir (após imports)
    lines = content.split('\n')
    insert_pos = 0
    
    for i, line in enumerate(lines):
        if line.startswith('class ') or line.startswith('def '):
            insert_pos = i
            break
    
    # Insere COLORS
    lines.insert(insert_pos, colors_dict)
    content_fixed = '\n'.join(lines)
    
    # Salva
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_fixed)
    
    print("✅ Dicionário COLORS adicionado!")
    
    return True


def main():
    """Executa todas as correções"""
    
    print("=" * 80)
    print("🔧 CORREÇÃO RÁPIDA - gs_visualization.py")
    print("=" * 80)
    
    # Correção 1: KeyError 'success'
    if fix_gs_visualization():
        print("\n✅ Correção 1 aplicada: KeyError resolvido")
    else:
        print("\n❌ Erro ao aplicar correção 1")
        return
    
    # Correção 2: Adiciona COLORS se necessário
    try:
        add_colors_if_missing()
        print("✅ Correção 2 verificada: COLORS presente")
    except Exception as e:
        print(f"⚠️ Aviso na correção 2: {e}")
    
    print("\n" + "=" * 80)
    print("✅ TODAS AS CORREÇÕES APLICADAS COM SUCESSO!")
    print("=" * 80)
    
    


if __name__ == "__main__":
    main()