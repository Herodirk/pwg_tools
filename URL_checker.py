# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 12:14:32 2024

@author: Herodirk

URL checker
This is a web crawler that check for the existence of videos on youtube with a specified URL.
THe goal of this program is to find youtube links that are useful for The Password Game.
Copyright (C) 2024 Herodirk

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/

This program is not affiliated with neal.fun

General warning: Google and Youtube have defenses setup against web crawlers.
There is a possibility that your IP will be blocked from Google and Youtube
if they detect and take action against this web crawler if you use it.
The terms of the GNU General Public License has a Limitation of Liability clause (see TERMS AND CONDITIONS 16),
this means I (Herodirk) am not responsible for your loss of access to Google or Youtube.
Although the GNU GPL does state you do not have to agree to the terms for you to copy and run this program (see TERMS AND CONDITIONS 9),
I (Herodirk) would appreciate that you do not blame me (Herodirk)
and that you understand that this is a run at your own risk program.
The GNU GPL does state that you automatically agree to the terms if you edit the code in any way (see TERMS AND CONDITIONS 9).

Usage:
copy the code from this Github repository to a .py file on your device
do not run this program on github
I suggest using a code editor and interpreter like VScode 
run the file to load the functions
then use the url_generator_and_checker or google_search_urls functions to check URLs


url_generator_and_checker(desired_strs={"begin": "", "middle": [], "end": "123456789"}, optimize=True, max_atom=48, max_dig=12)
this function will ping youtube at all possible video identifier that comply with your inputted settings
these pings will happen one by one with some time in between, controlled by sleep_time

desired_strs argument takes a dictionary with "begin", "middle" and "end" as keys
a youtube video identifier is 11 characters long
the function will loop through all possible combinations and permutations for left over spaces
the identifier it tries will start with what is inputted for "begin" and end with the "end" input
the "middle" input will be permutated with the other generated characters

the optimize argument takes a boolean toggling automatic optimizations
automatic optimizations skip video identifiers that will not be useful for The Password Game

max_atom takes an integer for the max atomic number sum of the identifier
this requires optimize to be True

max_dig takes an integer for the max digit sum of the identifier
this requires optimize to be True


