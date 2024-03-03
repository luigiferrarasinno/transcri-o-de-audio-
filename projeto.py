from flask import Flask, render_template, request
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

app = Flask(__name__)
app.secret_key = "alura"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        duration = int(request.form['duration'])  # Obter a duração da gravação
        tempo = request.form['tempo']  # Obter a unidade de tempo (segundos, minutos ou horas)

        # Converter a duração para segundos, se necessário
        if tempo == 'minutos':
            duration *= 60
        elif tempo == 'horas':
            duration *= 3600

        fs = 44100

        # Gravação de áudio
        print("Gravando áudio...")
        gravacao = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

        # Salvar o áudio em um arquivo WAV
        sf.write('audio_gravado.wav', gravacao, fs)

        # Carregar o arquivo de áudio gravado
        audio_gravado, _ = sf.read('audio_gravado.wav')

        # Transcrição do áudio
        recognizer = sr.Recognizer()
        with sr.AudioFile('audio_gravado.wav') as source:
            audio_data = recognizer.record(source)
            try:
                texto_transcrito = recognizer.recognize_google(audio_data, language='pt-BR')
            except sr.UnknownValueError:
                texto_transcrito = "Não foi possível transcrever o áudio."
            except sr.RequestError as e:
                texto_transcrito = f"Erro durante o reconhecimento de fala: {e}"

        return render_template('index.html', texto_transcrito=texto_transcrito)

    return render_template('index.html', texto_transcrito=None)

if __name__ == '__main__':
    app.run(debug=True)
