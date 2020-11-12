#!/usr/bin/env python3


import adhesive
import os
from adhesive.workspace import docker


@adhesive.lane("local")
def lane_default(context):
    context.workspace.pwd = os.getcwd()
    yield context.workspace


@adhesive.task("Render AsciiDoc to DocBook")
def convert_asciidoc_to_docbook(context):
    with docker.inside(context.workspace, "bmst/docker-asciidoctor") as dw:
        dw.run(
            """
            asciidoctor -b docbook -o README.docbook.xml README.adoc
        """
        )


@adhesive.task("Render AsciiDoc to PDF")
def render_asciidot_to_pdf(context):
    with docker.inside(context.workspace, "bmst/docker-asciidoctor") as dw:
        dw.run(
            """
            asciidoctor-pdf -o README.pdf README.adoc
        """
        )


@adhesive.task("Convert DocBook to Markdown")
def convert_docbook_to_markdown(context):
    with docker.inside(context.workspace, "bmst/pandoc") as dw:
        dw.run(
            """
            pandoc --from docbook --to markdown_strict README.docbook.xml -o README.md
        """
        )


@adhesive.task("Convert DocBook to ReStructuredText")
def convert_docbook_to_restructuredtext(context):
    with docker.inside(context.workspace, "bmst/pandoc") as dw:
        dw.run(
            """
            pandoc --reference-links --from docbook --to rst README.docbook.xml -o README.rst
        """
        )


@adhesive.task("Validate ReStructuredText")
def validate_restructuredtext(context):
    with docker.inside(context.workspace, "bmst/python-rst-validator") as dw:
        dw.run(
            """
            python -m readme_renderer README.rst -o /dev/null
        """
        )


@adhesive.task("Remove DocBook documentation")
def remove_docbook_documentation(context):
    context.workspace.run(
        """
        rm README.docbook.xml
    """
    )


adhesive.process_start().subprocess_start(
    "Render Documents", lane="local"
).branch_start().task(
    "Render AsciiDoc to DocBook", lane="local"
).branch_end().branch_start().task(
    "Render AsciiDoc to PDF", lane="local"
).branch_end().subprocess_end().subprocess_start(
    "Convert Documents", lane="local"
).branch_start().task(
    "Convert DocBook to Markdown", lane="local"
).branch_end().branch_start().task(
    "Convert DocBook to ReStructuredText", lane="local"
).task(
    "Validate ReStructuredText", lane="local"
).branch_end().subprocess_end().task(
    "Remove DocBook documentation", lane="local"
).process_end().build()
