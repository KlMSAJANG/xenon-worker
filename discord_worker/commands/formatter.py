from dataclasses import dataclass


@dataclass()
class Format:
    color: int = None
    title: str = None
    icon: str = None


class Formatter:
    DEFAULT = Format()
    INFO = Format(
        title="Info",
        color=0x478fce,
        icon="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678110-sign-info-512.png"
    )
    SUCCESS = Format(
        title="Success",
        color=0x48ce6c,
        icon="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678134-sign-check-512.png"
    )
    WARNING = Format(
        title="Warning",
        color=0xefbc2f,
        icon="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678136-shield-warning-512.png"
    )
    ERROR = Format(
        title="Error",
        color=0xc64935,
        icon="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678069-sign-error-512.png"
    )
    WORKING = Format(
        title="Please Wait ...",
        color=0x36393e,
        icon="https://images-ext-1.discordapp.net/external/AzWR8HxPJ4t4rPA1DagxJkZsOCOMp4OTgwxL3QAjF4U/https/"
             "cdn.discordapp.com/emojis/424900448663633920.gif"
    )
    WAITING = Format(
        title="Waiting for Input ...",
        color=0x478fce,
        icon="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/bubbles-alt2-512.png"
    )

    def format(self, content="", *, embed=None, f: Format = DEFAULT, **kwargs):
        formatted = {
            "color": f.color,
            "description": content,
            "author": {
                "name": f.title,
                "icon_url": f.icon
            }
        }

        if embed is not None:
            formatted.update(embed)

        return dict(
            embed=formatted,
            **kwargs
        )
