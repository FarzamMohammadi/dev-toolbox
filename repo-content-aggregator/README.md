# Repository Content Aggregator

Aggregates repository content into a single markdown file while respecting .gitignore rules.

## Setup & Usage

1. Create virtual environment:
    ```sh
    python -m venv venv
    ```

2. Activate:
- Windows: `.\venv\Scripts\activate`
- Unix/macOS: `source venv/bin/activate`

3. Install & Run:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the script:
    ```sh
    python main.py <repo_path> [-o output.txt] [-m max_size_mb]
    ```

## Features
- Full .gitignore support (all levels, all patterns)
- Auto-skips binary and large files
- Structured output with file/directory markers
- Repository metadata included