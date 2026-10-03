import json
import subprocess
import base64

from winotify import Notification, audio


CONFIG_FILE = "config.json"


def load_config():
    try:
        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception:
        return {
            "assistant_name": "JARVIS",
            "user_title": "sir",
            "voice_enabled": True,
            "notification_enabled": True,
            "voice_rate": 165
        }


config = load_config()


def speak_with_windows(text):
    """
    Use Windows PowerShell + Microsoft David
    directly through Windows Speech.
    """

    escaped_text = text.replace(
        "'",
        "''"
    )

    powershell_script = f'''
Add-Type -AssemblyName System.Speech

$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer

$voiceFound = $false

foreach ($voice in $speaker.GetInstalledVoices()) {{
    if ($voice.VoiceInfo.Name -like "*David*") {{
        $speaker.SelectVoice($voice.VoiceInfo.Name)
        $voiceFound = $true
        break
    }}
}}

if (-not $voiceFound) {{
    Write-Host "DAVID VOICE NOT FOUND"
}}

$speaker.Rate = 0
$speaker.Volume = 100

$speaker.Speak('{escaped_text}')

$speaker.Dispose()
'''

    encoded = base64.b64encode(
        powershell_script.encode("utf-16le")
    ).decode("ascii")

    try:

        print(
            "   🔊 Starting Windows David voice..."
        )

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-EncodedCommand",
                encoded
            ],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.stdout.strip():
            print(
                "   [VOICE]",
                result.stdout.strip()
            )

        if result.stderr.strip():
            print(
                "   [VOICE ERROR]",
                result.stderr.strip()
            )

        if result.returncode == 0:

            print(
                "   ✅ JARVIS voice finished."
            )

        else:

            print(
                f"   ❌ Voice process exited with code "
                f"{result.returncode}"
            )

    except Exception as error:

        print(
            f"   ❌ WINDOWS VOICE ERROR: {error}"
        )


def speak(text):

    if not config.get(
        "voice_enabled",
        True
    ):

        print(
            "[VOICE] Voice is disabled."
        )

        return

    print()
    print(
        "🔊 JARVIS SPEAKING:"
    )
    print(
        f"   {text}"
    )

    speak_with_windows(text)


def get_voices():

    try:

        import pyttsx3

        engine = pyttsx3.init(
            driverName="sapi5"
        )

        voices = engine.getProperty(
            "voices"
        )

        engine.stop()

        return voices

    except Exception:

        return []


def show_available_voices():

    voices = get_voices()

    print()
    print(
        "=" * 70
    )
    print(
        "AVAILABLE WINDOWS VOICES"
    )
    print(
        "=" * 70
    )

    if not voices:

        print(
            "No voices detected."
        )

        return

    for index, voice in enumerate(
        voices
    ):

        print()
        print(
            f"{index}: {voice.name}"
        )

        print(
            f"   ID: {voice.id}"
        )

    print()
    print(
        "=" * 70
    )


def show_notification(
    title,
    message
):

    if not config.get(
        "notification_enabled",
        True
    ):

        return

    try:

        notification = Notification(
            app_id="JARVIS Notification Engine",
            title=title,
            msg=message
        )

        notification.set_audio(
            audio.Default,
            loop=False
        )

        notification.show()

    except Exception as error:

        print(
            f"[NOTIFICATION ERROR] {error}"
        )


def notify(
    message,
    title="🔷 JARVIS"
):

    print()

    print(
        "╔" + "═" * 58 + "╗"
    )

    print(
        "║"
        + "  🔷 JARVIS NOTIFICATION"
        .ljust(58)
        + "║"
    )

    print(
        "╠" + "═" * 58 + "╣"
    )

    words = message.split()

    lines = []

    current = ""

    for word in words:

        if len(current) + len(word) + 1 <= 54:

            current += (
                (" " if current else "")
                + word
            )

        else:

            lines.append(
                current
            )

            current = word

    if current:
        lines.append(
            current
        )

    for line in lines:

        print(
            "║ "
            + line.ljust(56)
            + "║"
        )

    print(
        "╚" + "═" * 58 + "╝"
    )

    show_notification(
        title,
        message
    )

    speak(
        message
    )


if __name__ == "__main__":

    print()

    print(
        "╔" + "═" * 58 + "╗"
    )

    print(
        "║"
        + "      🤖 JARVIS WINDOWS VOICE TEST"
        .center(58)
        + "║"
    )

    print(
        "╚" + "═" * 58 + "╝"
    )

    print()

    print(
        "Testing Microsoft David..."
    )

    speak(
        "Good evening, sir. "
        "This is JARVIS. "
        "Microsoft David is connected directly "
        "to the Windows speech system."
    )

    print()

    print(
        "🔷 Voice test complete."
    )