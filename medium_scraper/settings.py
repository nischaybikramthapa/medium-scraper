"""All the default setting go here"""

from dateutil import tz

DT_FORMAT = "%Y-%m-%d"
LOCAL_TZ = tz.gettz("Australia/Melbourne")

TITLE_ELEMENTS = {
    "h3": [
        "graf graf--h3 graf-after--figure graf--title",
        "graf graf--h3 graf-after--figure graf--trailing graf--title",
        "graf graf--h3 graf--leading graf--title",
        "graf graf--h3 graf--startsWithDoubleQuote graf--leading graf--title",
        "graf graf--h3 graf--startsWithDoubleQuote graf-after--figure graf--trailing graf--title",
    ],
    "h4": "graf graf--h4 graf--leading",
    "p": "graf graf--p graf--leading",
}


SUBTITLE_ELEMENTS = {
    "h4": [
        "graf graf--h4 graf-after--h3 graf--subtitle",
        "graf graf--h4 graf-after--h3 graf--trailing graf--subtitle",
        "graf graf--p graf-after--h3 graf--trailing",
    ],
    "strong": "markup--strong markup--p-strong",
    "p": [
        "graf graf--p graf-after--h3 graf--trailing",
        "graf graf--p graf-after--figure",
        "graf graf--p graf-after--figure graf--trailing",
        "graf graf--p graf-after--p graf--trailing",
    ],
    "blockquote": [
        "graf graf--pullquote graf-after--figure graf--trailing",
        "graf graf--blockquote graf-after--h3 graf--trailing",
    ],
    "em": "markup--em markup--p-em",
}
