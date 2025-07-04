#!/usr/bin/env python3
"""
Demo Simples - Sistema de Upgrade Ionic/Angular

Demonstração técnica focada apenas no core funcional.
Sem QA, sem testes complexos, apenas o essencial.

Autor: Sistema MetaGPT
Versão: 1.0.0-simple
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Importar o sistema simples
try:
    from simple_ionic_angular_upgrade import (
        SimpleUpgradeSystem,
        ProjectInfo,
        UpgradeResult
    )
except ImportError as e:
    print(f"❌ Erro ao importar sistema: {e}")
    print("Certifique-se de que o arquivo simple_ionic_angular_upgrade.py está no mesmo diretório.")
    sys.exit(1)


class SimpleDemoRunner:
    """Executor da demonstração simples."""
    
    def __init__(self):
        self.demo_dir = Path("./demo_simple_ionic_project")
        self.system = SimpleUpgradeSystem()
    
    def print_header(self, title: str):
        """Imprime cabeçalho formatado."""
        print(f"\n{'='*60}")
        print(f"{title.center(60)}")
        print(f"{'='*60}")
    
    def print_step(self, step: str):
        """Imprime passo da demonstração."""
        print(f"\n🔹 {step}")
        print(f"{'─'*50}")
    
    async def create_demo_project(self):
        """Cria projeto demo para demonstração."""
        self.print_step("Criando Projeto Demo")
        
        # Criar diretório
        self.demo_dir.mkdir(exist_ok=True)
        
        # Criar package.json com versões antigas
        package_json = {
            "name": "demo-ionic-angular-app",
            "version": "1.0.0",
            "description": "Projeto demo para upgrade Ionic/Angular",
            "scripts": {
                "ng": "ng",
                "start": "ng serve",
                "build": "ng build",
                "test": "ng test",
                "lint": "ng lint",
                "e2e": "ng e2e"
            },
            "dependencies": {
                "@angular/animations": "^12.2.0",
                "@angular/common": "^12.2.0",
                "@angular/core": "^12.2.0",
                "@angular/forms": "^12.2.0",
                "@angular/platform-browser": "^12.2.0",
                "@angular/platform-browser-dynamic": "^12.2.0",
                "@angular/router": "^12.2.0",
                "@ionic/angular": "^5.9.0",
                "rxjs": "~6.6.0",
                "tslib": "^2.2.0",
                "zone.js": "~0.11.4"
            },
            "devDependencies": {
                "@angular-devkit/build-angular": "^12.2.0",
                "@angular/cli": "^12.2.0",
                "@angular/compiler": "^12.2.0",
                "@angular/compiler-cli": "^12.2.0",
                "@ionic/angular-toolkit": "^4.0.0",
                "@types/jasmine": "~3.8.0",
                "@types/node": "^12.11.1",
                "jasmine-core": "~3.8.0",
                "karma": "~6.3.2",
                "karma-chrome-launcher": "~3.1.0",
                "karma-coverage": "~2.0.3",
                "karma-jasmine": "~4.0.0",
                "karma-jasmine-html-reporter": "~1.7.0",
                "protractor": "~7.0.0",
                "typescript": "~4.3.5"
            }
        }
        
        with open(self.demo_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Criar angular.json básico
        angular_json = {
            "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
            "version": 1,
            "newProjectRoot": "projects",
            "projects": {
                "app": {
                    "projectType": "application",
                    "schematics": {},
                    "root": "",
                    "sourceRoot": "src",
                    "prefix": "app",
                    "architect": {
                        "build": {
                            "builder": "@angular-devkit/build-angular:browser",
                            "options": {
                                "outputPath": "dist/app",
                                "index": "src/index.html",
                                "main": "src/main.ts",
                                "polyfills": "src/polyfills.ts",
                                "tsConfig": "tsconfig.app.json",
                                "assets": [
                                    "src/favicon.ico",
                                    "src/assets"
                                ],
                                "styles": [
                                    "src/global.scss"
                                ],
                                "scripts": []
                            }
                        },
                        "serve": {
                            "builder": "@angular-devkit/build-angular:dev-server",
                            "options": {
                                "browserTarget": "app:build"
                            }
                        }
                    }
                }
            }
        }
        
        with open(self.demo_dir / "angular.json", "w") as f:
            json.dump(angular_json, f, indent=2)
        
        # Criar ionic.config.json
        ionic_config = {
            "name": "demo-ionic-angular-app",
            "integrations": {
                "capacitor": {}
            },
            "type": "angular"
        }
        
        with open(self.demo_dir / "ionic.config.json", "w") as f:
            json.dump(ionic_config, f, indent=2)
        
        # Criar estrutura básica de diretórios
        (self.demo_dir / "src" / "app").mkdir(parents=True, exist_ok=True)
        (self.demo_dir / "src" / "assets").mkdir(parents=True, exist_ok=True)
        
        # Criar app.component.ts básico
        app_component = '''
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {
  constructor() {}
}
'''
        
        with open(self.demo_dir / "src" / "app" / "app.component.ts", "w") as f:
            f.write(app_component)
        
        # Criar app.component.html básico
        app_template = '''
<ion-app>
  <ion-router-outlet></ion-router-outlet>
</ion-app>
'''
        
        with open(self.demo_dir / "src" / "app" / "app.component.html", "w") as f:
            f.write(app_template)
        
        print(f"✅ Projeto demo criado em: {self.demo_dir}")
        print(f"   📦 Angular: 12.2.0")
        print(f"   📦 Ionic: 5.9.0")
        print(f"   📁 Estrutura básica criada")
    
    async def demonstrate_analysis(self):
        """Demonstra a análise do projeto."""
        self.print_step("Análise do Projeto")
        
        try:
            from simple_ionic_angular_upgrade import SimpleAnalyzeAction
            
            analyzer = SimpleAnalyzeAction()
            project_info = await analyzer.run(str(self.demo_dir))
            
            print(f"✅ Análise concluída:")
            print(f"   📁 Caminho: {project_info.path}")
            print(f"   🔄 Angular: {project_info.current_angular} → {project_info.target_angular}")
            print(f"   🔄 Ionic: {project_info.current_ionic} → {project_info.target_ionic}")
            
            return project_info
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            return None
    
    async def demonstrate_backup(self):
        """Demonstra o backup do projeto."""
        self.print_step("Backup do Projeto")
        
        try:
            from simple_ionic_angular_upgrade import SimpleBackupAction
            
            backup_action = SimpleBackupAction()
            backup_path = await backup_action.run(str(self.demo_dir))
            
            print(f"✅ Backup criado:")
            print(f"   📁 Localização: {backup_path}")
            print(f"   💾 Tamanho: {self._get_dir_size(backup_path):.1f} MB")
            
            return backup_path
            
        except Exception as e:
            print(f"❌ Erro no backup: {e}")
            return None
    
    def _get_dir_size(self, path: str) -> float:
        """Calcula tamanho do diretório em MB."""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in Path(path).walk():
                for filename in filenames:
                    filepath = dirpath / filename
                    total_size += filepath.stat().st_size
            return total_size / (1024 * 1024)  # Convert to MB
        except:
            return 0.0
    
    async def demonstrate_upgrade_simulation(self):
        """Simula o processo de upgrade."""
        self.print_step("Simulação de Upgrade")
        
        print("🔄 Simulando processo de upgrade...")
        
        # Simular etapas do upgrade
        steps = [
            ("Verificando pré-requisitos", 1.0),
            ("Atualizando Angular CLI", 2.0),
            ("Atualizando @angular/core", 1.5),
            ("Atualizando @angular/common", 1.0),
            ("Atualizando @angular/forms", 1.0),
            ("Atualizando @angular/router", 1.0),
            ("Atualizando @ionic/angular", 2.0),
            ("Instalando dependências", 3.0),
            ("Verificando build", 2.5)
        ]
        
        changes = []
        start_time = datetime.now()
        
        for step_name, duration in steps:
            print(f"   🔄 {step_name}...")
            await asyncio.sleep(0.5)  # Simular processamento
            print(f"   ✅ {step_name} concluído")
            changes.append(step_name)
        
        total_duration = (datetime.now() - start_time).total_seconds()
        
        # Simular resultado
        result = UpgradeResult(
            success=True,
            duration=total_duration,
            changes=changes,
            errors=[]
        )
        
        print(f"\n✅ Simulação concluída:")
        print(f"   ⏱️  Duração: {result.duration:.1f}s")
        print(f"   📝 Mudanças: {len(result.changes)}")
        print(f"   ❌ Erros: {len(result.errors)}")
        
        return result
    
    async def demonstrate_report(self, project_info, result, backup_path):
        """Demonstra a geração de relatório."""
        self.print_step("Geração de Relatório")
        
        try:
            from simple_ionic_angular_upgrade import SimpleReportAction
            
            report_action = SimpleReportAction()
            report_path = await report_action.run(project_info, result, backup_path)
            
            print(f"✅ Relatório gerado:")
            print(f"   📄 Arquivo: {report_path}")
            print(f"   📊 Formato: Markdown")
            print(f"   📝 Conteúdo: Completo")
            
            # Mostrar preview do relatório
            print(f"\n📋 Preview do relatório:")
            with open(report_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]  # Primeiras 10 linhas
                for line in lines:
                    print(f"   {line.rstrip()}")
                if len(f.readlines()) > 10:
                    print("   ...")
            
            return report_path
            
        except Exception as e:
            print(f"❌ Erro na geração do relatório: {e}")
            return None
    
    async def cleanup_demo(self):
        """Limpa arquivos da demonstração."""
        try:
            import shutil
            if self.demo_dir.exists():
                shutil.rmtree(self.demo_dir)
            
            # Limpar backups
            for backup_dir in Path(".").glob("*_backup_*"):
                if backup_dir.is_dir():
                    shutil.rmtree(backup_dir)
            
            print("🧹 Arquivos de demonstração removidos")
            
        except Exception as e:
            print(f"⚠️  Erro ao limpar demonstração: {e}")
    
    async def run_complete_demo(self):
        """Executa demonstração completa."""
        self.print_header("DEMO SIMPLES - UPGRADE IONIC/ANGULAR")
        print("POC Técnica - Apenas Core Funcional")
        print("Sem QA, sem testes complexos, apenas o essencial")
        
        try:
            # 1. Criar projeto demo
            await self.create_demo_project()
            
            # 2. Demonstrar análise
            project_info = await self.demonstrate_analysis()
            if not project_info:
                print("❌ Falha na análise. Abortando demo.")
                return False
            
            # 3. Demonstrar backup
            backup_path = await self.demonstrate_backup()
            if not backup_path:
                print("❌ Falha no backup. Abortando demo.")
                return False
            
            # 4. Simular upgrade
            result = await self.demonstrate_upgrade_simulation()
            
            # 5. Gerar relatório
            report_path = await self.demonstrate_report(project_info, result, backup_path)
            
            # 6. Resumo final
            self.print_header("DEMO CONCLUÍDA COM SUCESSO")
            print(f"\n✅ Demonstração técnica concluída!")
            print(f"\n📊 Resultados:")
            print(f"   📁 Projeto demo: {self.demo_dir}")
            print(f"   💾 Backup: {backup_path}")
            print(f"   📄 Relatório: {report_path}")
            print(f"   ⏱️  Duração total: {result.duration:.1f}s")
            
            print(f"\n🎯 Funcionalidades demonstradas:")
            print(f"   ✅ Análise automática de projeto")
            print(f"   ✅ Backup seguro antes do upgrade")
            print(f"   ✅ Processo de upgrade simulado")
            print(f"   ✅ Geração de relatório detalhado")
            
            print(f"\n🚀 Para usar em projeto real:")
            print(f"   1. python simple_ionic_angular_upgrade.py")
            print(f"   2. Informar caminho do projeto")
            print(f"   3. Aguardar conclusão")
            print(f"   4. Revisar relatório gerado")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na demonstração: {e}")
            return False
        
        finally:
            # Perguntar sobre limpeza
            print(f"\n🧹 Remover arquivos de demonstração? (s/N): ", end="")
            # Para demo, manter arquivos
            print("Mantendo para análise.")


async def main():
    """Função principal da demonstração."""
    demo = SimpleDemoRunner()
    
    try:
        success = await demo.run_complete_demo()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Demonstração interrompida pelo usuário")
        return 1
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        return 1


if __name__ == "__main__":
    print("🚀 Iniciando Demo Simples do Sistema de Upgrade")
    print("📋 Versão técnica - Apenas funcionalidades core")
    print("⏱️  Tempo estimado: 2-3 minutos")
    print("\nPressione Ctrl+C para interromper.\n")
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Demo encerrada.")
        sys.exit(0)