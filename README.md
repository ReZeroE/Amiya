# Amiya
Amiya - a lightweight cross-platform automation tool that allows scheduled start and automation of any application from the CLI.


<div align="center">
    <p style="padding-bottom: 0">
        <img src="https://i.imgur.com/l6VZmHq.png" alt="Amiya Icon" width="85%" height="auto"/>
    </p>
    <!-- <span style="color: #093163">A lightweight cross-platform automation tool for daily tasks!</span> -->
</div>


## Overview
_This project is currently in development (`Development Status :: 4 - Beta`)._

Amiya is a easy-to-use and versatile cross-platform application and game automation tool designed for efficiency and ease of use directly from the CLI. This package offers automation capabilities for any applications (including games), enabling users to start and control any application with simple CLI commands.


The primary features supported by the `amiya` package are:
1. **Application Launcher**: Start and terminate any applications from the CLI
2. **Automation Controller**: Automate any applications with recorded mouse & keyboard sequences
3. **Scheduling**: Schedule the start/automation of any application to run at any time
4. **Other Utilities** Other lightweight quality-of-life utilities for applications:
    - Volume control by individual application (GUI)
    - Shutdown/Sleep/Hibernate PC after countdown
    - Internet speed test (CLI), etc.


Designed to be lightweight and fully CLI-based, Amiya is perfect for users who need a reliable and scalable solution for managing and automating their software applications or games.


## Installation Guide
To install the beta version of the `amiya` package locally, run:
```bash
$ pip install amiya==0.0.4
```
OR
```bash
$ git clone https://github.com/ReZeroE/Amiya.git
$ cd Amiya/
$ pip install -e .
```

**Alternatively**, you may install the most up-to-date development version by cloning the `dev` branch (unstable):
```bash
$ git clone -b dev https://github.com/ReZeroE/Amiya.git
$ cd Amiya/
$ pip install -e .
```
## Usage Guide
To activate the Amiya CLI environment after installation, simply run:
```
$ amiya
```
Then the CLI environment should be activated with the following being displayed.
```

                                          _    __  __ _____   __ _       ____ _     ___
                                         / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _|
                                        / _ \ | |\/| || | \ V // _ \   | |   | |    | |
                                       / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |
                                      /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___|

                            A lightweight cross-platform automation tool for games and daily tasks!
                                               https://github.com/ReZeroE/Amiya
                                                          By Kevin L.

Welcome to the Amiya CLI Environment (Beta-0.0.4)
  Type 'help' to display commands list
  Type 'exit' to quit amiya CLI
  Type 'clear' to clear terminal

[02:12:34 Amiya-CLI] >
```
To list all commands currently supported, run:
```
[02:12:34 Amiya-CLI] > help
```

##### More Documentation Coming soon!

## Amiya CLI Key Bindings
Windows terminals' navigation and key bindings can often be cumbersome and less intuitive compared to Linux terminals. To address this, the Amiya CLI environment incorporates these familiar _**Linux-style key bindings**_ to make command-line navigation and editing easier and more efficient.

#### Supported Key Bindings
- Ctrl + W: Delete the word before the cursor.
- Ctrl + A: Move the cursor to the beginning of the line.
- Ctrl + E: Move the cursor to the end of the line.
- Ctrl + U: Clear the line before the cursor.
- Ctrl + K: Kill (cut) text from the cursor to the end of the line.
- Ctrl + Y: Yank (paste) the most recently killed text.
- Ctrl + B: Move backward one character.
- Ctrl + F: Move forward one character.
- Ctrl + P: Move to the previous line in the history.
- Ctrl + N: Move to the next line in the history.
- Ctrl + B: Move backward one word.
- Ctrl + F: Move forward one word.


