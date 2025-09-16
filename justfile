# -----------------------------------------------------------------------------
# -- just global configuration
# -----------------------------------------------------------------------------

set unstable := true
set positional-arguments := true
set script-interpreter := ['uv', 'run', '--script']

# uv env vars
# see: https://docs.astral.sh/uv/reference/environment/

# project base directory = directory of this justfile
PROJECT_DIR := justfile_directory()

# Default recipe: list all recipes
default:
    @echo ""
    @echo "Web Application Messaging Protocol (WAMP)"
    @echo ""
    @just --list
    @echo ""

# Tell uv to always copy files instead of trying to hardlink them.
# set export UV_LINK_MODE := 'copy'

# Tell uv to use project-local cache directory.
export UV_CACHE_DIR := './.uv-cache'

# Use this common single directory for all uv venvs.
VENV_DIR := './.venvs'

# Define a justfile-local variable for our environments.
ENVS := 'cpy314 cpy313 cpy312 cpy311 cpy310 pypy311 pypy310'

# internal helper to map Python version short name to full uv version
_get-spec short_name:
    #!/usr/bin/env bash
    set -e
    case {{short_name}} in
        cpy314)  echo "cpython-3.14";;
        cpy313)  echo "cpython-3.13";;
        cpy312)  echo "cpython-3.12";;
        cpy311)  echo "cpython-3.11";;
        cpy310)  echo "cpython-3.10";;
        pypy311) echo "pypy-3.11";;
        pypy310) echo "pypy-3.10";;
        *)       echo "Unknown environment: {{short_name}}" >&2; exit 1;;
    esac

