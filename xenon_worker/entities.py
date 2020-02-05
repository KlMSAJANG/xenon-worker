from datetime import datetime
import re

from enums import *


DISCORD_EPOCH = 1420070400000
DISCORD_CDN = "https://cdn.discordapp.com"


def parse_time(timestamp):
    if timestamp:
        return datetime(*map(int, re.split(r'[^\d]', timestamp.replace('+00:00', ''))))

    return None


class Snowflake:
    __slots__ = ("id",)

    def __init__(self, id):
        self.id = id

    def __hash__(self):
        return int(self.id) >> 22

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.id != self.id

        return True

    @property
    def created_at(self):
        return datetime.utcfromtimestamp(((int(self.id) >> 22) + DISCORD_EPOCH) / 1000)


class Entity(Snowflake):
    __slots__ = ("_data",)

    def __init__(self, data: dict):
        self._preprocess(data)
        self._data = data

    def _preprocess(self, data):
        pass

    def __getattr__(self, item):
        return self._data.get(item)

    def update(self, data: dict):
        self._preprocess(data)
        self._data.update(data)

    def to_dict(self):
        return self._data


class Role(Entity):
    def _preprocess(self, data):
        self.permissions = None


class Channel(Entity):
    __slots__ = ("type", "guild_id", "position", "permission_overwrites", "name", "topic", "nsfw", "last_message_id",
                 "bitrate", "user_limit", "rate_limit_per_user", "recipients", "icon", "owner_id", "application_id",
                 "parent_id", "last_pin_timestamp")

    def _preprocess(self, data):
        self.type = ChannelType(data["type"])
        self.permission_overwrites = None

    @property
    def icon_url(self):
        return None


class User(Entity):
    __slots__ = ("username", "discriminator", "avatar", "bot", "system", "mfa_enabled")

    @property
    def name(self):
        return self.username

    @property
    def avatar_url(self):
        return None

    @property
    def mention(self):
        return "<@{0.id}>".format(self)

    def __str__(self):
        return "{0.name}#{0.discriminator}".format(self)


class Member(User):
    __slots__ = ("user", "nick", "deaf", "mute", "roles", "joined_at", "premium_since")

    def _preprocess(self, data):
        self.user = User(data["user"])
        self.joined_at = parse_time(data["joined_at"])
        self.premium_since = parse_time(data.get("premium_since"))

    def __getattr__(self, item):
        user_attr = getattr(self.user, item)
        if user_attr is not None:
            return user_attr

        return self._data.get(item)

    def roles_from_guild(self, guild):
        for role in guild.roles:
            if role.id in self.roles:
                yield role


class Guild(Entity):
    __slots__ = ("name", "icon", "splash", "owner", "owner_id", "permissions", "region", "afk_channel_id",
                 "afk_timeout", "embed_enabled", "embed_channel_id", "verification_level",
                 "default_message_notifications", "explicit_content_filter", "roles", "emojis", "features",
                 "mfa_level", "application_id", "widget_enabled", "widget_channel_id", "system_channel_id",
                 "joined_at", "large", "unavailable", "member_count", "voice_states", "members", "channels",
                 "presences", "max_presences", "max_members", "vanity_url_code", "description", "banner",
                 "premium_tier", "premium_subscription_count", "preferred_locale")

    def _preprocess(self, data):
        self.permissions = None
        self.verification_level = VerificationLevel(data["verification_level"])
        self.default_message_notifications = DefaultMessageNotifications(data["default_message_notifications"])
        self.explicit_content_filter = ExplicitContentFilter(data["explicit_content_filter"])
        self.mfa_level = MFALevel(data["mfa_level"])
        self.roles = [Role(d) for d in data["roles"]]
        # self.emojis =
        self.members = [Member(d) for d in data.get("members", [])]
        self.channels = [Channel(d) for d in data.get("channel", [])]

    @property
    def icon_animated(self):
        return bool(self.icon and self.icon.startswith('a_'))

    @property
    def icon_url(self):
        return self.icon_url_as()

    def icon_url_as(self, *, format=None, static_format='webp', size=1024):
        if self.icon is None:
            return None

        if format is None:
            if self.icon_animated:
                format = "gif"

            else:
                format = static_format

        return DISCORD_CDN + "/icons/{0.id}/{0.icon}.{1}?size={2}".format(self, format, size)

    @property
    def splash_url(self):
        return None


class Message(Entity):
    def _preprocess(self, data):
        self.type = MessageType(data["type"])
        self.timestamp = parse_time(data["timestamp"])
        # self.mentions
        # self.mention_roles
        # self.mention_everyone
        self.author = Member({"user": data["author"], **data.get("member", {})})
        self.member = self.author
        self.edited_timestamp = parse_time(data["edited_timestamp"])
        # self.attachments