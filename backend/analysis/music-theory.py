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

    return note_map[midi % 12] + str((midi/12) - 1)

 
def _create_stream(measures: list, base_tempo: int):
    """take a list of measures retrieved from tracks table and return a music21 stream object for it"""

    s = stream.Score()
    p = stream.Part()

    for measure in measures:
        m = stream.Measure(number=len(p.getElementsByClass('Measure')) + 1)

        for beat in measure.get("beats"):
            beat_ql = (beat.get("duration") * base_tempo) / 60

            # not accounting for rests yet
            note_data = beat.get("notes")
            # if there is only one note for the beat, add it as a note
            if len(note_data) == 1:
                n = note.Note(
                    _midi_to_pitch(note_data.get("midi")),
                    quarterLength=beat_ql
                )
                m.append(n)

            else:
                c = chord.Chord([_midi_to_pitch(n.get("midi")) for n in note_data])
                c.quarterLength = beat_ql

                m.append(c)

        p.append(m)

    s.append(p)

            









