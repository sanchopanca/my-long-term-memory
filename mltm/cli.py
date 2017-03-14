import os
import subprocess
import tempfile

from mltm.models import Entry


def get_editor():
    return os.environ.get("VISUAL") or os.environ.get("EDITOR", "vi")


def add_entry():
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    subprocess.run([get_editor(), f.name])

    for _ in (1,):  # Now we can use break
        with open(f.name) as f:
            lines = f.readlines()
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip() == '':
                    lines.pop(i)
            if len(lines) < 3:
                print('Adding new entry was aborted')
                break
            title = lines[0].strip()
            text = ''.join(lines[1:-1])
            text = text.strip()
            tags = [tag.strip() for tag in lines[-1].split(',')]
            Entry.add_entry(title, text, tags)
    os.remove(f.name)


def show_entries(search_string=None):
    if search_string:
        entries = Entry.search_arbitrary_text(search_string)
    else:
        entries = Entry.get_all()
    delimiter = '─' * 42 + '\n'
    print(delimiter.join((entry.display() for entry in entries)))
