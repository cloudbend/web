from string import Template
from pathlib import Path

TMPL_DIR = Path(__file__).parent

with open(TMPL_DIR / "contact.html", "r") as html:
    content = html.read()
    CONTACT_TEMPLATE = Template(content)
