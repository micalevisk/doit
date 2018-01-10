<p align="center">
        <img src=".github/logo.png"/>
</p>

[![Add](https://img.shields.io/badge/Add%20to-Telegram-00afee.svg?style=flat-square)](https://t.me/jditbot)
[![BuildStatus](https://img.shields.io/scrutinizer/build/g/enotcode/doit.svg?style=flat-square)](https://scrutinizer-ci.com/g/enotcode/doit/build-status/master)
[![ScrutinizerCodeQuality](https://img.shields.io/scrutinizer/g/enotcode/doit.svg?style=flat-square)](https://scrutinizer-ci.com/g/enotcode/doit/?branch=master)
![language](https://img.shields.io/badge/language-Python-brightgreen.svg?style=flat-square)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/enotcode/doit/blob/master/LICENSE)

# Just Do It 🚀

[Just Do It 🚀](https://t.me/jditbot) — is a simple tool to manage daily tasks

Bot based on a [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

# Where to go for help?

If you need help with, you can [open an issue](https://github.com/enotcode/doit/issues/new), or seek support to [@enotcode](https://t.me/enotcode)

Thanks for using the bot ❤️

# Want to contribute?

[Just Do It 🚀](https://t.me/jditbot) — is a open-source project.

If you want to help the project, please do so fixing [issues](https://github.com/enotcode/doit/issues) from the list and creating a pull request.

Please use [PEP8](https://www.python.org/dev/peps/pep-0008/) Style Guide as the main tool to follow our project-wide code style.

You can also evaluate bot in [StoreBot](https://t.me/storebot?start=jditbot).

# Installation

```sh
git clone https://github.com/enotcode/doit.git
cd doit
pip install -r requirements.txt
```

Then set the environment variable:

* **TOKEN** - token for your telegram bot (received from [@BotFather](https://t.me/BotFather))
* **BASE** - url of your mongo database (*for example* `mongodb://localhost:27017/`)
* **BOTAN** - api key for statistics your telegram bot (read more here [botan.io](https://botan.io))
* **URL** - url of your bot server (*for example* `https://localhost:5000/`)

After that you can start the bot with the command

```sh
python bot.py
```

# License

[MIT](/LICENSE/)
