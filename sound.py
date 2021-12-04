def play_sound(ev3):
    ev3.speaker.set_volume(100, which='_all_')
    ev3.speaker.set_speech_options(language="pt", voice=None, speed=20, pitch=None)
    ev3.speaker.say("TRAVA NA POSE OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!")

    notes = ['A4/4', 'A4/4', 'A4/4', 'A4/4', 'A4/4', 'B4/4','D4/5', 'A4/4']
    ev3.speaker.play_notes(notes, tempo=120)
    ev3.speaker.play_file("tokio.wav")
