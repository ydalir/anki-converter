import re
import csv

def convert_to_topic(text: str):
    # Convert spaces to underscore and remove invalid characters
    # Valid characters are a-z A-Z 0-9 and _
    return re.sub(r'[^\w ]', '', text) \
        .strip() \
        .replace(" ", "_")

class Deck:
    def __init__(self) -> None:
        # Main topic, all cards are tagged with this
        self.topic = None

        # Cards are grouped by tags
        # Each card in a tag group has the same tag applied
        self.tags = []

    def parse(self, text: str):
        text = self.normalize_whitespace(text)
        self.topic, text = self.extract_topic(text)

        self.tags = self.get_tags(text)

    def extract_topic(self, text: str):
        # Get topic
        # Topic is the first h1 headline, marked by '# '
        pattern = re.compile(r'^# (.*$)', re.MULTILINE)
        result = pattern.search(text)
        if result:
            topic = convert_to_topic(result.group(1))
            span = result.span()
            # Return text with topic removed
            return (topic, text[:span[0]] + text[span[1]:])

        # If no topic is found, return text
        return (None, text)

    def get_tags(self, text) -> None:
        rows = []
        # Splits text by tag
        # Tags are h2 headlines, marked by "## "
        tags = [Tag(txt).get_cards() for txt in text.split("## ")[1:]]
        for tag in tags:
            for row in tag:
                rows.append(row)
        
        return rows

    def normalize_whitespace(self, text: str):
        # Replace tabs with two spaces
        normalized = text.replace("\t", "  ")
        return normalized
    
    def write(self, filename: str):
        # Clears file if it already exists, writes tag at top of file
        with open(filename, 'w') as f:
            if self.topic:
                f.write(f"tags:{self.topic}\n")
            else:
                f.write("")

        self.write_csv(filename)
    
    def write_csv(self, filename: str):
        # Appends CSV formatted data to file
        with open(filename, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerows(self.tags)

class Tag:
    def __init__(self, text: str) -> None:
        self.topic = None
        self.cards = []

        self.parse(text)
    
    def parse(self, text: str):
        # Text is split by "## " topic marker before being sent to this function
        # Topic must be at the start of the string
        # Pattern gets all characters until first card marker
        topic_pattern = re.compile(r'[^*+-]*', re.S)
        self.topic = convert_to_topic(topic_pattern.match(text).group())

        # Cards are marked with "* " "- " or "+ "
        # First marker is the front, second marker is the back
        card_pattern = re.compile(r'[*+-] ([^*+-]*)[*+-] ([^*+-]*)', re.S)
        cards = card_pattern.findall(text)

        # Removes excess whitespace
        self.cards = [(strip(q), strip(a)) for q, a in cards]
    
    def get_cards(self):
        # Adds tag to each card if topic is set
        if self.topic:
            return [[q, a, self.topic] for q, a in self.cards]

        return [[q, a] for q, a in self.cards]

def strip(text: str):
    return " ".join([line.strip() for line in text.split("\n") if line.strip()])
