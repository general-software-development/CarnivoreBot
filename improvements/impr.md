# Index

- [ ] CB-1, Admin Privacy Notice Command
- [ ] CB-2, Clean up the code
- [ ] CB-3, Slash command support
- [ ] CB-4, Log Command
- [ ] CB-5, Output initialisation times
- [ ] CB-6, Profiling Command

## CB-1 (Open) <!-- Admin Privacy Notice Command -->

7th October 2026

Author: @bogdan-glitchm

Assigned: @bogdan-glitchm

Add an `;admin privacy-notice` command to send a notice that the privacy policy was changed, to everyone that has used the bot.

Use a table in `dcClient` to track who runs any command.

## CB-2 (Open) <!-- Clean up the code -->

7th October 2026

Author: @bogdan-glitchm

Assigned: @bogdan-glitchm

Clean up code, unused import headers, and more.

## CB-3 (Open) <!-- Slash Command Support -->

7th October 2026

Author: @bogdan-glitchm

Assigned: @bogdan-glitchm

Add slash command support via a new command in `dcClient`.

Use a function to, at runtime, generate pre-defined handler functions, and inject signatures via the `inspect` library to dynamically control the arguments that discord.py will use for slash commands.

Process slash command arguments into standard `msg: discord.message, cmd: typing.Iterable[str]` arguments, passing them to the assigned handler, plus another `interaction: discord.Interaction` parameter with the interaction.

## CB-4 (Open) <!-- Log Command -->

7th October 2026

Author: @bogdan-glitchm

Assigned: @bogdan-glitchm

Add a command to view all logs emitted via the logging library.

This may require storing logs in a `Queue` object to be consumed by the command.

Permissions: bot-owner = `rwx`, whitelist = `rx` (does not delete log entries when read), default = `n`, others = `n`.

## CB-5 (Open) <!-- Output initialisation times -->

7th October 2026

Author: @bogdan-glitchm

Assigned: @bogdan-glitchm

Use a timer to track how much time it takes to initialise the bot and all features.

## CB-6 (Open) <!-- Profiling Command -->

7th October 2026

Author: @bogdan-glitchm

Assigned: @bogdan-glitchm

Add a command to profile the bot when run.

For Python 3.14 and earlier, add a "--profile" flag to enable profiling from program startup.

For Python 3.15 and later, use `profiling.sampling` and start sample profiling after the command is run, returning the profiled times as soon as available.
