#!/usr/bin/env python3
"""
Script de teste para verificar a sanitização de nomes de arquivos
"""

def sanitize_filename(filename):
    """Sanitizar nome de arquivo removendo caracteres inválidos do Windows"""
    # Caracteres inválidos no Windows: < > : " | ? * \ /
    invalid_chars = '<>:"|?*\\/'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remover espaços no início e fim
    filename = filename.strip()
    
    # Se o nome ficou vazio, usar nome padrão
    if not filename:
        filename = "unnamed_file"
    
    return filename

def test_sanitization():
    """Testar sanitização de nomes de arquivos"""
    test_cases = [
        "Workflow Backups Sunday 11:00 AM 27-07-2025",
        "My workflow 4.json",
        "Listas - Teste.json",
        "Folder/with/slashes",
        "File:with:colons",
        "File*with*asterisks",
        "File?with?question?marks",
        "File<with>invalid<chars>",
        "File\"with\"quotes",
        "File|with|pipes",
        "File\\with\\backslashes",
        "   File with spaces   ",
        "",
        "Normal file name.txt"
    ]
    
    print("=== TESTE DE SANITIZAÇÃO DE NOMES DE ARQUIVOS ===")
    print()
    
    for original in test_cases:
        sanitized = sanitize_filename(original)
        print(f"Original: '{original}'")
        print(f"Sanitizado: '{sanitized}'")
        print("-" * 50)

if __name__ == '__main__':
    test_sanitization() 