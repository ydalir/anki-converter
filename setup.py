import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="anki_converter",
    version="0.0.1",
    description="Convert from Markdown-esque to Anki-compatible CSV",
    long_description=long_description
)