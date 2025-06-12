import os
from pprint import pprint
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

def createvoice(text_message):
    #Synthesizerの初期化
    voicevox_onnxruntime_path = "onnxruntime/lib/" + Onnxruntime.LIB_VERSIONED_FILENAME
    open_jtalk_dict_dir = "dict/open_jtalk_dic_utf_8-1.11"
    synthesizer = Synthesizer(Onnxruntime.load_once(filename=voicevox_onnxruntime_path), OpenJtalk(open_jtalk_dict_dir))
        
    #音声モデルの読み込み
    with VoiceModelFile.open("models/vvms/0.vvm") as model:
        synthesizer.load_voice_model(model)

    #テキスト音声合成
    style_id = 8

    query = synthesizer.create_audio_query(text=text_message, style_id=style_id)
    query.speed_scale = 1.2

    wav = synthesizer.synthesis(audio_query=query,style_id=style_id)
    with open("output.wav", "wb") as f:
        f.write(wav)

    return