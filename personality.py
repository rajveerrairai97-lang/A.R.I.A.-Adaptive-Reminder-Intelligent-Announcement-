import random

from datetime import datetime

from zoneinfo import ZoneInfo


IST = ZoneInfo(
    "Asia/Kolkata"
)


STUDY_TEMPLATES = [

    "Good {time_of_day}, sir. It appears you have successfully postponed {task} until the last possible moment. Your revision session is now due.",

    "Good {time_of_day}, sir. {task} has requested your attention. I suggest we finally give it some.",

    "Good {time_of_day}, sir. Your {task} revision session is now due. I shall assume the procrastination phase has concluded.",

    "Good {time_of_day}, sir. The scheduled {task} revision has arrived. Fortunately, I remembered. You are welcome.",

    "Good {time_of_day}, sir. It is time for {task}. I recommend beginning before the textbook starts judging us.",

    "Good {time_of_day}, sir. Your {task} session is due. Shall we pretend this was part of the master plan?"
]


CLASS_TEMPLATES = [

    "Good {time_of_day}, sir. Your {task} is scheduled now. I suggest attending before the teacher begins wondering where you are.",

    "Sir, it is time for {task}. Yes, apparently education continues to exist.",

    "Your {task} is due, sir. Your calendar has spoken, and unfortunately it appears to be correct.",

    "Good {time_of_day}, sir. You have {task} now. I recommend being there physically as well as spiritually.",

    "Sir, it is time for {task}. I have detected a recurring pattern here. Apparently you actually do this regularly."
]


PROJECT_TEMPLATES = [

    "Sir, your {task} session is now due. The code is unlikely to write itself, despite my repeated requests.",

    "Good {time_of_day}, sir. It is time for {task}. I suggest we make some progress before the bugs reproduce.",

    "Sir, your {task} session has arrived. The machines await their instructions.",

    "Your {task} is due, sir. Shall we create something unnecessarily impressive again?"
]


GENERAL_TEMPLATES = [

    "Good {time_of_day}, sir. Your reminder for {task} is now due.",

    "Good {time_of_day}, sir. You asked me to remind you about {task}. Consider yourself reminded.",

    "Good {time_of_day}, sir. It is time for {task}.",

    "Good {time_of_day}, sir. Your scheduled task, {task}, is now due.",

    "Good {time_of_day}, sir. {task} requires your attention."
]


DEADLINE_TEMPLATES = [

    "Sir, your {task} deadline is approaching. It is due on {date}. I thought I would mention it before time becomes inconvenient.",

    "Good {time_of_day}, sir. Your {task} is due on {date}. The deadline has officially entered the danger zone.",

    "Sir, your {task} deadline is approaching. You still have time, which is considerably better than having an excuse.",

    "Good {time_of_day}, sir. {task} is due on {date}. I recommend dealing with it before tomorrow becomes today."
]


DEADLINE_TODAY_TEMPLATES = [

    "Sir, your {task} is due today. I recommend treating this as a deadline rather than a philosophical suggestion.",

    "Good {time_of_day}, sir. Today is the deadline for {task}. The clock has become rather interested in your progress.",

    "Sir, {task} is due today. This would be an excellent time to stop negotiating with time.",

    "Good {time_of_day}, sir. Your {task} deadline has arrived. I trust we have not relied entirely on optimism."
]


SARCASM_MESSAGES = [

    "Excellent planning, sir. Almost suspiciously competent.",

    "Remarkable. You remembered something before it became an emergency.",

    "A surprisingly responsible decision, sir. I shall document this historic event.",

    "Well done, sir. The procrastination department will be disappointed.",

    "Efficient, organized, and on time. I may need to update my expectations.",

    "Sir, I detect productivity. Should I alert the authorities?"
]


LATE_MESSAGES = [

    "Sir, it is rather late. You did schedule this reminder yourself, so I shall refrain from judging.",

    "Sir, it is quite late. I admire your commitment to making tomorrow's problem today's problem.",

    "It is late, sir. I would recommend sleep, but apparently we have other plans.",

    "Sir, the clock strongly suggests that this could have been done earlier."
]


def get_time_of_day():

    hour = datetime.now(
        IST
    ).hour

    if 5 <= hour < 12:
        return "morning"

    if 12 <= hour < 17:
        return "afternoon"

    if 17 <= hour < 21:
        return "evening"

    return "night"


