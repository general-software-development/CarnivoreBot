# CarnivoreBot Privacy Policy

Last modified: 15th September 2026

## Data Processing

### 1. Mandatory Data Processing

| Data | Processing | Storage | Distribution | Reason |
| :--: | :--------: | :------: | :--------: | :----: |
| User ID | Sometimes | Sometimes | Sometimes | Used for blacklist behaviours, requiring storage |
| Non-command Message contents | Always | Temporary (<48h) | No | Processed to determine whether they are commands or not; potentially stored due to caching |

This data may be collected through native Discord API's and `on_message` hooks, even when not interacting with the bot, as they are required for the bot's core behaviour.

### 2. Optional Identifiable Data Processing

| Data | Processing | Storage | Distribution | Reason |
| :--: | :--------: | :------: | :--------: | :----: |
| User ID | Always | Temporary (<48h) | Sometimes | Used for whitelist behaviours, logging, and ratelimits, potentially logged or cached |
| Username | Sometimes | Temporary (<48h) | Sometimes | Used for whitelist behaviours and logging, potentially logged or cached |

This data may be collected through native Discord API's and `on_message` hooks, when a message represents or is similar to one of the bot's commands. If 
a message does not represent a valid command, this data will not be collected.

Please note that, for these data categories, requesting permanent deletion of this data via your **Right to Erasure** is impossible due to technological constraints, and requesting a copy of this data via your **Right to Access** is impossible due to them being impossible for the operator to purposefully access and incredibly short-lived. None of this data is stored in a database.

### 3. Optional Potentially-Identifiable Data Processing

| Data | Processing | Storage | Distribution | Reason |
| :--: | :--------: | :------: | :--------: | :----: |
| Message Contents | Always | Sometimes | Sometimes | Used for processing flags and arguments, which may be potentially stored in a database. One example of arguments being stored is `config.set`, which sets a per-server configuration value. |

### 4. Optional Non-Identifiable Data Processing

| Data | Processing | Storage | Distribution | Reason |
| :--: | :--------: | :------: | :--------: | :----: |
| Commands | Always | Temporary (<365d) | Sometimes | Processed for core bot behaviour, potentially cached, logged, or distributed |

## Data Collection

The data we collect:

### User Data

| Data | Details | Reason/Purpose |
| :--: | :-----: | :----: |
| User ID | &mdash; | Whitelist behaviours, logging, ratelimits, caching |
| Username | &mdash; | Whitelist behaviours, logging, caching |
| Message Contents | &mdash; | Core bot behaviour, storing settings |
| Command Usage | Commands used, User ID, usage timestampts | Used for ratelimiting and logging |
| Guild permissions | What permissions the user has in the server | Used for whitelisting behaviour and permissions |

### Server Data

| Data | Details | Reason/Purpose |
| :--: | :-----: | :----: |
| Server Settings | &mdash; | Core bot behaviour and configuration |
| Channel ID | Where messages are sent | Core bot behaviour |
| Guild ID | &mdash; | Core bot behaviour |
| Guild owner ID | &mdash; | Bot permission systems |

## 5. Contact

For any questions or inquiries, contact us at `github.34373732+legal@gmail.com`.

To exercise your Right to Erause or Right to Access, contact us at `github.34373732+legal@gmail.com` with either "Right to Erasure" or "Right to Access" as the subject line.
