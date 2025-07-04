#!/usr/bin/env python3
"""
POC Simples - Sistema de Upgrade Ionic/Angular

Versão simplificada focada apenas na parte técnica do upgrade.
Sem QA, sem testes complexos, apenas o core funcional.

Autor: Sistema MetaGPT
Versão: 1.0.0-simple
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Importações do MetaGPT
try:
    from metagpt.actions import Action
    from metagpt.roles import Role
    from metagpt.schema import Message
    from metagpt.team import Team
    from metagpt.logs import logger
except ImportError:
    print("⚠️  MetaGPT não encontrado. Executando em modo standalone.")
    
    # Classes mock para execução standalone
    class Action:
        def __init__(self, name: str = ""):
            self.name = name
        
        async def run(self, *args, **kwargs):
            pass
    
    class Role:
        def __init__(self, name: str = "", profile: str = ""):
            self.name = name
            self.profile = profile
            self.actions = []
        
        def set_actions(self, actions: List[Action]):
            self.actions = actions
        
        async def run(self, *args, **kwargs):
            pass
    
    class Message:
        def __init__(self, content: str = ""):
            self.content = content
    
    class Team:
        def __init__(self, *args, **kwargs):
            pass
        
        async def run(self, *args, **kwargs):
            pass
    
    class logger:
        @staticmethod
        def info(msg): print(f"ℹ️  {msg}")
        @staticmethod
        def error(msg): print(f"❌ {msg}")
        @staticmethod
        def warning(msg): print(f"⚠️  {msg}")


@dataclass
class ProjectInfo:
    """Informações básicas do projeto."""
    path: str
    current_angular: str
    current_ionic: str
    target_angular: str = "17.0.0"
    target_ionic: str = "7.0.0"


@dataclass
class UpgradeResult:
    """Resultado do upgrade."""
    success: bool
    duration: float
    changes: List[str]
    errors: List[str]
    backup_path: Optional[str] = None


class SimpleAnalyzeAction(Action):
    """Ação simples para analisar o projeto."""
    
    def __init__(self):
        super().__init__(name="SimpleAnalyze")
    
    async def run(self, project_path: str) -> ProjectInfo:
        """Analisa o projeto e retorna informações básicas."""
        logger.info(f"Analisando projeto em: {project_path}")
        
        package_json_path = Path(project_path) / "package.json"
        
        if not package_json_path.exists():
            raise FileNotFoundError(f"package.json não encontrado em {project_path}")
        
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        dependencies = package_data.get('dependencies', {})
        
        # Detectar versões atuais
        angular_version = self._extract_version(dependencies.get('@angular/core', '0.0.0'))
        ionic_version = self._extract_version(dependencies.get('@ionic/angular', '0.0.0'))
        
        project_info = ProjectInfo(
            path=project_path,
            current_angular=angular_version,
            current_ionic=ionic_version
        )
        
        logger.info(f"Projeto analisado: Angular {angular_version}, Ionic {ionic_version}")
        return project_info
    
    def _extract_version(self, version_string: str) -> str:
        """Extrai versão limpa da string."""
        return version_string.replace('^', '').replace('~', '').replace('>=', '')


class SimpleBackupAction(Action):
    """Ação simples para backup do projeto."""
    
    def __init__(self):
        super().__init__(name="SimpleBackup")
    
    async def run(self, project_path: str) -> str:
        """Cria backup do projeto."""
        logger.info("Criando backup do projeto...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{project_path}_backup_{timestamp}"
        
        try:
            # Usar robocopy no Windows ou cp no Linux/Mac
            if os.name == 'nt':  # Windows
                cmd = ['robocopy', project_path, backup_path, '/E', '/XD', 'node_modules', '.git']
                result = subprocess.run(cmd, capture_output=True, text=True)
                # robocopy retorna códigos diferentes, 0-7 são sucessos
                if result.returncode > 7:
                    raise subprocess.CalledProcessError(result.returncode, cmd)
            else:  # Linux/Mac
                cmd = ['cp', '-r', project_path, backup_path]
                subprocess.run(cmd, check=True)
            
            logger.info(f"Backup criado em: {backup_path}")
            return backup_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao criar backup: {e}")
            raise


class SimpleUpgradeAction(Action):
    """Ação simples para executar o upgrade."""
    
    def __init__(self):
        super().__init__(name="SimpleUpgrade")
    
    async def run(self, project_info: ProjectInfo) -> UpgradeResult:
        """Executa o upgrade do projeto."""
        start_time = datetime.now()
        changes = []
        errors = []
        
        try:
            logger.info("Iniciando upgrade do projeto...")
            
            # Mudar para o diretório do projeto
            original_cwd = os.getcwd()
            os.chdir(project_info.path)
            
            # 1. Atualizar Angular CLI globalmente
            logger.info("Atualizando Angular CLI...")
            await self._run_command(['npm', 'install', '-g', '@angular/cli@latest'])
            changes.append("Angular CLI atualizado")
            
            # 2. Atualizar dependências Angular
            logger.info("Atualizando dependências Angular...")
            angular_packages = [
                '@angular/core',
                '@angular/common',
                '@angular/forms',
                '@angular/router',
                '@angular/platform-browser',
                '@angular/platform-browser-dynamic'
            ]
            
            for package in angular_packages:
                try:
                    await self._run_command(['ng', 'update', package, '--force'])
                    changes.append(f"Atualizado {package}")
                except Exception as e:
                    errors.append(f"Erro ao atualizar {package}: {str(e)}")
            
            # 3. Atualizar Ionic
            logger.info("Atualizando Ionic...")
            try:
                await self._run_command(['npm', 'install', f'@ionic/angular@{project_info.target_ionic}'])
                changes.append(f"Ionic atualizado para {project_info.target_ionic}")
            except Exception as e:
                errors.append(f"Erro ao atualizar Ionic: {str(e)}")
            
            # 4. Instalar dependências
            logger.info("Instalando dependências...")
            await self._run_command(['npm', 'install'])
            changes.append("Dependências instaladas")
            
            # 5. Executar build para verificar
            logger.info("Verificando build...")
            try:
                await self._run_command(['ng', 'build', '--configuration=production'])
                changes.append("Build verificado com sucesso")
            except Exception as e:
                errors.append(f"Erro no build: {str(e)}")
            
            # Voltar ao diretório original
            os.chdir(original_cwd)
            
            duration = (datetime.now() - start_time).total_seconds()
            success = len(errors) == 0
            
            logger.info(f"Upgrade concluído em {duration:.1f}s")
            
            return UpgradeResult(
                success=success,
                duration=duration,
                changes=changes,
                errors=errors
            )
            
        except Exception as e:
            os.chdir(original_cwd)
            logger.error(f"Erro durante upgrade: {e}")
            duration = (datetime.now() - start_time).total_seconds()
            
            return UpgradeResult(
                success=False,
                duration=duration,
                changes=changes,
                errors=errors + [str(e)]
            )
    
    async def _run_command(self, cmd: List[str]):
        """Executa comando de forma assíncrona."""
        logger.info(f"Executando: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Comando falhou"
            raise subprocess.CalledProcessError(process.returncode, cmd, error_msg)
        
        return stdout.decode()


class SimpleReportAction(Action):
    """Ação simples para gerar relatório."""
    
    def __init__(self):
        super().__init__(name="SimpleReport")
    
    async def run(self, project_info: ProjectInfo, result: UpgradeResult, backup_path: str) -> str:
        """Gera relatório simples do upgrade."""
        logger.info("Gerando relatório...")
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Preparar textos para o relatório
        changes_text = "\n".join(f"- {change}" for change in result.changes) if result.changes else "Nenhuma mudança registrada."
        errors_text = "Nenhum erro encontrado." if not result.errors else "\n".join(f"- {error}" for error in result.errors)
        
        report = f"""
