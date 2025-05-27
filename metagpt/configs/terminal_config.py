#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/05/17
@Author  : MetaGPT
@File    : terminal_config.py
"""
from metagpt.utils.yaml_model import YamlModel


class TerminalConfig(YamlModel):
    """Config for Terminal"""

    executable: str = "bash"  # Default to bash if not specified