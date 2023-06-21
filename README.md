# Rontext

A new way for find and navigate your files, purely based on context.

----------
## Initial Configuration

What things you need to install the software and how to install them

*Warning:* This section was tested using:
- Debian 10 (2019-12-28)
- Linux Mint 19.2 (2019-12-28)
- elementary OS 5 (2019-12-28)
- Manjaro (5.15.114-2) (2023-06-21)

I do not recommend installing and running this software withouth development skills.

#### Setup - the easy way:

After clonning the project, open the project directory in some shell and run:
1. If you're using a debian-based GNU/Linux distribution: `make debian-based-setup`
2. If you're using a arch-based GNU/Linux distribution: `make arch-based-setup`

After running the distribution-specific setup, run: `make setup`

#### Setup - the DIY way:

Install all the dependencies, for your current Linux distribution equivalent to the following debian packages:

```
- ruby
- ri
- ruby-bundler
- ruby-dev
- python3-pip
- make
- build-essential
- libssl-dev
- zlib1g-dev
- libbz2-dev
- libreadline-dev
- libsqlite3-dev
- wget
- curl
- llvm
- libncurses5-dev
- libncursesw5-dev
- xz-utils
- tk-dev
```

Create the python virtual environment:
```bash
python3 -m venv venv
```

Install the python dependencies:
```bash
pip3 install -r requirements.txt
```

Install the ruby dependencies:
```bash
gem install icalendar
```

Now the project should be ready to run

## Getting Started

*Warning: The Rontext is actually under development, and is not recommended in this phase for non-developers.*

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Clone the lastest stable (vX.X.0-stable) or beta (vX.X.X) version from https://github.com/joaovitor123jv/rontext
2. Install the dependencies (see Initial Configuration)
3. Open two shell instances in the project root and activate the python virtual environment in both of them:
    - `source venv/bin/activate`
4. Create a directory named `Rontext` in your home directory: `mkdir $HOME/Rontext`
5. Run `./filesystem_listener/main.py` in one instance
6. Run `./virtual_filesystem/main.py` in the remaining instance

To stop the software:
1. Go to the shell instances running this software and run `ctrl+c` twice in both instances.

To configure the software:
1. Explore the configurations in `$HOME/.ctxt_search-config.yml` and fix what you think is wrong for you.

Running the software (after configuring):
1. Open two shell instances in the project root and activate the python virtual environment in both of them:
    - `source venv/bin/activate`
2. Run `./filesystem_listener/main.py` in one instance
3. Run `./virtual_filesystem/main.py` in the remaining instance


## Built With

* [Python](https://www.python.org/) - The main scripting language
* [Ruby](https://www.ruby-lang.org/) - Used to parse the calendar files
* [SQLite3](https://www.sqlite.org/index.html) - The database used

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/joaovitor123jv/rontext/tags). 

## Authors

* **João Vitor** - *Initial work* - [joaovitor123jv](https://github.com/joaovitor123jv)

See also the list of [contributors](https://github.com/joaovitor123jv/rontext/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


-----

# TODO

### Already implemented:
* Access type, changed from IN\_ACCESS to IN\_OPEN, to identify only file openings
* Added partial file path checking directly in configuration file
* Added navigation through events
* Added navigation through localizations
* Implemented testing system
* Added README.md
* Add LICENSE.md
* Add CONTIBUTING.md
* Remove `__pycache__` directories from git tracking
* Update running and install instructions
* Add instalation instructions

### What I need to do:
* Add testing scripts
* Add testing instructions
* Add "rename" localization function
    - This will allow the user to personalize the localization name, to give it a meaning. Not only "localization 1"
* Move the project to a closer system language (like C++)
* Fix crash after `file permission` on recursive listening mode
* Daemonize the system (boot with the operating system)
* Integrate calendar files with the cloud, and get the events directly from google servers.
* Add translations to directories
* Test, Test, Test!
* Launch a stable release
