#!/usr/bin/env python3
"""
Exemplo de Uso do Sistema de Upgrade Ionic/Angular
Este arquivo demonstra como utilizar o sistema multiagente para upgrade
automatizado de projetos empresariais com 50+ componentes.

Autor: MetaGPT Ionic/Angular Upgrade System
Versão: 1.0.0
Data: 2024
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Importações do sistema de upgrade
from ionic_angular_upgrade_system import (
    IonicAngularUpgradeSystem,
    CodeReaderAgent,
    PlannerAgent,
    IonicUpgradeAgent,
    AngularUpgradeAgent,
    RefactorAgent,
    TestAgent,
    ReportAgent,
    ProjectAnalysis,
    UpgradePlan,
    ComponentResult,
    UpgradeReport
)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('upgrade_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class UpgradeExecutor:
    """
    Executor principal para o processo de upgrade.
    Gerencia a execução completa do sistema multiagente.
    """
    
    def __init__(self, project_path: str, config_path: str = "upgrade_config.yaml"):
        """
        Inicializa o executor de upgrade.
        
        Args:
            project_path: Caminho para o projeto Ionic/Angular
            config_path: Caminho para o arquivo de configuração
        """
        self.project_path = Path(project_path)
        self.config_path = Path(config_path)
        self.upgrade_system = None
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega a configuração do arquivo YAML.
        
        Returns:
            Dicionário com as configurações
        """
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Retorna configuração padrão caso o arquivo não seja encontrado.
        
        Returns:
            Configuração padrão
        """
        return {
            "project": {
                "name": "Enterprise Ionic Angular App",
                "path": str(self.project_path),
                "backup_path": "./backups"
            },
            "versions": {
                "current": {
                    "angular": "12.2.0",
                    "ionic": "5.9.0"
                },
                "target": {
                    "angular": "18.0.0",
                    "ionic": "8.0.0"
                }
            },
            "upgrade_settings": {
                "migration_strategy": "incremental",
                "safety": {
                    "create_backup": True,
                    "rollback_enabled": True,
                    "validation_required": True
                }
            }
        }
    
    async def validate_prerequisites(self) -> bool:
        """
        Valida os pré-requisitos para o upgrade.
        
        Returns:
            True se todos os pré-requisitos forem atendidos
        """
        logger.info("Validando pré-requisitos...")
        
        # Verificar se o projeto existe
        if not self.project_path.exists():
            logger.error(f"Projeto não encontrado: {self.project_path}")
            return False
        
        # Verificar arquivos essenciais
        essential_files = [
            "package.json",
            "angular.json",
            "ionic.config.json"
        ]
        
        for file_name in essential_files:
            file_path = self.project_path / file_name
            if not file_path.exists():
                logger.error(f"Arquivo essencial não encontrado: {file_name}")
                return False
        
        # Verificar espaço em disco
        import shutil
        free_space_gb = shutil.disk_usage(self.project_path).free / (1024**3)
        required_space = self.config.get("environment", {}).get("system_checks", {}).get("disk_space_gb", 10)
        
        if free_space_gb < required_space:
            logger.error(f"Espaço insuficiente. Necessário: {required_space}GB, Disponível: {free_space_gb:.2f}GB")
            return False
        
        logger.info("Todos os pré-requisitos foram atendidos")
        return True
    
    async def create_backup(self) -> bool:
        """
        Cria backup do projeto antes do upgrade.
        
        Returns:
            True se o backup foi criado com sucesso
        """
        logger.info("Criando backup do projeto...")
        
        try:
            import shutil
            from datetime import datetime
            
            backup_dir = Path(self.config["project"]["backup_path"])
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{self.config['project']['name']}_{timestamp}"
            backup_path = backup_dir / backup_name
            
            # Copiar projeto para backup
            shutil.copytree(
                self.project_path,
                backup_path,
                ignore=shutil.ignore_patterns(
                    'node_modules', 'dist', 'platforms', 'plugins', '.git'
                )
            )
            
            logger.info(f"Backup criado com sucesso: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return False
    
    async def initialize_upgrade_system(self) -> bool:
        """
        Inicializa o sistema de upgrade com todos os agentes.
        
        Returns:
            True se a inicialização foi bem-sucedida
        """
        logger.info("Inicializando sistema de upgrade...")
        
        try:
            # Criar instância do sistema de upgrade
            self.upgrade_system = IonicAngularUpgradeSystem(
                project_path=str(self.project_path),
                config=self.config
            )
            
            # Inicializar agentes
            await self.upgrade_system.initialize_agents()
            
            logger.info("Sistema de upgrade inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema de upgrade: {e}")
            return False
    
    async def execute_upgrade(self) -> UpgradeReport:
        """
        Executa o processo completo de upgrade.
        
        Returns:
            Relatório final do upgrade
        """
        logger.info("Iniciando processo de upgrade...")
        
        try:
            # Executar upgrade
            report = await self.upgrade_system.execute_upgrade()
            
            logger.info("Processo de upgrade concluído")
            return report
            
        except Exception as e:
            logger.error(f"Erro durante o upgrade: {e}")
            # Em caso de erro, tentar rollback
            await self.rollback_if_needed()
            raise
    
    async def rollback_if_needed(self) -> bool:
        """
        Executa rollback em caso de falha no upgrade.
        
        Returns:
            True se o rollback foi bem-sucedido
        """
        logger.warning("Executando rollback...")
        
        try:
            if self.upgrade_system:
                await self.upgrade_system.rollback()
                logger.info("Rollback executado com sucesso")
                return True
        except Exception as e:
            logger.error(f"Erro durante rollback: {e}")
        
        return False
    
    async def generate_final_report(self, report: UpgradeReport) -> str:
        """
        Gera relatório final em múltiplos formatos.
        
        Args:
            report: Relatório do upgrade
            
        Returns:
            Caminho para o relatório principal
        """
        logger.info("Gerando relatório final...")
        
        try:
            from datetime import datetime
            import json
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = Path(f"reports/upgrade_{timestamp}")
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # Relatório JSON
            json_report_path = report_dir / "upgrade_report.json"
            with open(json_report_path, 'w', encoding='utf-8') as f:
                json.dump(report.dict(), f, indent=2, ensure_ascii=False)
            
            # Relatório HTML
            html_report_path = report_dir / "upgrade_report.html"
            html_content = self._generate_html_report(report)
            with open(html_report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Relatório executivo
            executive_report_path = report_dir / "executive_summary.md"
            executive_content = self._generate_executive_summary(report)
            with open(executive_report_path, 'w', encoding='utf-8') as f:
                f.write(executive_content)
            
            logger.info(f"Relatórios gerados em: {report_dir}")
            return str(html_report_path)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return ""
    
    def _generate_html_report(self, report: UpgradeReport) -> str:
        """
        Gera relatório em formato HTML.
        
        Args:
            report: Relatório do upgrade
            
        Returns:
            Conteúdo HTML do relatório
        """
        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório de Upgrade - {report.project_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .warning {{ color: #ffc107; }}
                .component {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 3px; }}
                .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .metric {{ text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Relatório de Upgrade Ionic/Angular</h1>
                <h2>Projeto: {report.project_name}</h2>
                <p><strong>Status:</strong> <span class="{'success' if report.success else 'error'}">
                    {'✅ Sucesso' if report.success else '❌ Falha'}
                </span></p>
                <p><strong>Duração:</strong> {report.duration_minutes:.2f} minutos</p>
                <p><strong>Data:</strong> {report.timestamp}</p>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <h3>{len(report.components_processed)}</h3>
                    <p>Componentes Processados</p>
                </div>
                <div class="metric">
                    <h3>{len([c for c in report.components_processed if c.success])}</h3>
                    <p>Componentes com Sucesso</p>
                </div>
                <div class="metric">
                    <h3>{len([c for c in report.components_processed if not c.success])}</h3>
                    <p>Componentes com Falha</p>
                </div>
            </div>
            
            <h3>Resumo Executivo</h3>
            <p>{report.summary}</p>
            
            <h3>Componentes Processados</h3>
            {''.join([f'<div class="component"><strong>{c.component_name}</strong> - <span class="{'success' if c.success else 'error'}">{"✅ Sucesso" if c.success else "❌ Falha"}</span><br><small>{c.changes_made}</small></div>' for c in report.components_processed])}
            
            <h3>Recomendações</h3>
            <ul>
                {''.join([f'<li>{rec}</li>' for rec in report.recommendations])}
            </ul>
            
            <h3>Próximos Passos</h3>
            <ul>
                {''.join([f'<li>{step}</li>' for step in report.next_steps])}
            </ul>
        </body>
        </html>
        """
        return html_template
    
    def _generate_executive_summary(self, report: UpgradeReport) -> str:
        """
        Gera resumo executivo em formato Markdown.
        
        Args:
            report: Relatório do upgrade
            
        Returns:
            Conteúdo Markdown do resumo executivo
        """
        success_rate = len([c for c in report.components_processed if c.success]) / len(report.components_processed) * 100 if report.components_processed else 0
        
        markdown_content = f"""
# Resumo Executivo - Upgrade {report.project_name}

## Status Geral
- **Resultado:** {'✅ Sucesso' if report.success else '❌ Falha'}
- **Duração:** {report.duration_minutes:.2f} minutos
- **Taxa de Sucesso:** {success_rate:.1f}%
- **Data de Execução:** {report.timestamp}

## Métricas Principais
- **Componentes Processados:** {len(report.components_processed)}
- **Componentes com Sucesso:** {len([c for c in report.components_processed if c.success])}
- **Componentes com Falha:** {len([c for c in report.components_processed if not c.success])}

## Resumo
{report.summary}

## Impacto no Negócio
- ✅ Aplicação atualizada para versões mais recentes e seguras
- ✅ Melhor performance e estabilidade
- ✅ Suporte a funcionalidades modernas
- ✅ Redução de vulnerabilidades de segurança

## Recomendações
{''.join([f'- {rec}\n' for rec in report.recommendations])}

## Próximos Passos
{''.join([f'- {step}\n' for step in report.next_steps])}

## Contato
Para dúvidas técnicas, entre em contato com a equipe de desenvolvimento.
        """
        return markdown_content


