import os

import toml
import uvicorn

from app import create_app

app = create_app()

if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(path, "./backend")
    app_config = toml.load(fr"{base_path}/app_config.toml")
    active = app_config.get('settings', {}).get('active', 'development')
    config_name = f'app_{active}_config.toml'
    config = toml.load(fr"{base_path}/config/{config_name}")
    port = config.get('fastapi', {}).get('port', 8302)
    uvicorn.run(app, host="0.0.0.0", port=port, log_config=None)
