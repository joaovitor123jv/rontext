# Rontext

A new way for find and navigate your files, purely based on context.

### Prerequisites

What things you need to install the software and how to install them

*Warning:* This section was tested using Debian 10, Linux Mint 19.2 and elementary OS 5 only. 
I do not recommend installing and running this software withouth any development skills.

#### Easy way:

After clonning the project, open the project directory in some shell and run `./install-dependencies.sh`

#### The "understand it" way:

Install all the dependencies, one-by-one. Open some shell and run these commands.

```
  sudo apt install -y ruby ri ruby-bundler ruby-dev python3-pip

  sudo apt install -y make build-essential libssl-dev zlib1g-dev
  sudo apt install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

  sudo pip3 install pyyaml
  sudo pip3 install inotify
  sudo gem install icalendar
```

## Getting Started

*Warning: The Rontext is actually under development, and is not recommended in this phase for non-developers.*

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Clone the lastest stable (vX.X.0-stable) or beta (vX.X.X) version from https://github.com/joaovitor123jv/ctxtsearch-system
2. Install the dependencies (see Prerequisites)
3. Open two shell instances in the project root
4. Run `./filesystem_listener/main.py` in any of the instances
5. Stop the proccess pressing `ctrl+c` one or two times
6. Explore the configurations in `$HOME/.ctxt_search-config.yml` and fix what you think is wrong for you.
7. Again, run `./filesystem_listener/main.py`.
8. If any error appears, return to step 5.
9. If all goes well, in the remaining shell instance, run `./virtual_filesystem/main.py`
10. If no errors happened, you'll see a `$HOME/Rontext` directory with some directories in. Explore it ;-)

### Installing

Rontext actually has no way to install. It will be developed as the project grows.

## Running the tests

Coming soon

### Break down into end to end tests

Coming soon

### And coding style tests

Actually no coding style tests, but I want to add it.

## Built With

https://www.python.org/
* [Python](https://www.python.org/) - The main scripting language
* [Ruby](https://www.ruby-lang.org/) - Used to parse the calendar files
* [SQLite3](https://www.sqlite.org/index.html) - The database used

## Contributing

Please read [CONTRIBUTING.md](CONTIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/joaovitor123jv/ctxtsearch-system/tags). 

## Authors

* **João Vitor** - *Initial work* - [joaovitor123jv](https://github.com/joaovitor123jv)

See also the list of [contributors](https://github.com/joaovitor123jv/ctxtsearch-system/contributors) who participated in this project.

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

### What I need to do:
* Remove `__pycache__` directories from git tracking
* Add testing scripts
* Add testing instructions
* Add "rename" localization function
    - This will allow the user to personalize the localization name, to give it a meaning. Not only "localization 1"
* Move the project to a closer system language (like C++)
* Update running and install instructions
* Fix crash after `file permission` on recursive listening mode
* Daemonize the system (boot with the operating system)
* Update running and install instructions
* Integrate calendar files with the cloud, and get the events directly from google servers.
* Add instalation instructions
* Add translations to directories
* Test, Test, Test!
* Launch a stable release
