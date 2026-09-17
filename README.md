# CarnivoreBot - Command Usage

## Server Configuration

To create/configure a setting for your server, use the `;config.set <key> <value>` command. To see what keys exist, use `;config.set help` command.

To get all server settings, use the `;config.get` command. To get a specific server setting, use the `;config.get <key>` command.

> [!NOTE]
> To use the `;config.set` or `;config.get` commands, you first need to consent to retention/collection of the **Server Data > Server Configs** data category. Run `;config.set` for instructions on how to do so.

### Configuration Values
The server settings/configs that `;config.set` takes as keys are:
* `gh.repo-owner`: The GitHub user owning a certain repository
* `gh.repo-name`: A GitHub repo owned by `gh.repo-owner`. Used for GitHub Issue Mentions.


## GitHub Issue Mentions

If the `gh.repo-owner` and `gh.repo-name` server settings are configured, when a user types `#` followed by a number (ex. `#3`), the bot will automatically reply with a link to the Issue / Pull Request with that ID.

For example, if a user sends `"Did you see #3?"`, the bot will reply with a link to the third Issue / Pull Request, along with details about it.

## Obtaining a copy of the License / Privacy Policy

While the license and privacy policy are available on the GitHub repository, and are linked in the bot's description, you can also run `;legal license` or `;legal privacy`, and the bot will respond with a PDF-rendered version of the corresponding document as an attachment.

## Ping Command

The `;ping` command, primarily intended for devs but available for anyone, is used to check whether the bot is online and functioning, and the time it takes to reach the database.

## GDPR Command

The `;gdpr consent {add|withdraw} <category>` command is used to handle providing/withdrawing consent to categories of data collected/stored on the legal basis of consent. Run `;gdpr consent` to view its usage.

The available `<category>` values are: `server-settings`.

## CheckIsSpam Command

> [!ERROR]
> This command is currently not guaranteed to be functional and is not currently documented.
