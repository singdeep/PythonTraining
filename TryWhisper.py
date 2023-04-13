import whisper

model = whisper.load_model("base")
result = model.transcribe("assets/sampleHomer.mp3")

print(result)