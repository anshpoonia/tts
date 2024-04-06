# import prep
from utils import hash256, get_dir, get_speakers, save_speaker, check_language
from error import SpeakerNotFoundError
from TTS.api import TTS as coqui
import whisper
import os
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


class TTS:
    def __init__(self):
        self.model = coqui(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(device)
        self.male_speakers = get_speakers("male")
        self.female_speakers = get_speakers("female")
        self.custom_speakers = get_speakers("custom")
        self.save_dir = get_dir("files")

    def transform(self, text, tag="male", speaker="1", lang="en"):

        file_name = hash256(text + tag + speaker + lang) + ".wav"
        file_path = os.path.join(self.save_dir, file_name)

        if os.path.isfile(file_path):
            return file_path

        speaker_file = self.get_speaker(tag, speaker)
        check_language(lang)

        self.model.tts_to_file(text=text, speaker_wav=speaker_file, file_path=file_path, language=lang)
        return file_path

    def get_speaker(self, tag, speaker):
        if tag == "male":
            try:
                return self.male_speakers[int(speaker)]
            except IndexError:
                raise SpeakerNotFoundError()
        elif tag == "female":
            try:
                return self.female_speakers[int(speaker)]
            except IndexError:
                raise SpeakerNotFoundError
        elif tag == "custom":
            for i in self.custom_speakers:
                if speaker in i:
                    return i
        raise SpeakerNotFoundError

    def new_speaker(self, file):
        file_path, code = save_speaker(file)
        self.custom_speakers.append(file_path)
        return code


class STT:
    def __init__(self):
        self.model_dir = get_dir("whisper_models")
        self.model = whisper.load_model("base", device=device, download_root=self.model_dir)

    def transform(self, file_path):
        text = self.model.transcribe(file_path)["text"]
        return text