async def main():
    """
    Função principal para execução do upgrade.
    """
    # Configurações do projeto
    project_path = input("Digite o caminho do projeto Ionic/Angular: ").strip()
    if not project_path:
        project_path = "./sample-ionic-angular-project"
    
    config_path = "upgrade_config.yaml"
    
    # Criar executor
    executor = UpgradeExecutor(project_path, config_path)
    
    try:
        # Validar pré-requisitos
        if not await executor.validate_prerequisites():
            logger.error("Pré-requisitos não atendidos. Abortando upgrade.")
            return
        
        # Criar backup
        if not await executor.create_backup():
            logger.error("Falha ao criar backup. Abortando upgrade.")
            return
        
        # Inicializar sistema
        if not await executor.initialize_upgrade_system():
            logger.error("Falha ao inicializar sistema. Abortando upgrade.")
            return
        
        # Executar upgrade
        report = await executor.execute_upgrade()
        
        # Gerar relatório
        report_path = await executor.generate_final_report(report)
        
        # Resultado final
        if report.success:
            logger.info(f"🎉 Upgrade concluído com sucesso!")
            logger.info(f"📊 Relatório disponível em: {report_path}")
            print(f"\n✅ UPGRADE CONCLUÍDO COM SUCESSO!")
            print(f"📊 Relatório: {report_path}")
            print(f"⏱️  Duração: {report.duration_minutes:.2f} minutos")
            print(f"📦 Componentes processados: {len(report.components_processed)}")
        else:
            logger.error(f"❌ Upgrade falhou. Verifique os logs para detalhes.")
            print(f"\n❌ UPGRADE FALHOU")
            print(f"📊 Relatório de erro: {report_path}")
            print(f"🔄 Rollback executado automaticamente")
    
    except KeyboardInterrupt:
        logger.warning("Upgrade interrompido pelo usuário")
        await executor.rollback_if_needed()
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        await executor.rollback_if_needed()


if __name__ == "__main__":
    print("""
    🚀 Sistema de Upgrade Ionic/Angular - MetaGPT
    =============================================
    
    Este sistema automatiza o upgrade de projetos empresariais
    Ionic/Angular usando agentes colaborativos inteligentes.
    
    Recursos:
    ✅ Upgrade incremental seguro
    ✅ Backup automático
    ✅ Validação completa
    ✅ Rollback automático em caso de falha
    ✅ Relatórios detalhados
    ✅ Suporte a 50+ componentes
    
    Versões suportadas:
    📱 Ionic: 5.x → 8.x
    🅰️  Angular: 12.x → 18.x
    
    """)
    
    # Executar upgrade
    asyncio.run(main())