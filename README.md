# Hokm Telegram Bot

A fully-featured Telegram bot for playing the Persian card game **Hokm** in group chats. The bot supports multi-language (English, Persian), group settings, and persistent game state using a database. It is designed for easy deployment with Docker and Docker Compose.

## Features
- Play the classic Hokm card game in Telegram groups
- Supports English and Persian languages
- Persistent group and game settings using SQLite and SQLAlchemy
- Sticker-based card selection
- Inline queries and interactive buttons for game actions
- Admin commands for group/game management

## Project Structure
```
.
├── Dockerfile              # Container build instructions
├── compose.yml             # Docker Compose configuration
├── main.py                 # Entry point for the bot
├── requirements.txt        # Python dependencies
├── hokm_bot/               # Telegram bot logic, handlers, database, localization
│   ├── handlers/           # Telegram command and callback handlers
│   ├── database/           # SQLAlchemy models, functions, and SQLite DB
│   ├── locales/            # Localization YAML files (en/fa)
│   └── ...
├── hokm_game/              # Core game logic (cards, players, game state)
├── stickers.json           # Card sticker mappings
├── stickers_unique.json    # Unique sticker IDs for game logic
└── ...
```

## Getting Started
### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- A Telegram bot token ([@BotFather](https://t.me/BotFather))

### Quick Start
1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd hokm
   ```

2. **Configure Environment**
   - Copy or edit `hokm_bot/.env`:
     ```env
     BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
     BOT_ID=YOUR_BOT_ID
     ```
   - Replace with your actual bot token and bot ID.

3. **Start with Docker Compose**
   ```sh
   docker-compose -f compose.yml up --build
   ```
   The bot will start and connect to Telegram. Use `/start` in your group to interact.

### Manual (Local) Run
If you prefer running without Docker:
```sh
pip install -r requirements.txt
python main.py
```

## Usage
- Add the bot to your Telegram group and grant admin rights for full functionality.
- Use `/start` to begin, `/newgame` to create a new game, and follow the inline buttons and commands for gameplay.
- Use `/help` for a list of commands and instructions.

## Customization
- **Languages:** Add or edit YAML files in `hokm_bot/locales/`.
- **Stickers:** Update `stickers.json` and `stickers_unique.json` for custom card stickers.

## Data Persistence
- Game and group settings are stored in `hokm_bot/database/groups.db` (SQLite).
- The database is persisted via a Docker volume (`groups_db_data`).

## License
This project is licensed under the terms of the LICENSE file included.

---

*Enjoy playing Hokm with your friends on Telegram!*
