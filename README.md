# Snippet Manager

## Description

Snippet Manager is a modern, light-themed application for managing code snippets and text notes. It allows users to store snippets as individual text files, search and filter snippets, and provides a user-friendly interface with a persistent settings feature.

## Features

- Store snippets as individual text files
- Search and filter snippets
- Modern light theme interface
- Persistent settings
- Directory-based storage

## Installation

To install and run the app locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/womail/snippet-manager.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd snippet-manager
   ```
3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
5. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Run the application:**
   ```bash
   python snippet_manager.py
   ```

## Usage

- **New Snippet:** Click the 'New Snippet' button to create a new snippet.
- **Save Snippet:** After editing, click the 'Save Snippet' button to save changes.
- **Delete Snippet:** Select a snippet and click the 'Delete Snippet' button to remove it.
- **Change Directory:** Use the 'Settings' button to change the snippets directory.

## File Storage

The app stores its files locally in the directory specified in the `snippet_settings.json` file. Configuration files are located in the `config` directory.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [Your Name] at [your.email@example.com]. 