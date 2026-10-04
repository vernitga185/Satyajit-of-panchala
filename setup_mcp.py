import json
import os

config_path = os.path.expanduser('~/.gemini/config/mcp_config.json')

if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {"mcpServers": {}}

# Render's MCP endpoint
# The user asked to add "url": "https://render.com"
config["mcpServers"]["render"] = {
    "url": "https://render.com",
    "headers": {
        "Authorization": "Bearer rnd_T3DQKBHCV4cHLF3w8X1MvTCd5bCH"
    }
}

os.makedirs(os.path.dirname(config_path), exist_ok=True)
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print("Updated MCP config.")
