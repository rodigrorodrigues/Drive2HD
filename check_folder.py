#!/usr/bin/env python3
"""
Script para verificar a estrutura da pasta de destino
"""

import os

def check_folder_structure(path):
    """Verificar estrutura de uma pasta"""
    print(f"=== VERIFICANDO ESTRUTURA DA PASTA: {path} ===")
    print()
    
    if not os.path.exists(path):
        print(f"❌ Pasta {path} não existe!")
        return
    
    print("ESTRUTURA ENCONTRADA:")
    print("=" * 50)
    
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
        for file in files:
            print(f"{sub_indent}📄 {file}")
    
    print("\n" + "=" * 50)
    
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

if __name__ == '__main__':
    import sys
    target_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    check_folder_structure(target_path)