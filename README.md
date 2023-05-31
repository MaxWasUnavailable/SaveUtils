# SaveUtils

## About

SaveUtils is a simple library and command line tool for interacting with Shadows of Doubt save files.

## Usage

### Library

The Python code can be used as a library. The `SaveFile` class is the main class that should be used.

This class can be used to read and parse save files, and have a number of methods to interact with the data in an
object-oriented way.

The cheat tools might be useful as examples, or as helper methods.

### Command Line Tools

The primary use of this project is to provide command line tools to interact with save files.

Although this can be useful for modding (or for cheating), the primary use is currently the character migration tool.

To use these, open a command prompt (console) in the tool's folder, and run the tool with the `-h` flag to see the help.

Examples and explanations are provided below.

#### Cheats

There currently are two "cheat" tools available:

- Money cheats
- Health cheats

##### Money Cheats

Adding, removing, setting, and printing of money is supported.

> Examples:
> - Add 100 money to the player's money:
> ```shell
> saveutils.exe -i "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My Save File.sod" money -a 100
> ```
> - Set the player's money to 10000:
> ```shell
> saveutils.exe -i "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My Save File.sod" money -s 10000
> ```

##### Health Cheats

Adding, removing, setting, and printing of health is supported.

> Examples:
> - Add 0.1 health to the player's health:
> ```shell
> saveutils.exe -i "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My Save File.sod" health -a 0.1
> ```
> - Set the player's health to 1:
> ```shell
> saveutils.exe -i "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My Save File.sod" health -s 1
> ```

#### Character Migration

Arguably the most useful tool in this program is the character migration tool.

It allows you to migrate your character from one save file to another, keeping your stats, money, health, inventory,
upgrades, and more.

There is a generic migration command, and a "new game plus" version.

##### Generic Migration

The generic migration tool allows you to migrate your character from one save file to another in the exact same state.

*(Currently, some stats such as thirst, hunger, temperature, etc... are not migrated, since this could be immersion
breaking for some players if they use this to simulate a longer-term move from one city to another. This can be easily
changed if people request it.)*

> Example:
> - Migrate the character from `My Save File.sod` to `My New Save File.sod`:
> ```shell
> saveutils.exe -i "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My Save File.sod" migrate -o "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My New Save File.sod"
> ```

##### New Game Plus

New game plus is a special type of migration that allows you to migrate your character from one save file to another,
but with some small differences:

- There are travel expenses worth 20k money, which you need to be able to pay before being able to migrate.
- Your apartment(s) will be sold for 2k each, to help pay for the travel expenses. (I plan on eventually using the
  actual purchase value, but could not immediately find this in the save data - if it even is available)
- The travel expenses will be subtracted from your money.

This system should make it a bit more realistic, and also make it a bit more challenging to migrate.

> Example:
> - New game plus migrate the character from `My Save File.sod` to `My New Save File.sod`:
> ```shell
> saveutils.exe -i "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My Save File.sod" migrate -n -o "C:\Users\max\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Save\My New Save File.sod"
> ```

## Authors

* [MaxWasTaken](https://github.com/MaxWasUnavailable)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.