google_search_urls(search_term="dQw4w9WgXcQ")
this function will ping Google's search engine with the query
'allinurl:[search_term]%20site:https://www.youtube.com/watch'
where search_term gets replaced by the function argument search_term
"""

import urllib.request
from urllib.request import Request, urlopen
from itertools import permutations, combinations_with_replacement
# from more_itertools import distinct_permutations
import numpy as np
import time
import math

sleep_time = 10
# sleep_time: time between each url request to not alert web crawlers defenses

print("One last warning: Google and Youtube have defenses setup against web crawlers.\nThere is a possibility that your IP will be blocked from Google and Youtube\nif they detect and take action against this web crawler if you use it.")


def find_time_ms(identifier="dQw4w9WgXcQ", toTerm=False):
    url = "https://www.youtube.com/watch?v=" + identifier
    time.sleep(sleep_time)
    f = urllib.request.urlopen(url)
    data = f.read().decode('utf-8')
    location = data.find("approxDurationMs")
    if location == -1:
        if toTerm:
            print("Duration not found\nidentifier probably does not exist or not public")
        return -1
    # it looks like this in the string (" included)
    # "approxDurationMs": "123456"
    # the time is in milliseconds and an approximation meaning it can change each call

    not_found = True
    shifted = 15  # start shifted 15 to the left to skip looping through 'approxDurationMs'
    counter = 0
    start_time = 0
    stop_time = 0
    while not_found:
        shifted += 1
        if data[location + shifted] == '"':
            counter += 1
            if counter == 2:
                start_time = location + shifted + 1
            if counter == 3:
                stop_time = location + shifted
                not_found = False
    time_ms = int(data[start_time:stop_time])
    if toTerm:
        print(time_ms)
        return
    else:
        return time_ms


def url_generator_and_checker(desired_strs={"begin": "", "middle": [], "end": "123456789"}, optimize=True, max_atom=48, max_dig=12):
    # dict with keys as the position of the desired strings
    # possible positions: "begin", "middle", "end"
    # "begin" and "end" will always be added to the begining and end of the url
    # "middle" will be permutated with the left over spaces

    # if optimize is True, the following characters will be left out of the random generation:
    # X, L, C, D, M, V, I, U, W
    if optimize:
        url_options = ['-', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                       'A', 'B', 'E', 'F', 'G', 'H', 'J', 'K', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'Y', 'Z',
                       'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                       'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        period_elems = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
                        'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20,
                        'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30,
                        'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40,
                        'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50,
                        'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60,
                        'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70,
                        'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80,
                        'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90,
                        'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100,
                        'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109,
                        'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}
    else:
        url_options = ["-", "_"] + [chr(i) for i in np.arange(48, 57 + 1)] + [chr(i) for i in np.arange(65, 90 + 1)] + [chr(i).lower() for i in np.arange(65, 90 + 1)]
        period_elems = {}
    video_id_len = 11

    used_chr_amount = 0
    desired_middle_amount = 0
    if "begin" in desired_strs:
        used_chr_amount += len(desired_strs["begin"])
    if "middle" in desired_strs:
        used_chr_amount += sum([len(string) for string in desired_strs["middle"]])
        desired_middle_amount = len(desired_strs["middle"])
    if "end" in desired_strs:
        used_chr_amount += len(desired_strs["end"])
    left_over_chr = video_id_len - used_chr_amount
    filler_options = combinations_with_replacement(url_options, left_over_chr)
    filler_amount = math.comb(len(url_options) + left_over_chr - 1, left_over_chr)
    update_every = 10**int(np.log10(filler_amount) - 0.5)
    permu_amount = math.factorial(left_over_chr + desired_middle_amount)

    print(f"Update every {update_every * permu_amount} out of {filler_amount * permu_amount}")
    counter = 0
    for filler in filler_options:
        counter += 1
        if counter % update_every == 0:
            print(f"{counter * permu_amount}/{filler_amount * permu_amount}")
        begin_part = ""
        end_part = ""
        middle_part_list = [*filler]
        for pos, string in desired_strs.items():
            if pos == "begin":
                begin_part += string
            if pos == "end":
                end_part += string
            if pos == "middle":
                middle_part_list += string

        middle_permut = permutations(middle_part_list)
        # amount of middle part permutations: (left_over_chr + amount of desired middle parts)!
        for middle in middle_permut:
            middle_part = "".join(middle)
            gen_url = begin_part + middle_part + end_part

            total_atomic = 0
            for elem in period_elems.keys():
            # change to loop over gen_url and check per 2 chr, 2 letter element has higher priority than 1 letter
                if elem in gen_url:
                    total_atomic += period_elems[elem]
            if total_atomic > max_atom:
                continue

            total_digit = 0
            for char in gen_url:
                if char.isdigit():
                    total_digit += int(char)
            if total_digit > max_dig:
                continue
            url_time = find_time_ms(identifier=gen_url, toTerm=False)
            if url_time != -1:
                print(gen_url, ":", url_time)
    # amount of generated urls = amount of filler combination * amount of middle part permutations

    # permutations() and the combinations_with_replacement() make
    # several duplicate urls. Cast to set can be used to filter these, but this becomes
    # very inefficient for high amounts of urls
    # a better solution would be to use `from more_itertools import distinct_permutations`
    # instead of permutations(), but i do not have the more_itertools module installed
    return


def google_search_urls(search_term="dQw4w9WgXcQ"):
    req_url = r'https://www.google.com/search?q=allinurl:[' + search_term + ']%20site:https://www.youtube.com/watch'
    req = Request(
        url=req_url,
        headers={'User-Agent': 'Mozilla/5.0'}
        # custom header to dodge web crawler defenses
    )
    response = urlopen(req).read()
    data = response.decode('utf-8')

    search_data = r'href="/url?q=https://www.youtube.com/watch%3Fv%3D'
    skipped = len(search_data)
    first_search = np.char.find(data, search_data)
    if first_search == -1:
        return []
    locations = [first_search]
    searching = True
    while searching:
        loc = np.char.find(data, search_data, start=locations[-1] + 2)
        if loc == -1:
            searching = False
            break
        locations.append(loc)

    urls = []
    for loc in locations:
        urls.append(data[loc + skipped: loc + skipped + 11])
    urls = list(set(urls))
    return urls
