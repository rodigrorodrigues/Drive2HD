#!/usr/bin/env python3
"""
Script para verificar a estrutura da pasta de destino
"""

import os
import glob

def check_directory_structure(path):
    """Verificar estrutura de diretórios"""
    print(f"=== VERIFICANDO ESTRUTURA DA PASTA: {path} ===")
    print()
    
    if not os.path.exists(path):
        print(f"ERRO: Pasta {path} não existe!")
        return
    
    # Listar todos os arquivos e pastas
    all_items = []
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, path)
            all_items.append(relative_path)
    
    print(f"Total de arquivos encontrados: {len(all_items)}")
    print()
    
    if not all_items:
        print("Nenhum arquivo encontrado!")
        return
    
    print("LISTA COMPLETA DE ARQUIVOS:")
    print("=" * 50)
    for item in sorted(all_items):
        print(f"📄 {item}")
    
    print("\n" + "=" * 50)
    
    # Agrupar por pasta pai
    folders = {}
    for item in all_items:
        parts = item.split(os.sep)
        if len(parts) > 1:
            parent_folder = parts[0]
            if parent_folder not in folders:
                folders[parent_folder] = []
            folders[parent_folder].append(item)
        else:
            if "RAIZ" not in folders:
                folders["RAIZ"] = []
            folders["RAIZ"].append(item)
    
    print("\nESTRUTURA POR PASTAS:")
    print("=" * 50)
    
    for folder, files in sorted(folders.items()):
        print(f"\n📁 {folder}:")
        for file in sorted(files):
            print(f"  📄 {file}")
    
    print("\n" + "=" * 50)
    
    # Verificar se há arquivos na raiz que deveriam estar em subpastas
    root_files = folders.get("RAIZ", [])
    if root_files:
        print(f"\n⚠️  ATENÇÃO: {len(root_files)} arquivos encontrados na raiz!")
        print("Isso pode indicar um problema na estrutura de pastas.")
        for file in root_files:
            print(f"  📄 {file}")
    
    # Verificar se há pastas com nomes estranhos
    suspicious_folders = []
    for folder in folders.keys():
        if folder != "RAIZ" and ("_" in folder or ":" in folder or "/" in folder):
            suspicious_folders.append(folder)
    
    if suspicious_folders:
        print(f"\n⚠️  ATENÇÃO: {len(suspicious_folders)} pastas com nomes suspeitos encontradas!")
        for folder in suspicious_folders:
            print(f"  📁 {folder}")

if __name__ == '__main__':
    path = r"C:\Users\Rodrigo Rodrigues\Documents\testehd"
    check_directory_structure(path) 