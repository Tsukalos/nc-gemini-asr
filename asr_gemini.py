import google.generativeai as genai
from pathlib import Path
from getpass import getpass
import os
import utils
   
class ASRGeminiModel:
    def __init__(self, model, safety_settings=None, gen_config=None, api_key=None):
        if (not api_key) and ("GOOGLE_API_KEY" not in os.environ):
            api_key = getpass("Provide your Google API key here: ")
        genai.configure(api_key=api_key)

        self.model = model
        self.safety_settings = safety_settings
        self.gen_config = gen_config

    def transcribe_episodes(self, eps, text_output_folder="transcriptions", stream=True):
        """
        Transcribes a list of podcast episodes.
        Args:
            eps (list): A list of dictionaries (or NCEpisodeScrapper) containing episode information. Each dictionary should have a "dl_url" key with the download URL of the episode.
            text_output_folder (str, optional): The folder where transcriptions will be saved. Defaults to "transcriptions".
            stream (bool, optional): Whether to stream the transcription results. Defaults to True.
        Returns:
            None
        This method downloads audio files from the provided URLs, transcribes them using a gemini model, and saves the transcriptions to text files. If a transcription already exists for an episode, it skips the transcription process for that episode.
        """
        text_output_folder = Path(text_output_folder)
        text_output_folder.mkdir(parents=True, exist_ok=True)

        for ep in eps:
            url = ep["dl_url"]

            downloaded = utils.download_audio(url, output_folder="nerdcasts")

            if not downloaded:
                print(f"Error downloading {url}, skipping...")
                continue

            text_transcription = text_output_folder / Path(downloaded.stem).with_suffix('.txt')
            
            if not text_transcription.exists():
                audio_file_up = genai.upload_file(downloaded)
                result_text = ""
                response = self.model.generate_content(
                    ["Transcreva o audio.", audio_file_up],
                    safety_settings=self.safety_settings,
                    generation_config=self.gen_config,
                    stream=stream
                )
                try:
                    if stream:
                        for chunk in response:
                            print(chunk.text)
                            result_text += chunk.text
                    else:
                        print(response.text)
                        result_text = response.text
                except ValueError as e:
                    print(f"Error {e=}")

                text_transcription.write_text(result_text)
                audio_file_up.delete()
            else:
                print(f"Transcription for {downloaded} already exists. Skipping...")

