# Makefile for installing the mkdocify Gemini extension.
# This Makefile is compatible with Windows, Linux, and macOS.

.PHONY: install clean

ifeq ($(OS),Windows_NT)
    # Windows settings
    TARGET_DIR := $(USERPROFILE)\.gemini\extensions\mkdocify
    VENV_PYTHON := $(TARGET_DIR)\venv\Scripts\python.exe
    REQUIREMENTS_DST := $(TARGET_DIR)\requirements.txt

install:
	@echo "Installing mkdocify extension for Windows..."
	@echo "Target directory: $(TARGET_DIR)"
	@if not exist "$(TARGET_DIR)" mkdir "$(TARGET_DIR)"
	@xcopy server "$(TARGET_DIR)\server\" /E /I /Y /Q
	@copy requirements.txt "$(TARGET_DIR)\" /Y > NUL
	@copy gemini.md "$(TARGET_DIR)\" /Y > NUL
	@copy gemini-extension.json "$(TARGET_DIR)\" /Y > NUL
	@echo "Creating Python virtual environment..."
	python -m venv "$(TARGET_DIR)\venv"
	@echo "Installing dependencies..."
	"$(VENV_PYTHON)" -m pip install --quiet -r "$(REQUIREMENTS_DST)"
	@echo "Installation complete."

clean:
	@echo "Cleaning up mkdocify extension..."
	@if exist "$(TARGET_DIR)" rmdir /S /Q "$(TARGET_DIR)"
	@echo "Cleanup complete."

else
    # Unix-like (Linux/macOS) settings
    TARGET_DIR := $(HOME)/.gemini/extensions/mkdocify
    VENV_PYTHON := $(TARGET_DIR)/venv/bin/python
    REQUIREMENTS_DST := $(TARGET_DIR)/requirements.txt

install:
	@echo "Installing mkdocify extension for Linux/macOS..."
	@echo "Target directory: $(TARGET_DIR)"
	@mkdir -p "$(TARGET_DIR)"
	@cp -r server "$(TARGET_DIR)/"
	@cp requirements.txt gemini.md gemini-extension.json "$(TARGET_DIR)/"
	@echo "Creating Python virtual environment..."
	python3 -m venv "$(TARGET_DIR)/venv"
	@echo "Installing dependencies..."
	"$(VENV_PYTHON)" -m pip install --quiet -r "$(REQUIREMENTS_DST)"
	@echo "Installation complete."

clean:
	@echo "Cleaning up mkdocify extension..."
	@rm -rf "$(TARGET_DIR)"
	@echo "Cleanup complete."

endif