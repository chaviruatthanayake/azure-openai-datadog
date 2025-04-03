send_log_to_datadog("Azure OpenAI full interaction log", {
    "start_time": start_time,
    "end_time": end_time,
    "latency": latency,
    "input_length": len(input_text),
    "output_length": len(output_text),
    "input_text": input_text,
    "output_text": output_text,
    "tokens_used": total_tokens,
    "prompt_tokens": prompt_tokens,
    "completion_tokens": completion_tokens,
    "temperature": 0.7,
    "top_p": 0.95,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "stream": False,
    "finish_reason": finish_reason,
    "api_version": "2024-05-01-preview",
})

print(output_text)