# Telegram Bot Setup

Step-by-step guide to creating a Telegram bot for MOPS.

## What You Need

- A Telegram account (personal phone number required for signup)
- The Telegram app on your phone or desktop

## Step 1: Open BotFather

BotFather is Telegram's official bot for creating and managing bots.

1. Open Telegram
2. In the search bar, type `@BotFather`
3. Select the verified account — it has a blue checkmark next to the name
4. Tap **Start** (or send `/start`) to begin

## Step 2: Create Your Bot

1. Send the command:
   ```
   /newbot
   ```

2. BotFather asks: **"Alright, a new bot. How are we going to call it?"**

   Type a display name for your bot. This is what users see in chat. Example:
   ```
   My MOPS Agent
   ```

3. BotFather asks: **"Good. Now let's choose a username for your bot."**

   The username must:
   - End in `bot` (e.g., `my_mops_agent_bot`)
   - Be unique across all of Telegram
   - Only contain letters, numbers, and underscores

   Example:
   ```
   my_mops_agent_bot
   ```

4. BotFather responds with your **bot token**:

   ```
   Done! Congratulations on your new bot. You will find it at t.me/my_mops_agent_bot.

   Use this token to access the HTTP API:
   7123456789:AAHBx3mK9zLEx_fG7Q2nwY8kJzR4p5sW1vM

   Keep your token secure and store it safely, it can be used by
   anyone to control your bot.
   ```

   **Copy this token** — you'll need it during MOPS onboarding. It looks like:
   ```
   7123456789:AAHBx3mK9zLEx_fG7Q2nwY8kJzR4p5sW1vM
   ```

> **Security note:** Your bot token is like a password. Anyone with this token can control your bot. Never share it publicly or commit it to version control.

## Step 3: Get Your User ID

MOPS needs your numeric Telegram user ID for the allowlist. This is NOT your username — it's a number like `123456789`.

1. In Telegram, search for `@userinfobot`
2. Tap **Start** (or send `/start`)
3. The bot replies with your info:
   ```
   Id: 123456789
   First: Nathan
   Last: Maine
   Lang: en
   ```
4. **Copy the Id number** — you'll need it for `allowed_user_ids`

## Step 4: Configure Bot Privacy (Required for Groups)

By default, Telegram bots in groups only see messages that start with `/` or mention the bot directly. For MOPS to work in groups, you need to disable privacy mode.

1. Go back to `@BotFather`
2. Send:
   ```
   /mybots
   ```
3. Select your bot from the list
4. Tap **Bot Settings**
5. Tap **Group Privacy**
6. Tap **Turn off**

BotFather confirms: "Privacy mode is disabled for your bot."

This allows MOPS to see all messages in groups where it's a member (MOPS still enforces its own allowlist — only authorized users and groups get responses).

## Step 5: Run MOPS Onboarding

Now run MOPS:

```bash
mops
```

The onboarding wizard will ask for:

1. **Bot token** — paste the token from Step 2
2. **Your user ID** — paste the number from Step 3
3. **Timezone** — your IANA timezone (e.g., `America/Chicago`)
4. **Docker sandboxing** — optional, recommended for security
5. **Background service** — optional, keeps MOPS running after you close the terminal

After onboarding completes, open Telegram, find your bot by its username, tap **Start**, and send a message. MOPS responds.

## Step 6: Group Setup (Optional)

To use MOPS in a Telegram group:

### Create the group and add the bot

1. Create a new Telegram group (or use an existing one)
2. Add your bot as a member: search for `@your_bot_username` in the "Add members" screen
3. The bot will join but won't respond until you authorize the group

### Get the group ID

1. Add `@userinfobot` to the group temporarily
2. Send any message in the group
3. The bot replies with the group info including the **chat ID** (a negative number like `-1001234567890`)
4. Copy this number
5. Remove `@userinfobot` from the group (optional)

### Authorize the group

Add the group ID to `allowed_group_ids` in `~/.mops/config/config.json`:

```json
{
  "allowed_group_ids": [-1001234567890],
  "allowed_user_ids": [123456789]
}
```

Both the group AND the user must be in their respective allowlists. This is a dual-check security model — unauthorized users in authorized groups are still blocked.

Allowlists hot-reload — no restart needed after editing `config.json`.

## Step 7: Enable Topics (Optional)

Telegram forum topics let you run multiple isolated AI conversations in one group.

1. Open the group → tap the group name → **Edit** (pencil icon)
2. Scroll down and enable **Topics**
3. Create topics for your projects (e.g., "Backend", "Frontend", "Research")

Each topic gets its own isolated session in MOPS — separate conversation history, separate provider choice. Switch models per-topic with `/model`.

## Step 8: Sub-Agent Bots (Optional)

For sub-agents, each one needs its own bot token:

1. Repeat Steps 1–2 with BotFather for each sub-agent (e.g., `my_researcher_bot`, `my_coder_bot`)
2. Add sub-agents via:
   ```bash
   mops agents add researcher
   ```
3. The wizard asks for the new bot's token and user IDs

Each sub-agent gets its own Telegram chat, workspace, and session state.

---

## Quick Reference

| Item | Where to get it | Example |
|------|----------------|---------|
| Bot token | `@BotFather` → `/newbot` | `7123456789:AAHBx3mK9z...` |
| User ID | `@userinfobot` → `/start` | `123456789` |
| Group ID | Add `@userinfobot` to group | `-1001234567890` |

## Troubleshooting

### Bot not responding in private chat
- Verify your user ID is in `allowed_user_ids`
- Make sure you tapped **Start** on the bot first
- Check `mops status` to confirm MOPS is running

### Bot not responding in group
- Verify both group ID and user ID are in their allowlists
- Confirm privacy mode is **disabled** (Step 4)
- If `group_mention_only` is `true` in config, mention or reply to the bot

### "Bot token invalid" during onboarding
- Copy the token again from BotFather — make sure there are no extra spaces
- The token format is: `numbers:letters-and-numbers`
- If you regenerated the token, the old one is invalidated

### Need a new token
Send `/revoke` to `@BotFather`, select your bot, and you'll get a fresh token. Update it in `~/.mops/config/config.json` and restart MOPS.