## Commands List
```
$ amiya --help

☆ About : Get information about the Amiya module in general.
  amiya version: Verbose module version
    -h, --help: show this help message and exit

  amiya author: Verbose module author
    -h, --help: show this help message and exit

  amiya repo: Verbose module repository link
    -h, --help: show this help message and exit


☆ App Management : Add, remove, and show applications in Amiya's app configuration.
  amiya add-app: Add a new application
    -h, --help: show this help message and exit

  amiya remove-app: Remove an existing application
    -h, --help: show this help message and exit
    tag: Tag of the application to remove

  amiya show-apps: Show applications
    -h, --help: show this help message and exit
    --short, -s: Only show the app ID, name, and verification status
    --full-path, -f: Show the full path of the applications

  amiya show-config: Show application configuration directory
    -h, --help: show this help message and exit
    tag: Tag of the application to show the configuration directory of
    --all, -a: Show all configuration directory paths (including automation)


☆ Application Launcher : Start or terminate applications from the CLI.
  amiya start: Start an application
    -h, --help: show this help message and exit
    tag: Tag of the application to start


☆ Tag Management : Add or remove tags associated with applications configured with Amiya.
  amiya add-tag: Add a new tag to an application
    -h, --help: show this help message and exit

  amiya remove-tag: Remove a tag from an application
    -h, --help: show this help message and exit


☆ Automation : Record, show, and run automations in applications.
  amiya list-auto: List all the automation sequences of the application
    -h, --help: show this help message and exit
    tag: Tag of the application

  amiya record-auto: [Admin Permission Req.] Record an automation sequence of the application
    -h, --help: show this help message and exit
    tag: Tag of the application

  amiya run-auto: [Admin Permission Req.] Run an automation sequence of the application
    -h, --help: show this help message and exit
    tag: Tag of the application
    seq_name: Name of the sequence to run
    --global-delay, -g: Add a global delay to the sequence during execution
    --terminate, -t: Terminate the application on automation completion
    --no-confirmation, -nc: Run the automation without confirmation
    --sleep: Put PC to sleep after automation finishes (overwrites --shutdown)
    --shutdown: Shutdown PC after automation finishes


☆ Sync Commands : Sync (auto-locate) and cleanup applications across different local machines.
  amiya sync: Sync configured applications on new machine OR auto configure application executable paths
    -h, --help: show this help message and exit

  amiya cleanup: Remove all unverified applications
    -h, --help: show this help message and exit


☆ Utility : Other useful and easy-to-use utilities provided by the Amiya module.
  amiya search: Initiate a search on the default browser
    -h, --help: show this help message and exit
    search_content: Content of the search

  amiya sleep: Put the PC to sleep after X seconds
    -h, --help: show this help message and exit
    delay: Delay in seconds before sleep

  amiya shutdown: Shutdown PC after X seconds
    -h, --help: show this help message and exit
    delay: Delay in seconds before shutdown

  amiya uuid: Display system UUID
    -h, --help: show this help message and exit

  amiya pixel: Track cursor position and color
    -h, --help: show this help message and exit
    --color, -c: Show pixel coordinate as well as the pixel's color hex value.

  amiya volume: Open simple application volume control UI
    -h, --help: show this help message and exit

  amiya click: Continuously click mouse.
    -h, --help: show this help message and exit
    --count, -c: Number of clicks. Leave empty (default) to run forever
    --interval, -d: Interval delay (seconds) between clicks
    --hold-time, -ht: Delay (seconds) between click press and release
    --start-after, -sa: Delay (seconds) before the clicks start
    --quiet, -q: Run without verbosing progress

  amiya elevate: Elevate `amiya` permissions.
    -h, --help: show this help message and exit
    --explain: Explain why this is needed and what will happen.

  amiya track-url: Track URL to monitor anchor href changes.
    -h, --help: show this help message and exit
    --url: The website URL to track
    --interval, -i: The interval duration between GET requests (seconds). Defaulted to 0.
    --open, -o: Open the URL when it is detected as new.

☆ Development : Developer's commands. Open available when [constants.DEVELOPMENT=True].
  amiya dev: [DEV] Developer's commands.
    -h, --help: show this help message and exit
    --objects, -obj: Show all controller objects and their addresses.
    --refresh, -ref: Refresh all controller objects.
    --code, -c: Open development environment with VSCode.
    --isadmin, -ia: Show whether the main thread has admin access.
```




