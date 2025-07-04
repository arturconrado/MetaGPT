#!/usr/bin/env python3
"""
Script de Execução Rápida - POC Simples

Script para executar rapidamente a POC técnica do sistema de upgrade.
Foco apenas no essencial, sem complexidades.

Autor: Sistema MetaGPT
Versão: 1.0.0-simple
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime


def print_banner():
    """Imprime banner da POC."""
    print("\n" + "="*70)
    print("🚀 POC SIMPLES - UPGRADE IONIC/ANGULAR".center(70))
    print("Prova de Conceito Técnica - Apenas Core".center(70))
    print("="*70)
    print("\n📋 Características:")
    print("   ✅ Análise automática de projeto")
    print("   ✅ Backup seguro")
    print("   ✅ Upgrade simulado")
    print("   ✅ Relatório detalhado")
    print("   ❌ Sem QA complexo")
    print("   ❌ Sem testes extensivos")
    print("\n⏱️  Tempo estimado: 2-3 minutos")
    print("\n" + "-"*70)


def check_dependencies():
    """Verifica dependências básicas."""
    print("\n🔍 Verificando dependências...")
    
    required_files = [
        "simple_ionic_angular_upgrade.py",
        "simple_config.yaml"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"   ✅ {file}")
    
    if missing_files:
        print(f"\n❌ Arquivos obrigatórios não encontrados:")
        for file in missing_files:
            print(f"   ❌ {file}")
        print("\n💡 Certifique-se de que todos os arquivos da POC estão no diretório atual.")
        return False
    
    print("\n✅ Todas as dependências encontradas!")
    return True


async def run_quick_test():
    """Executa teste rápido da POC."""
    print("\n🧪 Executando teste rápido...")
    
    try:
        # Importar sistema
        from simple_ionic_angular_upgrade import SimpleUpgradeSystem
        
        # Criar sistema
        system = SimpleUpgradeSystem()
        print("   ✅ Sistema inicializado")
        
        # Testar configuração
        config_path = Path("simple_config.yaml")
        if config_path.exists():
            print("   ✅ Configuração carregada")
        
        # Simular projeto básico
        test_dir = Path("./test_project_simple")
        test_dir.mkdir(exist_ok=True)
        
        # Criar package.json mínimo
        package_json = {
            "name": "test-app",
            "version": "1.0.0",
            "dependencies": {
                "@angular/core": "^12.0.0",
                "@ionic/angular": "^5.0.0"
            }
        }
        
        import json
        with open(test_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        print("   ✅ Projeto de teste criado")
        
        # Testar análise
        from simple_ionic_angular_upgrade import SimpleAnalyzeAction
        analyzer = SimpleAnalyzeAction()
        project_info = await analyzer.run(str(test_dir))
        
        print(f"   ✅ Análise concluída: Angular {project_info.current_angular} → {project_info.target_angular}")
        
        # Limpar
        import shutil
        shutil.rmtree(test_dir)
        print("   ✅ Limpeza concluída")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False


async def run_full_demo():
    """Executa demonstração completa."""
    print("\n🎬 Executando demonstração completa...")
    
    try:
        # Importar e executar demo
        from demo_simple import SimpleDemoRunner
        
        demo = SimpleDemoRunner()
        success = await demo.run_complete_demo()
        
        return success
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        return False


def show_menu():
    """Mostra menu de opções."""
    print("\n📋 Opções disponíveis:")
    print("   1. Teste rápido (30 segundos)")
    print("   2. Demonstração completa (2-3 minutos)")
    print("   3. Sair")
    print("\n" + "-"*50)
    
    while True:
        try:
            choice = input("\n🔹 Escolha uma opção (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                print("❌ Opção inválida. Digite 1, 2 ou 3.")
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            return 3
        except EOFError:
            return 3


async def main():
    """Função principal."""
    print_banner()
    
    # Verificar dependências
    if not check_dependencies():
        return 1
    
    while True:
        choice = show_menu()
        
        if choice == 1:
            print("\n🚀 Iniciando teste rápido...")
            start_time = datetime.now()
            
            success = await run_quick_test()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if success:
                print(f"\n✅ Teste rápido concluído com sucesso!")
                print(f"⏱️  Duração: {duration:.1f}s")
                print("\n💡 O sistema está funcionando corretamente.")
            else:
                print(f"\n❌ Teste rápido falhou.")
                print(f"⏱️  Duração: {duration:.1f}s")
        
        elif choice == 2:
            print("\n🚀 Iniciando demonstração completa...")
            start_time = datetime.now()
            
            success = await run_full_demo()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if success:
                print(f"\n🎉 Demonstração concluída com sucesso!")
                print(f"⏱️  Duração: {duration:.1f}s")
                print("\n💡 Todos os componentes da POC funcionaram corretamente.")
            else:
                print(f"\n❌ Demonstração falhou.")
                print(f"⏱️  Duração: {duration:.1f}s")
        
        elif choice == 3:
            print("\n👋 Encerrando POC...")
            break
        
        # Perguntar se quer continuar
        print("\n" + "-"*50)
        try:
            continue_choice = input("\n🔄 Executar outra opção? (s/N): ").strip().lower()
            if continue_choice not in ['s', 'sim', 'y', 'yes']:
                print("\n👋 Encerrando POC...")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Encerrando POC...")
            break
    
    print("\n" + "="*70)
    print("🏁 POC SIMPLES FINALIZADA".center(70))
    print("Obrigado por testar o sistema!".center(70))
    print("="*70)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 POC interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)