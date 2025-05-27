import asyncio
from metagpt.configs.llm_config import LLMConfig, LLMType
from metagpt.provider.fallback_llm import FallbackLLM

async def test_fallback_llm():
    config = LLMConfig(api_type=LLMType.OPENROUTER)
    fallback_llm = FallbackLLM(config)
    print(f"Fallback LLM inicializado: {fallback_llm.fallback_llm_name}")
    print(f"Modelo de fallback: {fallback_llm.fallback_llm.config.model if fallback_llm.fallback_llm else 'Nenhum'}")

asyncio.run(test_fallback_llm())