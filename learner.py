import json
import os

from collections import defaultdict

from datetime import datetime

from zoneinfo import ZoneInfo


MEMORY_FILE = "memory.json"

IST = ZoneInfo(
    "Asia/Kolkata"
)


def empty_memory():

    return {

        "reminder_history": [],

        "patterns": [],

        "pattern_notifications": []
    }


def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):

        return empty_memory()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory = json.load(
                file
            )

        if "reminder_history" not in memory:
            memory["reminder_history"] = []

        if "patterns" not in memory:
            memory["patterns"] = []

        if "pattern_notifications" not in memory:
            memory["pattern_notifications"] = []

        return memory

    except Exception:

        return empty_memory()


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def normalize_task(task):

    task = task.lower().strip()

    replacements = {

        "mathematics": "math",

        "mathematics class": "math class",

        "study mathematics": "math",

        "revision of mathematics": "math revision",

        "social science": "sst",

        "computer class": "computer"
    }

    return replacements.get(
        task,
        task
    )


def record_reminder(
    task,
    reminder_time
):

    memory = load_memory()

    entry = {

        "task": task,

        "normalized_task":
            normalize_task(task),

        "time":
            reminder_time.strftime(
                "%H:%M"
            ),

        "date":
            reminder_time.strftime(
                "%Y-%m-%d"
            ),

        "weekday":
            reminder_time.strftime(
                "%A"
            ),

        "created_at":
            datetime.now(
                IST
            ).isoformat()
    }

    memory[
        "reminder_history"
    ].append(
        entry
    )

    memory[
        "reminder_history"
    ] = memory[
        "reminder_history"
    ][-500:]

    save_memory(
        memory
    )

    detect_patterns()


def detect_patterns():

    memory = load_memory()

    history = memory.get(
        "reminder_history",
        []
    )

    groups = defaultdict(list)

    for entry in history:

        key = (

            entry[
                "normalized_task"
            ],

            entry[
                "time"
            ]
        )

        groups[key].append(
            entry
        )

    patterns = []

    for (
        task,
        reminder_time
    ), entries in groups.items():

        count = len(
            entries
        )

        if count < 3:
            continue

        weekdays = sorted(
            set(
                entry[
                    "weekday"
                ]
                for entry in entries
            )
        )

        patterns.append({

            "task": task,

            "time": reminder_time,

            "occurrences": count,

            "weekdays": weekdays
        })

    memory[
        "patterns"
    ] = patterns

    save_memory(
        memory
    )

    return patterns


def get_patterns():

    memory = load_memory()

    return memory.get(
        "patterns",
        []
    )


def find_pattern_for_time(
    current_time
):

    patterns = get_patterns()

    current_time_string = (
        current_time.strftime(
            "%H:%M"
        )
    )

    matches = []

    for pattern in patterns:

        if pattern[
            "time"
        ] == current_time_string:

            matches.append(
                pattern
            )

    return matches


def was_pattern_notified_today(
    task,
    reminder_time
):

    memory = load_memory()

    today = reminder_time.strftime(
        "%Y-%m-%d"
    )

    normalized = normalize_task(
        task
    )

    for entry in memory.get(
        "pattern_notifications",
        []
    ):

        if (

            entry[
                "normalized_task"
            ] == normalized

            and

            entry[
                "date"
            ] == today

            and

            entry[
                "time"
            ] == reminder_time.strftime(
                "%H:%M"
            )

        ):

            return True

    return False


def record_pattern_notification(
    task,
    reminder_time
):

    memory = load_memory()

    entry = {

        "task": task,

        "normalized_task":
            normalize_task(task),

        "time":
            reminder_time.strftime(
                "%H:%M"
            ),

        "date":
            reminder_time.strftime(
                "%Y-%m-%d"
            ),

        "created_at":
            datetime.now(
                IST
            ).isoformat()
    }

    memory[
        "pattern_notifications"
    ].append(
        entry
    )

    memory[
        "pattern_notifications"
    ] = memory[
        "pattern_notifications"
    ][-200:]

    save_memory(
        memory
    )


def get_learning_summary():

    memory = load_memory()

    return {

        "history_count":
            len(
                memory.get(
                    "reminder_history",
                    []
                )
            ),

        "pattern_count":
            len(
                memory.get(
                    "patterns",
                    []
                )
            ),

        "patterns":
            memory.get(
                "patterns",
                []
            )
    }