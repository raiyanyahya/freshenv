
[![Actions Status](https://github.com/raiyanyahya/freshenv/workflows/Build%20Test/badge.svg)](https://github.com/raiyanyahya/freshenv/actions) [![Actions Status](https://github.com/raiyanyahya/freshenv/workflows/Package%20Release/badge.svg)](https://github.com/raiyanyahya/freshenv/actions) [![Actions Status](https://github.com/raiyanyahya/freshenv/workflows/Integration%20Tests/badge.svg)](https://github.com/raiyanyahya/freshenv/actions) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=raiyanyahya_freshenv&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=raiyanyahya_freshenv) [![CodeQL](https://github.com/raiyanyahya/freshenv/workflows/CodeQL/badge.svg)](https://github.com/raiyanyahya/freshenv/actions?query=workflow%3ACodeQL) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/786fd03c3cc5450c8ad6cf7c00302a94)](https://www.codacy.com/gh/raiyanyahya/freshenv/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=raiyanyahya/freshenv&amp;utm_campaign=Badge_Grade) [![](https://img.shields.io/badge/python-3.6+-blue.svg)]() [![](https://img.shields.io/github/license/raiyanyahya/freshenv.svg)]() [![freshenv](https://snapcraft.io/freshenv/badge.svg)](https://snapcraft.io/freshenv)
 [![PyPI version](https://badge.fury.io/py/freshenv.svg)](https://badge.fury.io/py/freshenv) [![PyPI download month](https://img.shields.io/pypi/dm/freshenv.svg)](https://pypi.python.org/pypi/freshenv/) [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)


# Freshenv 🥗
```freshenv``` is a  command line application to provision and manage local developer environments. Build and develop your projects in completely isolated environments. Save, switch and restart your environments. Choose from a wide variety of flavours to get the developer tools you need.\
\
<kbd>
[![download-17adc07640182f121.gif](https://s10.gifyu.com/images/download-17adc07640182f121.gif)](https://gifyu.com/image/Sbsim)
</kbd>
## The Story

This is a solution to a problem I have always had. I like my system to be clean, minimal and structured. 
It gets quite tricky to manage multiple projects on my on machine, projects tend to gather and are placed everywhere. 
Overtime managing system wide dependencies becomes a problem. It is quite easy to mess up a system setting or to 
keep track of a package I wont need tomorrow. This is why I built ```freshenv```. It is a command line application
 which helps developers in running and managing completely isolated developer environments locally. 
It fetches and lets you run environment flavours in the form of docker containers
which are preconfigured with tools and packages developer needs everyday. Read about the usage below. 
I imagine it would help developers like me. I hope you like it.

## Flavours

```freshenv flavours``` are different configurations for freshenv environments. You choose a flavour and provision it as an environment. A flavour can be a combination of operating systems, language packs, tools and application bundles. By default freshenv provisions you with a ```base``` flavour which runs ubuntu 18.04 and has packages like ```wget git python3-pip curl zsh wget nano zsh``` and more. The base flavour is a 260mb environment when provisioned. There are bigger flavours like ```devenv``` which runs on the latest ubuntu and has been loaded and configured with ```docker (run docker inside your freshenv environment), golang, python, node, java, a vscode server, build-essential automake make cmake sudo g++ wget git python3-pip curl zsh wget nano nodejs npm fonts-powerline``` and more. This environment is around 1.6gb large. Freshenv also gives you the option to provision a language based environment which contains necessary developer tools for that language. Checkout the usage section below on the flavours command to see a list of flavours available.

Freshenv depends on docker and python. You must have ```docker``` and ```python3.6+```  installed to be able to use the cli.

## Installation Linux

I recommend using the snap package manager to install freshenv. 

```console
  snap install freshenv 
  snap connect freshenv:docker docker:docker-daemon # give it access to the docker interface
```

If you dont have or use snap, install the freshenv python package from pypi. 

```console
  pip install freshenv
```

I would recommend using pipx instead of pip to install cli applications on you machine.

## Installation MacOS

I am trying to get freshenv on homebrew-core but I need more stars on the repository for 
them to accept my pull request. The self hosted tap is available
on the repo raiyanyahya/homebrew-freshenv. Install the freshenv python package from a self hosted homebrew tap.

```console
  brew tap raiyanyahya/freshenv
  brew install freshenv
```

## Usage

```console
Usage: fr [OPTIONS] COMMAND [ARGS]...

  A cli to provision and manage local developer environments.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  check      Check system compatibility for running freshenv.
  clean      Remove all freshenv flavours and environments.
  flavours   Show all available flavours for provisioning.
  provision  Provision a developer environment.
  remove     Remove a freshenv environment.
  start      Resume working in an environment.
  view       View local freshenv managed environments.
```

### Commands and Options

**```flavours```**
```console
Usage: fr flavours [OPTIONS]

  Show all available flavours for provisioning.

Options:
  --help  Show this message and exit.
```


**```provision```**
```console
Usage: freshenv provision [OPTIONS]

  Provision a developer environment.

Options:
  -f, --flavour TEXT   The flavour of the environment.  [default: base]
  -c, --command TEXT   The command to execute at startup of environment.[default: zsh]
  -p, --ports INTEGER  List of ports to forward.  [default: 3000]
  -n, --name TEXT      Name of your environment.
  --help               Show this message and exit.
```


**```start```**
```console
Usage: freshenv start [OPTIONS] NAME

  Resume working in an environment.

Options:
  --help  Show this message and exit.
```

**```remove```**
```console
Usage: freshenv remove [OPTIONS] NAME

  Remove a freshenv environment.

Options:
  -f, --force      Force remove an environment.
  --help           Show this message and exit.
```

**```view```**
```console
Usage: freshenv view [OPTIONS]

  View local freshenv managed environments.

Options:
  --help  Show this message and exit.
```

**```check```**
```console
Usage: freshenv check [OPTIONS]

  Check system compatibility for running freshenv.

Options:
  --help  Show this message and exit.
```

**```clean```**
```console
Usage: fr clean [OPTIONS]

  Remove all freshenv flavours and environments.

Options:
  -f, --force  Force remove freshenv flavours and environments.
  --help       Show this message and exit.
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started. Please adhere to this project's `code of conduct`.


## Contact

Contact me through email at contact@freshenv.io
