from music21 import stream, note, chord, meter, key, tempo



def _midi_to_pitch(midi: int) -> str:
    note_map = {
        0: "C",
        1: "C#",
        2: "D",
        3: "D#",
        4: "E",
        5: "F",
        6: "F#",
        7: "G",
        8: "G#",
        9: "A",
        10: "A#",
        11: "B"
    }

    return note_map[midi % 12] + str((midi//12) - 1)

 
def _create_stream(measures: list, base_tempo: int):
    """take a list of measures retrieved from tracks table and return a music21 stream object for it"""

    s = stream.Score()
    p = stream.Part()

    for measure in measures:
        m = stream.Measure(number=len(p.getElementsByClass('Measure')) + 1)

        for beat in measure["beats"]:
            beat_ql = (int(beat["duration"]) * base_tempo) / 60

            # not accounting for rests yet
            note_data = beat["notes"]
            # if there is only one note for the beat, add it as a note
            if len(note_data) == 1:
                n = note.Note(
                    _midi_to_pitch(note_data[0]["midi"]),
                    quarterLength=beat_ql
                )
                print(f"adding note: {_midi_to_pitch(note_data[0]["midi"])}")
                m.append(n)

            else:
                c = chord.Chord([_midi_to_pitch(n["midi"]) for n in note_data])
                c.quarterLength = beat_ql

                m.append(c)

        p.append(m)

    s.append(p)

    return s


def get_theory(measures: list, base_tempo: int):
    """returns the theory of a list of measures from a song"""

    stream = _create_stream(measures, base_tempo)

    return stream.analyze("key")


def main():
    test_tempo = 100
    test_measures = [
        {
            "index": 0,
            "beats": [
                {"time": 0.0, "duration": 0.6, "notes": [{"string": 2, "fret": 1, "midi": 60}]},   # C4
                {"time": 0.6, "duration": 0.6, "notes": [{"string": 2, "fret": 3, "midi": 62}]},   # D4
                {"time": 1.2, "duration": 0.6, "notes": [{"string": 1, "fret": 0, "midi": 64}]},   # E4
                {"time": 1.8, "duration": 0.6, "notes": [{"string": 1, "fret": 1, "midi": 65}]},   # F4
            ],
        },
        {
            "index": 1,
            "beats": [
                {"time": 2.4, "duration": 0.6, "notes": [{"string": 1, "fret": 3, "midi": 67}]},   # G4
                {"time": 3.0, "duration": 0.6, "notes": [{"string": 1, "fret": 5, "midi": 69}]},   # A4
                {"time": 3.6, "duration": 0.6, "notes": [{"string": 1, "fret": 7, "midi": 71}]},   # B4
                {"time": 4.2, "duration": 0.6, "notes": [{"string": 1, "fret": 8, "midi": 72}]},   # C5
            ],
        },
    ]
    print(get_theory(test_measures, test_tempo))



if __name__ == "__main__":
    main()




            