# Relatório de Upgrade Ionic/Angular

**Data:** {timestamp}
**Status:** {'✅ Sucesso' if result.success else '❌ Falha'}
**Duração:** {result.duration:.1f} segundos

## Projeto
- **Caminho:** {project_info.path}
- **Angular:** {project_info.current_angular} → {project_info.target_angular}
- **Ionic:** {project_info.current_ionic} → {project_info.target_ionic}
- **Backup:** {backup_path}

## Mudanças Realizadas
{changes_text}

## Erros Encontrados
{errors_text}

## Próximos Passos
- Testar a aplicação manualmente
- Verificar funcionalidades críticas
- Fazer deploy em ambiente de teste

---
*Relatório gerado automaticamente*
"""
        
        # Salvar relatório
        report_path = Path(project_info.path) / f"upgrade_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Relatório salvo em: {report_path}")
        return str(report_path)


class SimpleUpgradeAgent(Role):
    """Agente simples para upgrade Ionic/Angular."""
    
    def __init__(self):
        super().__init__(
            name="SimpleUpgradeAgent",
            profile="Agente especializado em upgrade Ionic/Angular"
        )
        
        self.set_actions([
            SimpleAnalyzeAction(),
            SimpleBackupAction(),
            SimpleUpgradeAction(),
            SimpleReportAction()
        ])
    
    async def run(self, project_path: str) -> Dict:
        """Executa o processo completo de upgrade."""
        logger.info("🚀 Iniciando processo de upgrade...")
        
        try:
            # 1. Analisar projeto
            analyze_action = SimpleAnalyzeAction()
            project_info = await analyze_action.run(project_path)
            
            # 2. Criar backup
            backup_action = SimpleBackupAction()
            backup_path = await backup_action.run(project_path)
            
            # 3. Executar upgrade
            upgrade_action = SimpleUpgradeAction()
            result = await upgrade_action.run(project_info)
            result.backup_path = backup_path
            
            # 4. Gerar relatório
            report_action = SimpleReportAction()
            report_path = await report_action.run(project_info, result, backup_path)
            
            logger.info("✅ Processo de upgrade concluído!")
            
            return {
                'success': result.success,
                'project_info': project_info,
                'result': result,
                'report_path': report_path,
                'backup_path': backup_path
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no processo de upgrade: {e}")
            return {
                'success': False,
                'error': str(e)
            }


class SimpleUpgradeSystem:
    """Sistema simples de upgrade Ionic/Angular."""
    
    def __init__(self):
        self.agent = SimpleUpgradeAgent()
    
    async def upgrade_project(self, project_path: str) -> Dict:
        """Executa upgrade de um projeto."""
        if not Path(project_path).exists():
            raise FileNotFoundError(f"Projeto não encontrado: {project_path}")
        
        return await self.agent.run(project_path)
    
    def print_summary(self, result: Dict):
        """Imprime resumo do resultado."""
        print("\n" + "="*60)
        print("📊 RESUMO DO UPGRADE")
        print("="*60)
        
        if result['success']:
            project_info = result['project_info']
            upgrade_result = result['result']
            
            print(f"✅ Status: Sucesso")
            print(f"📁 Projeto: {project_info.path}")
            print(f"🔄 Angular: {project_info.current_angular} → {project_info.target_angular}")
            print(f"🔄 Ionic: {project_info.current_ionic} → {project_info.target_ionic}")
            print(f"⏱️  Duração: {upgrade_result.duration:.1f}s")
            print(f"📝 Mudanças: {len(upgrade_result.changes)}")
            print(f"❌ Erros: {len(upgrade_result.errors)}")
            print(f"💾 Backup: {upgrade_result.backup_path}")
            print(f"📄 Relatório: {result['report_path']}")
            
            if upgrade_result.errors:
                print("\n⚠️  Erros encontrados:")
                for error in upgrade_result.errors:
                    print(f"   - {error}")
        else:
            print(f"❌ Status: Falha")
            print(f"🐛 Erro: {result.get('error', 'Erro desconhecido')}")
        
        print("="*60)


async def main():
    """Função principal para demonstração."""
    print("🚀 POC Simples - Sistema de Upgrade Ionic/Angular")
    print("📋 Versão técnica focada apenas no core funcional")
    print()
    
    # Exemplo de uso
    project_path = input("Digite o caminho do projeto (ou Enter para demo): ").strip()
    
    if not project_path:
        print("\n📁 Criando projeto demo...")
        # Criar projeto demo simples
        demo_path = Path("./demo_simple_project")
        demo_path.mkdir(exist_ok=True)
        
        # Criar package.json demo
        package_json = {
            "name": "demo-ionic-angular",
            "version": "1.0.0",
            "dependencies": {
                "@angular/core": "^12.0.0",
                "@ionic/angular": "^5.0.0"
            }
        }
        
        with open(demo_path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        project_path = str(demo_path)
        print(f"✅ Projeto demo criado em: {project_path}")
    
    # Executar upgrade
    system = SimpleUpgradeSystem()
    
    try:
        result = await system.upgrade_project(project_path)
        system.print_summary(result)
        
        if result['success']:
            print("\n🎉 Upgrade concluído com sucesso!")
            print("\n📋 Próximos passos:")
            print("   1. Revisar o relatório gerado")
            print("   2. Testar a aplicação")
            print("   3. Fazer commit das mudanças")
        else:
            print("\n❌ Upgrade falhou. Verifique os erros acima.")
            print("\n🔄 Para reverter:")
            print(f"   1. Restaurar backup: {result.get('backup_path', 'N/A')}")
            print("   2. Verificar dependências")
            print("   3. Tentar novamente")
    
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Processo interrompido pelo usuário")
        exit(1)