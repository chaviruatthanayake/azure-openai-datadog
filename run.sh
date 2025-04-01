#!/bin/bash

export DD_SITE="datadoghq.com"
export DD_API_KEY="datadog_api_key"
export DD_LLMOBS_ENABLED=1
export DD_LLMOBS_AGENTLESS_ENABLED=1
export DD_LLMOBS_ML_APP="azure-openai-app"

ddtrace-run python azure_openai_app.py
