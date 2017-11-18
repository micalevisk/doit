<p align="center">
        <img src=".github/logo.png"/>
</p>

[![Add](https://img.shields.io/badge/Add%20to-Telegram-00afee.svg?style=flat-square)](https://t.me/ne_robot)
![language](https://img.shields.io/badge/language-Python-brightgreen.svg?style=flat-square)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/enotcode/todobot.svg?style=flat-square)](https://scrutinizer-ci.com/g/enotcode/todobot/?branch=master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/enotcode/todobot/blob/master/LICENSE)

# ToDo 🚀

[ToDo 🚀](https://t.me/ne_robot) — is a simple tool to manage daily tasks

# Where to go for help?

If you need help with, you can [open an issue](https://github.com/enotcode/todobot/issues/new), or seek support to [@enotcode](https://t.me/enotcode)

Thanks for using the bot ❤️

# Want to contribute?

[ToDo 🚀](https://t.me/ne_robot) — is a non-profit project.

If you want to help the project, please do so fixing [issues](https://github.com/enotcode/todobot/issues) from the list and creating a pull request.

Please use [PEP8](https://www.python.org/dev/peps/pep-0008/) Style Guide as the main tool to follow our project-wide code style.

You can also evaluate bot in [StoreBot](https://t.me/storebot?start=ne_robot).

# Installation

```sh
git clone https://github.com/enotcode/todobot.git
cd todobot
pip install -r requirements.txt
```

Then set the environment variable:

* **TOKEN** - token for your telegram bot (received from [@BotFather](https://t.me/BotFather))
* **BASE** - url of your mongo database (*for example* `mongodb://localhost:27017/`)
* **BOTAN** - api key for statistics your telegram bot (read more here [botan.io](https://botan.io))
* **ADMIN** - the administrator ID of the bot (you can read it from the [@JsonDumpBot](https://t.me/JsonDumpBot))
* **URL** - url of your bot server (*for example* `https://localhost:5000/`)

After that you can start the bot with the command

```sh
python bot.py
```

# License

[MIT](/LICENSE/)
