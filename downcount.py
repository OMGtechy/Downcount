#!/usr/bin/env python

"""
    This file is part of Downcount.

    Downcount is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Downcount is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Downcount.  If not, see <http://www.gnu.org/licenses/>.
"""

import itertools
import argparse

def parse_options():
    parser = argparse.ArgumentParser(description = "Solve anagrams and sub-anagrams")

    parser.add_argument("--word-list", dest = "word_list", help = "The word list to check against", required = True)
    parser.add_argument("--phrase", type = str.lower, dest = "phrase", help = "The phrase to check for [sub-]anagrams of", required = True)

    return parser.parse_args()

def postprocess_word_list(word_list):
    def postprocess(word):
        lowered = word.lower()
        return lowered, sorted(lowered)

    return map(postprocess, word_list)

def read_word_list(filename):
    with open(filename, "r") as word_list_file:
        return word_list_file.read().splitlines()

def get_sorted_subphrases(anagram):
    def gen():
        for anagram_length in range(1, len(anagram)):
            for sub_anagram in itertools.combinations(anagram, anagram_length):
                yield sorted("".join(sub_anagram))

    return [x for x in gen()]

if __name__ == "__main__":
    options = parse_options()

    word_list_tuples = postprocess_word_list(read_word_list(options.word_list))
    phrases = [sorted(options.phrase), ] + get_sorted_subphrases(options.phrase)

    matches = set()

    for word_tuple in word_list_tuples:
        for phrase in phrases:
            if phrase == word_tuple[1]:
                matches.add(word_tuple[0])

    if len(matches) > 0:
        print(str(len(matches)) + " " + ("matches" if len(matches) > 1 else "match") + "!")
        print("-" * 20)
    else:
        print("No matches...")

    for match in sorted(matches, key = lambda m: len(m)):
        print(match)
 
