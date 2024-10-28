import requests
from pathlib import Path

def download_audio(url, output_filename=None, output_folder="audio_dl", chunk_size=8192):
        """Downloads an audio file from a URL.

        Args:
            url: The URL of the audio file.
            output_filename: The desired filename for the downloaded file.
                            If None, the filename is extracted from the URL.
            chunk_size: The size of the chunks to download (in bytes).  A larger
                    chunk size can improve download speed.


        Returns:
            The Path to the downloaded file, or None if there's an error.
            Prints an informative message about the download.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            if output_filename is None:
                # Extract filename from URL (robust method)
                filename = Path(url).name
                if not filename:  # handle edge cases where there might not be a filename component
                    raise ValueError("Could not determine filename from URL")
                output_path = Path(filename)
            else:
                output_path = Path(output_filename)  # Use pathlib.Path for robustness

            output_folder = Path(output_folder)

            # Ensure the directory exists
            output_folder.mkdir(parents=True, exist_ok=True)
            output_path = output_folder / output_path
            
            if output_path.exists():
                print(f"File '{output_path}' already exists. Skipping download.")
                return output_path

            with open(output_path, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)

            print(f"Audio file downloaded successfully to: {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Request error downloading file: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None