#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/06/18
@Author  : User
@File    : fallback_llm.py
@Desc    : Implementação de um provedor de LLM com fallback automático para lidar com erros de limite de taxa
"""
from __future__ import annotations

import asyncio
from typing import Optional, Union, List, Dict, Any

from openai import APIConnectionError, RateLimitError, AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from metagpt.configs.llm_config import LLMConfig, LLMType
from metagpt.configs.models_config import ModelsConfig
from metagpt.const import USE_CONFIG_TIMEOUT
from metagpt.logs import logger
from metagpt.provider.openai_api import OpenAILLM
from metagpt.provider.llm_provider_registry import register_provider, create_llm_instance
from metagpt.utils.common import log_and_reraise


class FallbackLLM(OpenAILLM):
    """Provedor de LLM com fallback automático para lidar com erros de limite de taxa
    
    Esta classe estende o OpenAILLM e adiciona a funcionalidade de fallback para outro provedor
    quando ocorre um erro de limite de taxa (RateLimitError).
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.models_config = ModelsConfig.default()
        self.fallback_llm_name = "groq-llama3-70b"  # Nome do modelo de fallback configurado em config2.yaml
        self.fallback_llm: Optional[OpenAILLM] = None
        self._init_fallback_llm()

    def _init_fallback_llm(self):
        """Inicializa o LLM de fallback a partir da configuração"""
        fallback_config = self.models_config.get(self.fallback_llm_name)
        if fallback_config:
            self.fallback_llm = create_llm_instance(fallback_config)
            logger.info(f"Fallback LLM inicializado: {self.fallback_llm_name} ({fallback_config.model})")
        else:
            logger.warning(f"Configuração para o LLM de fallback '{self.fallback_llm_name}' não encontrada")

    async def _achat_completion_with_fallback(self, messages: list[dict], timeout=USE_CONFIG_TIMEOUT) -> ChatCompletion:
        """Executa a chamada de completude do chat com suporte a fallback para outro provedor"""
        try:
            return await super()._achat_completion(messages, timeout=timeout)
        except RateLimitError as e:
            if self.fallback_llm:
                logger.warning(f"RateLimitError no provedor principal ({self.config.api_type}). "  
                              f"Alternando para o provedor de fallback: {self.fallback_llm_name}")
                return await self.fallback_llm._achat_completion(messages, timeout=timeout)
            else:
                logger.error(f"RateLimitError e nenhum provedor de fallback disponível: {e}")
                raise

    async def _achat_completion_stream_with_fallback(self, messages: list[dict], timeout=USE_CONFIG_TIMEOUT) -> str:
        """Executa a chamada de completude do chat em streaming com suporte a fallback para outro provedor"""
        try:
            return await super()._achat_completion_stream(messages, timeout=timeout)
        except RateLimitError as e:
            if self.fallback_llm:
                logger.warning(f"RateLimitError no provedor principal ({self.config.api_type}) durante streaming. "  
                              f"Alternando para o provedor de fallback: {self.fallback_llm_name}")
                return await self.fallback_llm._achat_completion_stream(messages, timeout=timeout)
            else:
                logger.error(f"RateLimitError e nenhum provedor de fallback disponível: {e}")
                raise

    async def _achat_completion(self, messages: list[dict], timeout=USE_CONFIG_TIMEOUT) -> ChatCompletion:
        """Sobrescreve o método _achat_completion para adicionar suporte a fallback"""
        return await self._achat_completion_with_fallback(messages, timeout=timeout)

    async def _achat_completion_stream(self, messages: list[dict], timeout=USE_CONFIG_TIMEOUT) -> str:
        """Sobrescreve o método _achat_completion_stream para adicionar suporte a fallback"""
        return await self._achat_completion_stream_with_fallback(messages, timeout=timeout)

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
        retry=retry_if_exception_type(APIConnectionError),
        retry_error_callback=log_and_reraise,
    )
    async def acompletion_text(self, messages: list[dict], stream=False, timeout=USE_CONFIG_TIMEOUT) -> str:
        """Sobrescreve o método acompletion_text para usar os métodos com fallback"""
        if stream:
            return await self._achat_completion_stream_with_fallback(messages, timeout=timeout)

        rsp = await self._achat_completion_with_fallback(messages, timeout=self.get_timeout(timeout))
        return self.get_choice_text(rsp)