def is_study_task(task):

    keywords = [

        "physics",
        "chemistry",
        "biology",
        "math",
        "mathematics",
        "sst",
        "social science",
        "history",
        "geography",
        "civics",
        "economics",
        "english",
        "hindi",
        "revision",
        "study",
        "homework",
        "test",
        "exam"
    ]

    task_lower = task.lower()

    return any(
        keyword in task_lower
        for keyword in keywords
    )


def is_class_task(task):

    keywords = [

        "class",
        "coaching",
        "school",
        "tuition",
        "lecture"
    ]

    task_lower = task.lower()

    return any(
        keyword in task_lower
        for keyword in keywords
    )


def is_project_task(task):

    keywords = [

        "project",
        "coding",
        "code",
        "programming",
        "github",
        "python",
        "jarvis"
    ]

    task_lower = task.lower()

    return any(
        keyword in task_lower
        for keyword in keywords
    )


def generate_reminder(task):

    time_of_day = get_time_of_day()

    if is_class_task(task):

        template = random.choice(
            CLASS_TEMPLATES
        )

    elif is_project_task(task):

        template = random.choice(
            PROJECT_TEMPLATES
        )

    elif is_study_task(task):

        template = random.choice(
            STUDY_TEMPLATES
        )

    else:

        template = random.choice(
            GENERAL_TEMPLATES
        )

    return template.format(
        time_of_day=time_of_day,
        task=task
    )


def generate_learned_pattern_message(
    task,
    reminder_time,
    occurrences
):

    time_string = reminder_time.strftime(
        "%H:%M"
    )

    time_of_day = get_time_of_day()

    messages = [

        f"Good {time_of_day}, sir. My records show that you usually have {task} around {time_string}. I believe we have discovered a pattern.",

        f"Sir, your historical reminders indicate {task} at {time_string} is becoming a regular event. I have reminded you before you could forget.",

        f"Good {time_of_day}, sir. You have scheduled {task} at {time_string} repeatedly. After {occurrences} observations, I have decided this is no longer a coincidence.",

        f"Sir, pattern detected. {task} usually occurs at {time_string}. Apparently I am now responsible for remembering your routine as well.",

        f"Good {time_of_day}, sir. You normally have {task} at {time_string}. I thought I would mention it before your memory module decided to take the evening off."
    ]

    return random.choice(
        messages
    )


def generate_deadline_message(
    task,
    deadline_date
):

    date_string = deadline_date.strftime(
        "%d %B %Y"
    )

    time_of_day = get_time_of_day()

    template = random.choice(
        DEADLINE_TEMPLATES
    )

    return template.format(
        time_of_day=time_of_day,
        task=task,
        date=date_string
    )


def generate_deadline_today_message(
    task
):

    time_of_day = get_time_of_day()

    template = random.choice(
        DEADLINE_TODAY_TEMPLATES
    )

    return template.format(
        time_of_day=time_of_day,
        task=task
    )


def generate_sarcastic_message():

    return random.choice(
        SARCASM_MESSAGES
    )


def generate_late_message():

    return random.choice(
        LATE_MESSAGES
    )


def generate_battery_message(level):

    if level <= 10:

        messages = [

            f"Sir, battery levels are at {level}%. I strongly recommend finding a charger before this laptop enters an unscheduled retirement.",

            f"Sir, we are now operating on {level}% battery. This seems like an excellent time to locate a power source.",

            f"Battery level: {level}%, sir. I would describe the situation as mildly concerning."
        ]

    elif level <= 20:

        messages = [

            f"Sir, battery levels have fallen to {level}%. A charger would be a remarkably sensible investment at this point.",

            f"Sir, the battery is currently at {level}%. Your laptop would appreciate some electricity.",

            f"Battery level is {level}%, sir. I recommend introducing it to a charger."
        ]

    else:

        messages = [

            f"Sir, battery level is currently {level}%.",

            f"Battery status: {level}%, sir."
        ]

    return random.choice(
        messages
    )


def generate_startup_message():

    messages = [

        "Good evening, sir. All systems are online.",

        "Systems initialized, sir. I am ready.",

        "Good to see you again, sir. Notification systems are online.",

        "All systems operational, sir. Try not to create unnecessary emergencies.",

        "JARVIS notification engine initialized. I am at your service, sir."
    ]

    return random.choice(
        messages
    )