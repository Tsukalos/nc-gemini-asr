import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from asr_gemini import ASRGeminiModel
from feed_scrapper import NCEpisodeScrapper

if __name__ == "__main__":

    model = genai.GenerativeModel("gemini-1.5-flash")
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT : HarmBlockThreshold.BLOCK_NONE,
    }

    # gen_config = genai.GenerationConfig(
    #     max_output_tokens=8192,
    #     top_p=0.95,
    # )

    asr_model = ASRGeminiModel(model, safety_settings)

    eps = NCEpisodeScrapper(feed="https://jovemnerd.com.br/feed-nerdcast/")
    asr_model.transcribe_episodes(eps)