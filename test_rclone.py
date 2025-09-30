#!/usr/bin/env python3
"""
Script para testar configuração do Rclone
"""

import subprocess
import sys
import os

def test_rclone_installation():
    """Testar se Rclone está instalado"""
    print("=== TESTANDO INSTALAÇÃO DO RCLONE ===")
    
    try:
        result = subprocess.run(['rclone', 'version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Rclone encontrado!")
            version_lines = result.stdout.strip().split('\n')
            print(f"Versão: {version_lines[0]}")
            return True
        else:
            print("❌ Rclone não encontrado!")
            print("Execute: setup_rclone.bat")
            return False
            
    except FileNotFoundError:
        print("❌ Rclone não encontrado!")
        print("Execute: setup_rclone.bat")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar Rclone: {str(e)}")
        return False

def test_rclone_remotes():
    """Testar remotes configurados"""
    print("\n=== TESTANDO REMOTES ===")
    
    try:
        result = subprocess.run(['rclone', 'listremotes'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            remotes = result.stdout.strip().split('\n')
            if remotes and remotes[0]:
                print("✅ Remotes encontrados:")
                for remote in remotes:
                    if remote.strip():
                        print(f"   📁 {remote.strip()}")
                return True
            else:
                print("❌ Nenhum remote configurado!")
                print("Execute: rclone config")
                return False
        else:
            print(f"❌ Erro ao listar remotes: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar remotes: {str(e)}")
        return False

def test_google_drive_connection(remote_name="gdrive"):
    """Testar conexão com Google Drive"""
    print(f"\n=== TESTANDO CONEXÃO COM GOOGLE DRIVE ({remote_name}) ===")
    
    try:
        # Testar listagem de pastas
        result = subprocess.run(['rclone', 'lsd', f'{remote_name}:'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Conexão com Google Drive OK!")
            print("📁 Pastas encontradas:")
            
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    print(f"   {line.strip()}")
            
            return True
        else:
            print(f"❌ Erro na conexão: {result.stderr}")
            print("Verifique a configuração: rclone config")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {str(e)}")
        return False

def test_sync_simulation(remote_name="gdrive", test_path="./test_sync"):
    """Testar sincronização (modo seco)"""
    print(f"\n=== TESTANDO SINCRONIZAÇÃO (MODO SECO) ===")
    
    try:
        # Criar pasta de teste
        os.makedirs(test_path, exist_ok=True)
        
        # Executar sync em modo seco
        cmd = ['rclone', 'sync', f'{remote_name}:', test_path, '--dry-run']
        
        print(f"Comando: {' '.join(cmd)}")
        print("Executando...")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Sincronização testada com sucesso!")
            
            # Mostrar algumas linhas da saída
            lines = result.stdout.strip().split('\n')
            print(f"📊 {len(lines)} itens processados")
            
            # Mostrar primeiras linhas
            for i, line in enumerate(lines[:5]):
                if line.strip():
                    print(f"   {line.strip()}")
            
            if len(lines) > 5:
                print(f"   ... e mais {len(lines) - 5} itens")
            
            return True
        else:
            print(f"❌ Erro na sincronização: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar sincronização: {str(e)}")
        return False
    finally:
        # Limpar pasta de teste
        try:
            import shutil
            shutil.rmtree(test_path, ignore_errors=True)
        except:
            pass

def main():
    """Função principal"""
    print("Drive2HD - Teste de Configuração Rclone")
    print("=" * 50)
    
    # Testar instalação
    if not test_rclone_installation():
        return
    
    # Testar remotes
    if not test_rclone_remotes():
        return
    
    # Testar conexão
    if not test_google_drive_connection():
        return
    
    # Testar sincronização
    if not test_sync_simulation():
        return
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ Rclone está configurado corretamente!")
    print("✅ Você pode usar: python main_rclone.py")
    print("=" * 50)

if __name__ == '__main__':
    main()
    input("\nPressione Enter para sair...") 