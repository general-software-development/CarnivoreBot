# CarnivoreBot Privacy Policy

Last modified: 16th September 2026

Identifier: `01a0ab71-9b73-700d-8c4c-522cb6dafdb5:8ee1fb30-c372-4fae-b85f-cfb9d87e36a0:SHA3-512-(Zx6PI+Sak{;o7Lnc99msY2!Lh(O&I=EXD8=Pk8yRp2)^<q@(+vXM577Q?JRse1#;7qFlXW^ajr7*m+i`

Controller: GitHub user `bogdan-glitchm` (see Contact)

## Data Processing

The categories listed underneath Optional Identifiable/Non-Identifiable Data Processing are automatically processed upon using the bot.

The categories listed underneath Mandatory Data Processing are processed on the basis of legitimate interest.

### 1. Mandatory Data Processing

| Data | Processing | Storage | Distribution | Reason |
| :--: | :--------: | :------: | :--------: | :----: |
| Non-command Message contents | Always | Temporary (<48h) | No | Processed to determine whether they are commands or not; potentially stored due to caching |

This data may be collected through native Discord API's and `on_message` hooks, even when not interacting with the bot, as they are required for the bot's core behaviour.

### 2. Optional Identifiable Data Processing

| Data | Processing | Storage | Distribution | Reason | Legal Basis |
| :--: | :--------: | :------: | :--------: | :----: | :-: |
| User ID | Always | Depends | Sometimes | Used for whitelist behaviours, logging, and ratelimits, potentially logged or cached | Legitimate Interest |
| Username | Sometimes | Temporary (<48h) | Sometimes | Used for whitelist behaviours and logging, potentially logged or cached | Legitimate Interest |

This data may be collected through native Discord API's and `on_message` hooks, when a message represents or is similar to one of the bot's commands. If 
a message does not represent a valid command, this data will not be collected.

### 3. Optional Non-Identifiable Data Processing

| Data | Processing | Storage | Distribution | Reason | Legal Basis |
| :--: | :--------: | :------: | :--------: | :----: | :-: |
| Commands | Always | Temporary (<365d) | Sometimes | Processed for core bot behaviour, potentially cached, logged, or distributed | Legitimate Interest |
| Message Contents | Always | Sometimes | Sometimes | Used for processing flags and arguments, which may be potentially stored in a database. One example of arguments being stored is `config.set`, which sets a per-server configuration value. | Legitimate Interest |

## Data Collection

The data we collect:

### User Data

| Data | Details | Reason/Purpose | Legal Basis |
| :--: | :-----: | :----: | :-----------------: |
| User ID | &mdash; | Whitelist behaviours, logging, ratelimits, caching | Legitimate Interest |
| Username | &mdash; | Whitelist behaviours, logging, caching | Legitimate Interest |
| Message Contents | &mdash; | Core bot behaviour, storing settings | Legitimate Interest |
| Command Usage | Commands used, User ID, usage timestampts | Used for ratelimiting and logging | Legitimate Interest |
| Guild permissions | What permissions the user has in the server | Used for whitelisting behaviour and permissions | Legitimate Interest |

### Server Data

| Data | Details | Reason/Purpose | Legal Basis |
| :--: | :-----: | :----: | :---: |
| Server Settings | &mdash; | Core bot behaviour and configuration | Legitimate Interest |
| Channel ID | Where messages are sent | Core bot behaviour | Legitimate Interest |
| Guild ID | &mdash; | Core bot behaviour | Legitimate Interest |
| Guild owner ID | &mdash; | Bot permission systems | Legitimate Interest |

## Data Retention

### User Data

| Data | Retention | Contents | Legal Basis |
| :--: | :-------: | :-----: | :---------: |
| User/Account Identification | Indefinite | User IDs, Usernames | Legitimate Interest |
| User Permissions & Roles | Temporary/Unknown (library caches) | Roles, Guild permissions | Legitimate Interest |

* **User/Account Identification:** User IDs and Usernames are generally stored temporarily and transiantly, though they may be left over in caches. However, user IDs may be stored indefinitely for whitelisting and blacklisting behaviour.

### Server Data

| Data | Retention | Contents | Legal Basis |
| :--: | :-------: | :-----: | :---------: |
| Server Settings | Indefinite, until deleted | *N/A* | Consent (consented to when using the `config.set` command) |
| Server Identification | Temporary/Unknown (transient in-memory usage, library caches) | Guild ID, Channel IDs | Legitimate Interest |
| Server Ownership | Temporary/Unknown (transient in-memory usage, library caches) | Guild owner's user ID | Legitimate Interest |

* **Server Settings:** To delete a setting, run `config.set <setting>` without specifying a value. This will delete it from the database. This is designed both as a way of deleting settings, and as a mechanism for withdrawal of consent.

## Children's Data & Child Safety

CarnivoreBot is designed as a Discord bot, or the implementation for one. As Discord is a 13+ platform, CarnivoreBot should not normally, is not designed to, and is not intended to collect data from children under 13. It does not knowingly or purposefully request data from children under 13, and does not knowingly request data from children for purposes unrelated to providing CarnivoreBot's features.

If a legal guardian believes their child has submitted sensitive, private or personal information to CarnivoreBot (see Data Collection), they may contact us for the **Right to Erasure**.

This section describes our current practices and is not a statement of legal compliance in any particular jurisdiction.

## Data Distribution

Data distribution may be disclosed or shared with third parties for the following purposes:

* Third parties being individual legal persons, for **debugging** purposes

Outside of the aforementioned criteria, we do not share your data.

We do not sell any of your data to anyone.

## Changes to This Privacy Policy

We may update this Privacy Policy from time to time. Any changes will be made to this file and uploaded to GitHub, and we will update the "Last Modified" field. Your continued use of the bot after any changes signifies your acceptance of the new policy.

## Contact

For any questions or inquiries, contact us at `github.34373732+legal@gmail.com`.

To exercise your Right to Erause or Right to Access, contact us at `github.34373732+legal@gmail.com` with either "Right to Erasure" or "Right to Access" as the subject line.
