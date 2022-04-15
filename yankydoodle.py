from adafruit_circuitplayground import cp
import random
import time

E   = 164.81
F   = 174.61
G   = 196.00
A   = 220.00
B   = 246.94
C   = 261.63
D   = 293.66
Ds  = 311.13
E2  = 329.63
F2  = 349.23
Fs  = 369.99
G2  = 392.00
Ab  = 415.30
A2  = 440.00
B2  = 493.88
C2  = 523.25

e  = 0.1
q  = 0.2
qd = 0.3
h  = 0.4
f  = 0.8

harmonic_c_major = [C, D, E, F, G, Ab, B, C2]
harmonic_a_minor = [E, Fs, G, A, B, C, Ds]

yankee_doodle_verse        = [C, C, D, E2, C, E2, D, C, C, D, E2, C, B, C, C, D, E2, F, E2, D, C, B, G, A, B, C, C]
yankee_doodle_verse_tempo  = [q, q, q, q, q, q, h, q, q, q, q, h, h, q, q, q, q, q, q, q, q, q, q, q, q, h, h]

yankee_doodle_chorus       = [A, B, A, G, A, B, C, G, A, G, F, E, G, A, B, A, G, A, B, C, A, G, C, B, D, C, C]
yankee_doodle_chorus_tempo = [qd,e, q, q, q, q, h, qd,e, q, q, h, h, qd,q, q, q, q, q, q, q, q, q, q, q, h, h]

while True:
    for i, note in enumerate(yankee_doodle_verse):
        tempo = yankee_doodle_verse_tempo[i]
        cp.play_tone(int(note), tempo)
    time.sleep(0.2)
    for i, note in enumerate(yankee_doodle_chorus):
        tempo = yankee_doodle_chorus_tempo[i]
        cp.play_tone(int(note), tempo)
    time.sleep(0.2)

    #for i in range(20):
    #    note = random.choice(harmonic_a_minor)
    #    tempo = random.choice(tempos)
    #    cp.play_tone(int(note), tempo)
    #for i in range(10):
    #    note = random.choice(harmonic_c_major)
    #    tempo = random.choice(tempos)
    #    cp.play_tone(int(note), tempo)
