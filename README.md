# Anki Converter
Convert from Markdown-esque to Anki-compatible CSV

## Format:
Format was borrowed from Markdown

---

From:
```
# Main Topic

## Subtopic
* question 1
  + answer 1

## Other tag
* question 2
  + answer 2
* question 3
  + answer 3
```
To:
```
tags:Main_Topic
question1;answer1;Subtopic
question2;answer2;Other_tag
question3;answer3;Other_tag
```

## Usage
`python -m anki_converter file1.md file2.md`