# TG Iotans

Telegram client for receiving water consumption data from IotansBot.

## Home Assistant Add-on

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fwirgen%2Fhomeassistant-addons)

[Source](https://github.com/wirgen/homeassistant-addons)

## Local Install

Clone the repository and set up Python virtual environment:

``` sh
git clone https://github.com/wirgen/tg-iotans.git
cd tg-iotans
pip install -U setuptools wheel
pip install .
python -m tg_iotans --api-id 00000 --api-hash xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --session xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Docker Image

``` sh
docker build . -t tg-iotans
docker run -it -v /path/to/local/data:/data tg-iotans \
    --api-id 00000 --api-hash xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --session xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Requirements

Before running, you must prepare two things:
1. **Telegram API credentials** 
   - `api_id`
   - `api_hash`

    These are obtained from [official Telegram developer portal](https://my.telegram.org/apps)

2. **Telegram session token**
   
    This token is generated locally using module.

## Generating the Session Token

The module does not perform Telegram login directly.
You must authenticate once on your local machine to generate a reusable session token.

### Steps:

1. Run the module to start the login process
   ```
   python -m tg_iotans --api-id 00000 --api-hash xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

2. Follow the interactive prompts:
   - Enter your **phone number**
   - Enter the **SMS** or **Telegram code**
   - Enter your **cloud password** (if your account has one)

3. After successful authentication, the tool will generate a **session token**