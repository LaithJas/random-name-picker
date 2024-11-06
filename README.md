
# Random Name Picker

This project is built using Python and requires the Pygame library to run. Below are simple instructions to set up your environment and install Pygame, whether you’re using Anaconda, a standard Python environment, or installing directly on your local machine.

## Prerequisites

- Python (already installed)
- Anaconda (if using an Anaconda environment)

## Installation Options

### Option 1: Install Pygame in an Anaconda Environment

1. **Create a new environment** (optional, but recommended):
   ```bash
   conda create -n pygame_env python=3.13
   ```

2. **Activate the environment**:
   ```bash
   conda activate pygame_env
   ```

3. **Install Pygame**:
   ```bash
   conda install -c cogsci pygame
   ```

### Option 2: Install Pygame in a Python Virtual Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv pygame_env
   ```

2. **Activate the environment**:
   - **On Windows**:
     ```bash
     pygame_env\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source pygame_env/bin/activate
     ```

3. **Install Pygame**:
   ```bash
   pip install pygame
   ```

### Option 3: Install Pygame Directly on Your Local Machine

If you prefer to install Pygame globally on your local machine:

```bash
pip install pygame
```

## Running the Script

Once Pygame is installed, you can run the script by navigating to the project directory and using:

```bash
python namePicker.py
```

Happy coding!