# Internal helper that calculates and prints the system-matching venv name.
_get-system-venv-name:
    #!/usr/bin/env bash
    set -e
    SYSTEM_VERSION=$(/usr/bin/python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    ENV_NAME="cpy$(echo ${SYSTEM_VERSION} | tr -d '.')"

    if ! echo "{{ ENVS }}" | grep -q -w "${ENV_NAME}"; then
        echo "Error: System Python (${SYSTEM_VERSION}) maps to '${ENV_NAME}', which is not a supported environment in this project." >&2
        exit 1
    fi
    # The only output of this recipe is the name itself.
    echo "${ENV_NAME}"

# -----------------------------------------------------------------------------
# -- General/global helper recipes
# -----------------------------------------------------------------------------

# Bootstrap repository after cloning
setup-githooks:
    #!/usr/bin/env bash
    set -e

    # Configure Git to use the versioned hooks directory
    git config core.hooksPath .githooks
    echo "✔ Git hooks are now configured to use .githooks/"
    echo "  (run 'git config core.hooksPath' to verify)"

# Setup bash tab completion for the current user (to activate: `source ~/.config/bash_completion`).
setup-completion:
    #!/usr/bin/env bash
    set -e

    COMPLETION_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion"
    MARKER="# --- Just completion ---"

    echo "==> Setting up bash tab completion for 'just'..."

    # Check if we have already configured it.
    if [ -f "${COMPLETION_FILE}" ] && grep -q "${MARKER}" "${COMPLETION_FILE}"; then
        echo "--> 'just' completion is already configured."
        exit 0
    fi

    echo "--> Configuration not found. Adding it now..."

    # 1. Ensure the directory exists.
    mkdir -p "$(dirname "${COMPLETION_FILE}")"

    # 2. Add our marker comment to the file.
    echo "" >> "${COMPLETION_FILE}"
    echo "${MARKER}" >> "${COMPLETION_FILE}"

    # 3. CRITICAL: Run `just` and append its raw output directly to the file.
    #    No `echo`, no `eval`, no quoting hell. Just run and redirect.
    just --completions bash >> "${COMPLETION_FILE}"

    echo "--> Successfully added completion logic to ${COMPLETION_FILE}."

    echo ""
    echo "==> Setup complete. Please restart your shell or run the following command:"
    echo "    source \"${COMPLETION_FILE}\""

# Remove ALL generated files, including venvs, caches, and build artifacts. WARNING: This is a destructive operation.
distclean:
    #!/usr/bin/env bash
    set -e

    echo "==> Performing a deep clean (distclean)..."

    # 1. Remove top-level directories known to us.
    #    This is fast for the common cases.
    echo "--> Removing venvs, cache, and build/dist directories..."
    rm -rf {{UV_CACHE_DIR}} {{VENV_DIR}} build/ dist/ .pytest_cache/ .ruff_cache/ .mypy_cache/

    # 2. Use `find` to hunt down and destroy nested artifacts that can be
    #    scattered throughout the source tree. This is the most thorough part.
    echo "--> Searching for and removing nested Python caches..."
    find . -type d -name "__pycache__" -exec rm -rf {} +

    echo "--> Searching for and removing compiled Python files..."
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete

    echo "--> Searching for and removing setuptools egg-info directories..."
    find . -type d -name "*.egg-info" -exec rm -rf {} +

    echo "--> Searching for and removing coverage data..."
    rm -f .coverage
    find . -type f -name ".coverage.*" -delete

    echo "==> Distclean complete. The project is now pristine."

# -----------------------------------------------------------------------------
# -- Python virtual environments
# -----------------------------------------------------------------------------

# List all Python virtual environments
list-all:
    #!/usr/bin/env bash
    set -e
    echo
    echo "Available Python run-times:"
    echo "==========================="
    echo
    uv python list
    echo
    echo "Mapped Python run-time shortname => full version:"
    echo "================================================="
    echo
    # This shell loop correctly uses a SHELL variable ($env), not a just variable.
    for env in {{ENVS}}; do
        # We call our helper recipe to get the spec for the current env.
        # The `--quiet` flag is important to only capture the `echo` output.
        spec=$(just --quiet _get-spec "$env")
        echo "  - $env => $spec"
    done
    echo
    echo "Create a Python venv using: just create <shortname>"

# Create a single Python virtual environment (usage: `just create cpy314` or `just create`)
create venv="":
    #!/usr/bin/env bash
    set -e

    VENV_NAME="{{ venv }}"

    # This is the "default parameter" logic.
    # If VENV_NAME is empty (because `just create` was run), calculate the default.
    if [ -z "${VENV_NAME}" ]; then
        echo "==> No venv name specified. Auto-detecting from system Python..."
        VENV_NAME=$(just --quiet _get-system-venv-name)
        echo "==> Defaulting to venv: '${VENV_NAME}'"
    fi

    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    # Only create the venv if it doesn't already exist
    if [ ! -d "${VENV_PATH}" ]; then
        # Get the Python spec just-in-time
        PYTHON_SPEC=$(just --quiet _get-spec "${VENV_NAME}")

        echo "==> Creating Python virtual environment '${VENV_NAME}' using ${PYTHON_SPEC} in ${VENV_PATH}..."
        mkdir -p "{{ VENV_DIR }}"
        uv venv --seed --python "${PYTHON_SPEC}" "${VENV_PATH}"
        echo "==> Successfully created venv '${VENV_NAME}'."
    else
        echo "==> Python virtual environment '${VENV_NAME}' already exists in ${VENV_PATH}."
    fi

    ${VENV_PATH}/bin/python3 -V
    ${VENV_PATH}/bin/pip3 -V

    echo "==> Activate Python virtual environment with: source ${VENV_PATH}/bin/activate"

# Meta-recipe to run `create` on all environments
create-all:
    #!/usr/bin/env bash
    for venv in {{ENVS}}; do
        just create ${venv}
    done

# Get the version of a single virtual environment's Python (usage: `just version`)
version venv="":
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"

    # This is the "default parameter" logic.
    # If VENV_NAME is empty (because `just create` was run), calculate the default.
    if [ -z "${VENV_NAME}" ]; then
        echo "==> No venv name specified. Auto-detecting from system Python..."
        VENV_NAME=$(just --quiet _get-system-venv-name)
        echo "==> Defaulting to venv: '${VENV_NAME}'"
    fi

    if [ -d "{{ VENV_DIR }}/${VENV_NAME}" ]; then
        echo "==> Python virtual environment '${VENV_NAME}' exists:"
        "{{VENV_DIR}}/${VENV_NAME}/bin/python" -V
    else
        echo "==>  Python virtual environment '${VENV_NAME}' does not exist."
    fi
    echo ""

# Get versions of all Python virtual environments
version-all:
    #!/usr/bin/env bash
    for venv in {{ENVS}}; do
        just version ${venv}
    done

# -----------------------------------------------------------------------------
# -- Installation of Tools (Sphinx, etc)
# -----------------------------------------------------------------------------

# Install the development tools for this Package in a single environment (usage: `just install`)
install venv="": (create venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        echo "==> No venv name specified. Auto-detecting from system Python..."
        VENV_NAME=$(just --quiet _get-system-venv-name)
        echo "==> Defaulting to venv: '${VENV_NAME}'"
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"
    echo "==> Installing package development tools in ${VENV_NAME}..."
    uv pip install --python "{{VENV_DIR}}/${VENV_NAME}/bin/python" -r requirements.txt

# Meta-recipe to run `install-tools` on all environments
install-all:
    #!/usr/bin/env bash
    set -e
    for venv in {{ENVS}}; do
        just install-tools ${venv}
    done

# -----------------------------------------------------------------------------
# -- Formatting/Linting
# -----------------------------------------------------------------------------

# Automatically fix all formatting and code style issues.
autoformat venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        echo "==> No venv name specified. Auto-detecting from system Python..."
        VENV_NAME=$(just --quiet _get-system-venv-name)
        echo "==> Defaulting to venv: '${VENV_NAME}'"
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    echo "==> Automatically formatting code with ${VENV_NAME}..."

    # 1. Run the FORMATTER first. This will handle line lengths, quotes, etc.
    "${VENV_PATH}/bin/ruff" format ./docs

    # 2. Run the LINTER'S FIXER second. This will handle things like
    #    removing unused imports, sorting __all__, etc.
    "${VENV_PATH}/bin/ruff" check --fix ./docs
    echo "--> Formatting complete."

# Lint code using Ruff in a single environment
check-format venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        echo "==> No venv name specified. Auto-detecting from system Python..."
        VENV_NAME=$(just --quiet _get-system-venv-name)
        echo "==> Defaulting to venv: '${VENV_NAME}'"
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"
    echo "==> Linting code with ${VENV_NAME}..."
    "${VENV_PATH}/bin/ruff" check ./docs

# -----------------------------------------------------------------------------
# -- Documentation
# -----------------------------------------------------------------------------

# Build the HTML documentation using Sphinx
docs venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        echo "==> No venv name specified. Auto-detecting from system Python..."
        VENV_NAME=$(just --quiet _get-system-venv-name)
        echo "==> Defaulting to venv: '${VENV_NAME}'"
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"
    echo "==> Building documentation..."
    "${VENV_PATH}/bin/sphinx-build" -b html docs/ docs/_build/html

# Open the HTML documentation in Web browser
docs-view venv="": (docs venv)
    echo "==> Opening documentation in viewer ..."
    open docs/_build/html/index.html

# Clean the generated documentation
docs-clean:
    echo "==> Cleaning documentation build artifacts..."
    rm -rf docs/_build

# -----------------------------------------------------------------------------
# -- Build system (migrated from Makefile)
# -----------------------------------------------------------------------------

# Show usage information
usage:
    @echo "Available build recipes:"
    @echo "  just build           - build spec in all formats"
    @echo "  just grep-options    - show places where *.Options are used"
    @echo "  just clean           - clean all generated data"
    @echo "  just authors         - show authors based on git log data"
    @echo "  just run-docs        - run http server on 8010 port to serve docs"
    @echo "  just spellcheck-docs - spell check the docs via sphinx-build"

# Build spec in all formats (main build pipeline)
build venv="": (clean) (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        VENV_NAME=$(just --quiet _get-system-venv-name)
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    export WAMP_BUILD_ID="${WAMP_BUILD_ID:-$(date -Iseconds)}"
    echo "==> Building with WAMP_BUILD_ID=${WAMP_BUILD_ID}"

    just _build-images
    just _update-spec-date
    just _build-spec
    just _build-docs

# Clean all generated data
clean:
    #!/usr/bin/env bash
    set -e
    echo "==> Cleaning build artifacts..."

    OUTPUTDIR="./dist"
    TMPBUILDDIR="./.build"
    SITEBUILDDIR="./docs/_static/gen"

    if [ -d "${OUTPUTDIR}" ]; then rm -rf "${OUTPUTDIR}"; fi
    if [ -d "${TMPBUILDDIR}" ]; then rm -rf "${TMPBUILDDIR}"; fi
    if [ -d "${SITEBUILDDIR}" ]; then rm -rf "${SITEBUILDDIR}"; fi

    mkdir -p "${OUTPUTDIR}"
    mkdir -p "${TMPBUILDDIR}"
    mkdir -p "${SITEBUILDDIR}"

# Find places where *.Options are used in the RFC files
grep-options:
    #!/usr/bin/env bash
    set -e
    echo "==> Searching for Options usage in RFC files..."
    find rfc/ -name "*.md" -type f -exec grep -o "\`\w*\.Options\.[a-z_]*|.*\`" {} \;

# Show authors based on git log data
authors:
    #!/usr/bin/env bash
    set -e
    echo "==> Authors from git log:"
    git log --pretty=format:"%an <%ae> %x09" rfc | sort | uniq

# Run HTTP server on port 8010 to serve documentation
run-docs:
    #!/usr/bin/env bash
    set -e
    echo "==> Starting HTTP server on port 8010..."
    cd dist && python -m http.server 8010

# Spell check the documentation via sphinx-build
spellcheck-docs venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        VENV_NAME=$(just --quiet _get-system-venv-name)
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    TMPBUILDDIR="./.build"
    mkdir -p "${TMPBUILDDIR}"

    echo "==> Spell checking documentation..."
    "${VENV_PATH}/bin/sphinx-build" -b spelling -d "${TMPBUILDDIR}/docs/doctrees" docs "${TMPBUILDDIR}/docs/spelling"

# -----------------------------------------------------------------------------
# -- Requirements installation (for build tools)
# -----------------------------------------------------------------------------

# Install xml2rfc (including PDF support) on Linux locally
requirements-xml2rfc:
    #!/usr/bin/env bash
    set -e
    echo "==> Installing xml2rfc requirements..."
    sudo apt install libpango1.0-dev enscript

# Install mmark on Linux locally
requirements-mmark:
    #!/usr/bin/env bash
    set -e
    echo "==> Installing mmark..."
    wget https://github.com/mmarkdown/mmark/releases/download/v2.2.25/mmark_2.2.25_linux_amd64.tgz
    tar xvzf mmark_2.2.25_linux_amd64.tgz
    rm -f ./mmark*.tgz
    sudo cp ./mmark /usr/local/bin/

# -----------------------------------------------------------------------------
# -- Internal build helpers
# -----------------------------------------------------------------------------

# Internal: Build optimized SVGs from docs/_graphics/*.svg using Scour
_build-images venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        VENV_NAME=$(just --quiet _get-system-venv-name)
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    SOURCEDIR="./docs/_graphics"
    SITEBUILDDIR="./docs/_static/gen"

    echo "==> Building optimized SVG images..."
    mkdir -p "${SITEBUILDDIR}"

    if [ -d "${SOURCEDIR}" ]; then
        find "${SOURCEDIR}" -name "*.svg" -type f | while read -r source_file; do
            filename=$(basename "${source_file}")
            target_file="${SITEBUILDDIR}/${filename}"
            echo "  Processing: ${filename}"
            "${VENV_PATH}/bin/scour" \
                --remove-descriptive-elements \
                --enable-comment-stripping \
                --enable-viewboxing \
                --indent=none \
                --no-line-breaks \
                --shorten-ids \
                "${source_file}" "${target_file}"
        done
    fi

# Internal: Update spec date in RFC files
_update-spec-date:
    #!/usr/bin/env bash
    set -e
    echo "==> Updating spec dates..."

    CURRENTDATE=$(TZ=UTC date -Iseconds)

    # Determine sed arguments based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed_args="-i ''"
    else
        sed_args="-i"
    fi

    sed ${sed_args} -e "s/^date = .*/date = ${CURRENTDATE}/g" ./rfc/wamp.md
    sed ${sed_args} -e "s/^date = .*/date = ${CURRENTDATE}/g" ./rfc/wamp-bp.md
    sed ${sed_args} -e "s/^date = .*/date = ${CURRENTDATE}/g" ./rfc/wamp-ap.md

# Internal: Build RFC specifications using mmark and xml2rfc
_build-spec venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        VENV_NAME=$(just --quiet _get-system-venv-name)
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    echo "==> Building RFC specifications..."

    TMPBUILDDIR="./.build"
    OUTPUTDIR="./dist"

    # Determine sed arguments based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed_args="-i ''"
    else
        sed_args="-i"
    fi

    # Build main WAMP spec
    echo "  Building wamp.md..."
    mmark ./rfc/wamp.md > "${TMPBUILDDIR}/wamp.xml"
    sed ${sed_args} 's/<sourcecode align="left"/<sourcecode/g' "${TMPBUILDDIR}/wamp.xml"
    sed ${sed_args} 's/<t align="left"/<t/g' "${TMPBUILDDIR}/wamp.xml"
    xmllint --noout "${TMPBUILDDIR}/wamp.xml"
    ${VENV_PATH}/bin/xml2rfc --v3 --text "${TMPBUILDDIR}/wamp.xml" -o "${OUTPUTDIR}/wamp_latest_ietf.txt"
    ${VENV_PATH}/bin/xml2rfc --v3 --html "${TMPBUILDDIR}/wamp.xml" -o "${OUTPUTDIR}/wamp_latest_ietf.html"
    ${VENV_PATH}/bin/xml2rfc --v3 --pdf "${TMPBUILDDIR}/wamp.xml" -o "${OUTPUTDIR}/wamp_latest_ietf.pdf"

    # Build WAMP-BP spec
    echo "  Building wamp-bp.md..."
    mmark ./rfc/wamp-bp.md > "${TMPBUILDDIR}/wamp-bp.xml"
    sed ${sed_args} 's/<sourcecode align="left"/<sourcecode/g' "${TMPBUILDDIR}/wamp-bp.xml"
    sed ${sed_args} 's/<t align="left"/<t/g' "${TMPBUILDDIR}/wamp-bp.xml"
    xmllint --noout "${TMPBUILDDIR}/wamp-bp.xml"
    ${VENV_PATH}/bin/xml2rfc --v3 --text "${TMPBUILDDIR}/wamp-bp.xml" -o "${OUTPUTDIR}/wamp_bp_latest_ietf.txt"
    ${VENV_PATH}/bin/xml2rfc --v3 --html "${TMPBUILDDIR}/wamp-bp.xml" -o "${OUTPUTDIR}/wamp_bp_latest_ietf.html"
    ${VENV_PATH}/bin/xml2rfc --v3 --pdf "${TMPBUILDDIR}/wamp-bp.xml" -o "${OUTPUTDIR}/wamp_bp_latest_ietf.pdf"

    # Build WAMP-AP spec
    echo "  Building wamp-ap.md..."
    mmark ./rfc/wamp-ap.md > "${TMPBUILDDIR}/wamp-ap.xml"
    sed ${sed_args} 's/<sourcecode align="left"/<sourcecode/g' "${TMPBUILDDIR}/wamp-ap.xml"
    sed ${sed_args} 's/<t align="left"/<t/g' "${TMPBUILDDIR}/wamp-ap.xml"
    xmllint --noout "${TMPBUILDDIR}/wamp-ap.xml"
    ${VENV_PATH}/bin/xml2rfc --v3 --text "${TMPBUILDDIR}/wamp-ap.xml" -o "${OUTPUTDIR}/wamp_ap_latest_ietf.txt"
    ${VENV_PATH}/bin/xml2rfc --v3 --html "${TMPBUILDDIR}/wamp-ap.xml" -o "${OUTPUTDIR}/wamp_ap_latest_ietf.html"
    ${VENV_PATH}/bin/xml2rfc --v3 --pdf "${TMPBUILDDIR}/wamp-ap.xml" -o "${OUTPUTDIR}/wamp_ap_latest_ietf.pdf"

# Internal: Build documentation using Sphinx
_build-docs venv="": (install venv)
    #!/usr/bin/env bash
    set -e
    VENV_NAME="{{ venv }}"
    if [ -z "${VENV_NAME}" ]; then
        VENV_NAME=$(just --quiet _get-system-venv-name)
    fi
    VENV_PATH="{{ VENV_DIR }}/${VENV_NAME}"

    TMPBUILDDIR="./.build"
    OUTPUTDIR="./dist"

    echo "==> Building documentation..."

    # First test with all warnings fatal
    "${VENV_PATH}/bin/sphinx-build" -nWT -b dummy ./docs "${TMPBUILDDIR}/docs"

    # Run spell checker
    "${VENV_PATH}/bin/sphinx-build" -b spelling -d "${TMPBUILDDIR}/docs/.doctrees" ./docs "${TMPBUILDDIR}/docs/spelling"

    # Generate HTML output
    "${VENV_PATH}/bin/sphinx-build" -b html ./docs "${TMPBUILDDIR}/site_build"

    # Copy to output directory
    cp -R "${TMPBUILDDIR}/site_build"/* "${OUTPUTDIR}/"
    cp -R docs/_static "${OUTPUTDIR}/"
    cp -R docs/_graphics "${OUTPUTDIR}/"
