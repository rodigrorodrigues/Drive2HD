#!/usr/bin/env python3
"""
Script para verificar a estrutura da pasta de destino
Execute este script para ver como ficaram as pastas
"""

import os

def verificar_estrutura(path=None):
    """Verificar estrutura da pasta de destino"""
    if path is None:
        path = os.getcwd()
    
    print(f"=== VERIFICANDO ESTRUTURA DA PASTA: {path} ===")
    print()
    
    if not os.path.exists(path):
        print(f"❌ Pasta {path} não existe!")
        return
    
    print("ESTRUTURA ENCONTRADA:")
    print("=" * 60)
    
    # Listar todos os arquivos e pastas
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root)
        
        if level == 0:
            print(f"📁 {folder_name}/ (RAIZ)")
        else:
            print(f"{indent}📁 {folder_name}/")
        
        sub_indent = '  ' * (level + 1)
        for file in sorted(files):
            print(f"{sub_indent}📄 {file}")
    
    print("\n" + "=" * 60)
    
    # Contar arquivos e pastas
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(path):
        total_files += len(files)
        total_dirs += len(dirs)
    
    print(f"📊 RESUMO:")
    print(f"   📁 Pastas: {total_dirs}")
    print(f"   📄 Arquivos: {total_files}")
    print(f"   📂 Total de itens: {total_files + total_dirs}")
    
    # Verificar se há arquivos na raiz que deveriam estar em subpastas
    print(f"\n🔍 ANÁLISE:")
    
    root_files = []
    subfolder_files = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if root == path:  # Arquivo na raiz
                root_files.append(file)
            else:  # Arquivo em subpasta
                relative_path = os.path.relpath(root, path)
                subfolder_files.append(f"{relative_path}/{file}")
    
    if root_files:
        print(f"⚠️  {len(root_files)} arquivos encontrados na raiz:")
        for file in sorted(root_files):
            print(f"   📄 {file}")
    else:
        print("✅ Nenhum arquivo na raiz (bom!)")
    
    if subfolder_files:
        print(f"\n📁 {len(subfolder_files)} arquivos em subpastas:")
        for file in sorted(subfolder_files):
            print(f"   📄 {file}")

if __name__ == '__main__':
    import sys
    target_path = sys.argv[1] if len(sys.argv) > 1 else None
    verificar_estrutura(target_path)