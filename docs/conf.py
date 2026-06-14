# docs/conf.py
# wamp-proto documentation configuration - modernized for 2025
import os
import time

# -- Project information -----------------------------------------------------
project = "WAMP"
author = "The WAMP/Autobahn/Crossbar.io OSS Project"
this_year = time.strftime('%Y')
if this_year != '2012':
    copyright = f"2012-{this_year}, typedef int GmbH (Germany)"
else:
    copyright = "2012, typedef int GmbH (Germany)"

# The short X.Y version
version = "version 2"
release = version
language = "en"

# -- General configuration ---------------------------------------------------
extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",

    # Modern UX extensions
    "sphinx_design",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinxcontrib.images",
    "sphinxcontrib.spelling",
]

# Source file suffixes
source_suffix = ".rst"

# The master toctree document
master_doc = "index"

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "_work", "_design"]

# -- sphinxcontrib-images Configuration --------------------------------------
images_config = {
    "override_image_directive": False,
}

# -- Spelling Configuration --------------------------------------------------
spelling_lang = "en_US"
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_show_suggestions = True

# -- HTML Output (Furo Theme) ------------------------------------------------
html_theme = "furo"
html_title = f"{project} {release}"

# Furo theme options with Noto fonts and WAMP subarea colors
html_theme_options = {
    # Source repository links
    "source_repository": "https://github.com/wamp-proto/wamp-proto/",
    "source_branch": "master",
    "source_directory": "docs/",

    # Noto fonts and WAMP Dark Anthracite (#1a1a1a) accent color
    "light_css_variables": {
        "font-stack": "'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font-stack--monospace": "'Noto Sans Mono', SFMono-Regular, Menlo, Consolas, monospace",
        "color-brand-primary": "#1a1a1a",
        "color-brand-content": "#1a1a1a",
    },
    "dark_css_variables": {
        "font-stack": "'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font-stack--monospace": "'Noto Sans Mono', SFMono-Regular, Menlo, Consolas, monospace",
        "color-brand-primary": "#e0e0e0",
        "color-brand-content": "#e0e0e0",
    },
}

# Logo and favicon (optimized from docs/_graphics/ by `just optimize-images`)
html_logo = "_static/img/wamp_logo.svg"
html_favicon = "_static/img/favicon.ico"

# Static files
html_static_path = ["_static"]
html_css_files = [
    # Load Noto fonts from Google Fonts
    "https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Noto+Sans+Mono:wght@400;500&display=swap",
]

# -- Syntax Highlighting -----------------------------------------------------
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# -- OpenGraph (Social Media Meta Tags) -------------------------------------
ogp_site_url = "https://wamp-proto.org/"

# -- Miscellaneous -----------------------------------------------------------
todo_include_todos = True
autosectionlabel_prefix_document = True
