tunning = [
    "E",
    "A",
    "D",
    "G",
    "B",
    "E"
]

def int_to_note(num):
    notes = {
        0: "A",
        1: "A#/Bb",
        2: "B",
        3: "C",
        4: "C#/Db",
        5: "D",
        6: "D#/Eb",
        7: "E",
        8: "F",
        9: "F#/Gb",
        10: "G",
        11: "G#/Ab"
        }
    return notes[num % 12]

def note_to_int(num):
    notes = {
        "A": 0,
        "A#/Bb": 1,
        "B": 2,
        "C": 3,
        "C#/Db": 4,
        "D": 5,
        "D#/Eb": 6, 
        "E": 7,
        "F": 8,
        "F#/Gb": 9,
        "G": 10,
        "G#/Ab": 11
        }
    return notes[num]

# intervals
# 0     perfect unison
# 1st   minor second
# 2nd   major second
# 3rd   minor third
# 4th   major third
# 5th   perfect fourth
# 6th   augmented fourth
# 7th   perfect 5th
# 8th   minor sixth
# 9th   major sixth
# 10th  minor seventh
# 11th  major seventh
# 12th  perfect octave

# major triad chord = root - major 3rd - perfect 5th
def calc_maj_tri_chord(note):
    chord = []
    num_note = note_to_int(note)
    chord.append(int_to_note(num_note))
    chord.append(int_to_note(num_note + 4))
    chord.append(int_to_note(num_note + 7))
    return chord

# minor triad chord = root - minor 3rd - perfect 5th
def calc_min_tri_chord(note):
    chord = []
    num_note = note_to_int(note)
    chord.append(int_to_note(num_note))
    chord.append(int_to_note(num_note + 3))
    chord.append(int_to_note(num_note + 7))
    return chord

# augmented triad chord = root - major 3rd - aug 5th
def calc_aug_tri_chord(note):
    chord = []
    num_note = note_to_int(note)
    chord.append(int_to_note(num_note))
    chord.append(int_to_note(num_note + 4))
    chord.append(int_to_note(num_note + 8))
    return chord

# diminished triad chord = root - minor 3rd - dim5th
def calc_dim_tri_chord(note):
    chord = []
    num_note = note_to_int(note)
    chord.append(int_to_note(num_note))
    chord.append(int_to_note(num_note + 3))
    chord.append(int_to_note(num_note + 6))
    return chord

# suspended 4th triad = root - perfect 4th - perfect 5th
def calc_sus4_tri_chord(note):
    chord = []
    num_note = note_to_int(note)
    chord.append(int_to_note(num_note))
    chord.append(int_to_note(num_note + 5))
    chord.append(int_to_note(num_note + 7))
    return chord

# suspended 2nd triad = root - major 2nd - perfect 5th
def calc_sus2_tri_chord(note):
    chord = []
    num_note = note_to_int(note)
    chord.append(int_to_note(num_note))
    chord.append(int_to_note(num_note + 2))
    chord.append(int_to_note(num_note + 7))
    return chord

def print_tunning():
    print("current tunning: ", end='')
    for s in tunning:
        print(s, end=' ')
    print("")

def print_fret_board():
    for string in range(7):
        for i in range(13):
            if (string != 0):
                print(int_to_note(note_to_int(tunning[string - 1]) + i) + "\t", end='')
            else:
                print(str(i) + "\t", end='')
        print("")
    print("")

# Find triad with "linear scan method"
# start search on starting_string scan for first note
# after first note is found go to next string and find second note
# same for all subsequent notes
def find_triad_lin_scan(tri_notes, starting_string=0):
    string = starting_string
    cur_note = 0
    rtn = []
    while True:
        for fret in range(13):
            freted_note = note_to_int(tunning[string]) + fret
            if (tri_notes[cur_note] == int_to_note(freted_note)):
                rtn.append([string, freted_note, fret])
                string += 1
                cur_note += 1
                break
            elif(fret == 12):
                string += 1
        if (cur_note == len(tri_notes)):
            break
        elif (string == len(tunning) or string == -1):
            print("failed to construct chord.")
            return []
    return rtn

chord_types = {
    "maj": calc_maj_tri_chord,
    "min": calc_min_tri_chord,
    "aug": calc_aug_tri_chord,
    "dim": calc_dim_tri_chord,
    "sus4": calc_sus4_tri_chord,
    "sus2": calc_sus2_tri_chord
}