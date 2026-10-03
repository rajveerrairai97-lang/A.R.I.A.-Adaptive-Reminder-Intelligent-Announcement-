import json
import os

from datetime import (
    datetime,
    date,
    timedelta
)

from zoneinfo import ZoneInfo


DEADLINES_FILE = "deadlines.json"

IST = ZoneInfo(
    "Asia/Kolkata"
)


def load_deadlines():

    if not os.path.exists(
        DEADLINES_FILE
    ):

        return []

    try:

        with open(
            DEADLINES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return []


def save_deadlines(
    deadlines
):

    with open(
        DEADLINES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            deadlines,
            file,
            indent=4,
            ensure_ascii=False
        )


def parse_deadline_date(
    date_input
):

    date_input = (
        date_input
        .strip()
        .lower()
    )

    formats = [

        "%d-%m-%Y",

        "%d/%m/%Y",

        "%d.%m.%Y",

        "%d %B %Y",

        "%d %b %Y",

        "%d %B",

        "%d %b"
    ]

    for fmt in formats:

        try:

            parsed = datetime.strptime(
                date_input,
                fmt
            )

            # If year wasn't entered,
            # use the current year.
            if "%Y" not in fmt:

                current_year = datetime.now(
                    IST
                ).year

                parsed = parsed.replace(
                    year=current_year
                )

                # If the date has already
                # passed this year, assume
                # the next year.
                today = datetime.now(
                    IST
                ).date()

                if parsed.date() < today:

                    parsed = parsed.replace(
                        year=current_year + 1
                    )

            return parsed.date()

        except ValueError:

            continue

    raise ValueError(
        "Invalid date"
    )


def add_deadline(
    task,
    deadline_date
):

    deadlines = load_deadlines()

    deadline = {

        "task": task,

        "date":
            deadline_date.isoformat(),

        "day_before_sent": False,

        "due_today_sent": False,

        "completed": False,

        "created_at":
            datetime.now(
                IST
            ).isoformat()
    }

    deadlines.append(
        deadline
    )

    save_deadlines(
        deadlines
    )

    return deadline


def get_deadlines():

    return load_deadlines()


def get_active_deadlines():

    deadlines = load_deadlines()

    return [

        deadline

        for deadline in deadlines

        if not deadline.get(
            "completed",
            False
        )
    ]


def check_deadlines():

    """
    Returns deadline events that need notification.

    day_before:
        Deadline is tomorrow.

    due_today:
        Deadline is today.
    """

    deadlines = load_deadlines()

    today = datetime.now(
        IST
    ).date()

    events = []

    changed = False

    for deadline in deadlines:

        if deadline.get(
            "completed",
            False
        ):

            continue

        try:

            deadline_date = date.fromisoformat(
                deadline[
                    "date"
                ]
            )

        except Exception:

            continue

        one_day_before = (
            deadline_date
            - timedelta(
                days=1
            )
        )

        if (

            today == one_day_before

            and

            not deadline.get(
                "day_before_sent",
                False
            )

        ):

            events.append({

                "type": "day_before",

                "task":
                    deadline[
                        "task"
                    ],

                "date":
                    deadline_date,

                "deadline":
                    deadline
            })

            deadline[
                "day_before_sent"
            ] = True

            changed = True

        elif (

            today == deadline_date

            and

            not deadline.get(
                "due_today_sent",
                False
            )

        ):

            events.append({

                "type": "due_today",

                "task":
                    deadline[
                        "task"
                    ],

                "date":
                    deadline_date,

                "deadline":
                    deadline
            })

            deadline[
                "due_today_sent"
            ] = True

            changed = True

    if changed:

        save_deadlines(
            deadlines
        )

    return events


def mark_completed(
    index
):

    deadlines = load_deadlines()

    if (
        index < 0
        or
        index >= len(deadlines)
    ):

        return False

    deadlines[
        index
    ][
        "completed"
    ] = True

    save_deadlines(
        deadlines
    )

    return True


def days_remaining(
    deadline
):

    try:

        deadline_date = date.fromisoformat(
            deadline[
                "date"
            ]
        )

        today = datetime.now(
            IST
        ).date()

        return (
            deadline_date
            - today
        ).days

    except Exception:

        return None