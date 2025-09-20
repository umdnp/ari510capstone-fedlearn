#!/bin/bash

# Create the virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  py -m venv .venv
fi

# Ensure the virtual environment was created
if [ ! -d ".venv" ]; then
  echo "Error: Virtual environment creation failed."
  exit 1
fi

# Create convenience symlinks based on OS
if [ "$(uname -s)" == "Linux" ] || [ "$(uname -s)" == "Darwin" ]; then
  # If Linux or macOS, use .venv/bin/activate
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Error: .venv/bin/activate does not exist."
    exit 1
  fi
  ln -sf .venv/bin/activate activate
  echo "Symlink for activation created: .venv/bin/activate"
elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ] || [ "$(expr substr $(uname -s) 1 7)" == "MSYS_NT" ]; then
  # If Windows, use .venv/Scripts/activate.bat
  if [ ! -f ".venv/Scripts/activate.bat" ]; then
    echo "Error: .venv/Scripts/activate.bat does not exist."
    exit 1
  fi
  ln -sf .venv/Scripts/activate activate
  ln -sf .venv/Scripts/activate.bat activate.bat
  echo "Symlink for activation created: .venv/Scripts/activate.bat"
else
  echo "Error: Unsupported operating system."
  exit 1
fi

# Install requirements.txt if it exists
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  source activate
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "No requirements.txt found. Skipping package installation."
fi

echo "Setup complete!"
