# ASR Gemini Nerdcast Transcriber

## Overview

This project provides a tool to download episodes from the popular podcast Nerdcast and transcribe them using the Gemini API. The transcriptions are saved as text files for easy access and reference.

## Features

- Download episodes from Nerdcast.
- Transcribe audio files using the Gemini API.
- Save transcriptions to a specified folder.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Tsukalos/nc-gemini-asr.git
    cd nc-gemini-asr
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your Google API key:
    - You can either set the `GOOGLE_API_KEY` environment variable:
        ```sh
        export GOOGLE_API_KEY=your_api_key_here
        ```
    - Or provide the API key when prompted during runtime.

## Usage

1. Configure the model and settings in .

2. Run the script:
    ```sh
    python asr_gemini.py
    ```

## Example

```python
from asr_gemini import ASRGeminiModel
from feed_scrapper import NCEpisodeScrapper

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

asr_model = ASRGeminiModel(model, safety_settings)

# Scrape episodes
eps = NCEpisodeScrapper(feed="https://jovemnerd.com.br/feed-nerdcast/")

# Transcribe episodes
asr_model.transcribe_episodes(eps)
```
## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements
[Nerdcast](https://jovemnerd.com.br/podcasts/nerdcast) for the podcast episodes.