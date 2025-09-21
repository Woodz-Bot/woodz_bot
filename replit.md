# Woodz Bot

## Overview

Woodz Bot is a Discord trading card game bot built with Python and discord.py. The bot features an economy system where users can collect leaves (currency), logs, and trading cards through various activities like daily bonuses, work commands, card drops, and fishing. The bot implements cooldown mechanisms to balance gameplay and includes administrative features for card management.

**Current Status**: Bot is successfully running with fully functional game commands including daily rewards, card dropping, and work system. All core gameplay mechanics are implemented and working.

## Recent Changes (September 18, 2025)

- **Project Setup**: Extracted and configured bot files from uploaded codebase
- **Dependencies**: Updated pyproject.toml with discord.py dependency and installed required packages
- **Token Configuration**: Set up secure token handling using environment variables (DISCORD_BOT_TOKEN)
- **Slash Commands**: Updated bot to use modern discord.py app_commands system instead of deprecated slash_command library
- **Workflow**: Created and started Discord Bot workflow - bot is now running successfully
- **Intent Configuration**: Removed privileged intents to avoid permission issues, bot works with default intents
- **User Data System**: Added comprehensive user data management with JSON persistence
- **Daily Command Functionality**: Implemented full daily reward system with 24-hour cooldowns
- **Economy System**: Added leaves and logs currency with proper reward distribution
- **Boost System**: Implemented 1-hour drop boost activation and management
- **Card System**: Added high-rarity card rewards (3-4 star) to user inventories
- **Drop Command**: Implemented weighted card dropping system with boost-aware cooldowns
- **Work Command**: Added random leaf earning system with proper cooldown management
- **Card Management**: Created admin-only card addition system with validation

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py Library**: Uses the modern discord.py library (v2.6.3) with app_commands for slash command functionality
- **Command System**: Implements Discord's application commands (slash commands) using bot.tree.command decorators
- **Event-Driven Architecture**: Uses Discord's event system for bot lifecycle management and automatic command synchronization
- **Modern Implementation**: Updated from deprecated discord.commands to current discord.app_commands

### Data Storage
- **JSON File Storage**: Simple file-based storage using JSON files for user data and card collections
- **Local Data Directory**: Organized data structure with separate files for users (`users.json`) and cards (`cards.json`)
- **No Database Dependencies**: Lightweight approach suitable for smaller Discord communities
- **Current State**: Data files exist but are empty, ready for implementation

### Economy System (Planned)
- **Multi-Currency Design**: 
  - Leaves (primary currency)
  - Logs (secondary resource)
  - Trading cards (collectibles)
- **Activity-Based Rewards**: Users earn resources through various commands (daily, work)
- **Cooldown Management**: Built-in cooldown system prevents spam and maintains game balance

### Command Structure
- **Daily System**: `/daily` - Provides daily bonuses including 2000 leaves, 30 logs, boost activation, and high-rarity cards
- **Work Command**: `/work` - Earn 100-300 leaves with 5-minute cooldown between uses
- **Card Dropping**: `/drop` - Weighted card drops (60% 1🌕, 25% 2🌕, 10% 3🌕, 5% 4🌕) with boost-aware cooldowns
- **Administrative Tools**: `/card_add` - Admin-only card addition with validation and permission enforcement

### Configuration Management
- **Environment Variables**: Secure token management using `DISCORD_BOT_TOKEN` environment variable
- **Centralized Config**: All bot settings, cooldowns, and constants managed in `config.py`
- **Role-Based Permissions**: Admin role system configuration ready (needs implementation)

## External Dependencies

### Core Dependencies
- **discord.py (v2.6.3)**: Primary library for Discord bot functionality and API interaction
- **Python Standard Library**: Uses built-in modules like `os` for environment variable management

### Discord Integration
- **Discord Developer Portal**: Configured with bot token from Discord's developer platform
- **Discord Permissions**: Uses default intents to avoid privileged intent requirements
- **Guild Integration**: Bot commands automatically sync with Discord's application command system

### Development Environment
- **Environment Variables**: Uses `DISCORD_BOT_TOKEN` environment variable for secure authentication
- **File System Access**: Requires read/write permissions for local JSON data storage
- **Workflow**: Discord Bot workflow configured to run `python main.py` with console output