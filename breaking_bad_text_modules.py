import random
from typing import List, Tuple, Optional 

words_to_ignore_list = [
'a', 'be', 'by', 'for', 'from', 'I', 'in', 'is', 'it', 'of', 'the', 'to',
'casting', 'created', 'c.s.a.', 'designer', 'directed', 'director', 'edited',
'guest',  'music', 'photography', 'production', 'starring', 'written'
]


elements = {
"Ac": 89,  "Ag": 47,  "Al": 13,  "Am": 95,  "Ar": 18,  
"As": 33,  "At": 85,  "Au": 79,  "B": 5,   "Ba": 56,
"Be": 4,   "Bh": 107, "Bi": 83,  "Bk": 97,  "Br": 35,  
"C": 6,    "Ca": 20,  "Cd": 48,  "Ce": 58,  "Cf": 98,
"Cl": 17,  "Cm": 96,  "Cn": 112, "Co": 27,  "Cr": 24,  
"Cs": 55,  "Cu": 29,  "Db": 105, "Ds": 110, "Dy": 66,
"Er": 68,  "Es": 99,  "Eu": 63,  "F": 9,    "Fe": 26,  
"Fl": 114, "Fm": 100, "Fr": 87,  "Ga": 31,  "Gd": 64,
"Ge": 32,  "H": 1,    "He": 2,   "Hf": 72,  "Hg": 80,  
"Ho": 67,  "Hs": 108, "I": 53,   "In": 49,  "Ir": 77,
"K": 19,   "Kr": 36,  "La": 57,  "Li": 3,   "Lr": 103, 
"Lu": 71,  "Lv": 116, "Mc": 115, "Md": 101, "Mg": 12,
"Mn": 25,  "Mo": 42,  "Mt": 109, "N": 7,    "Na": 11,  
"Nb": 41,  "Nd": 60,  "Ne": 10,  "Nh": 113, "Ni": 28,
"No": 102, "Np": 93,  "O": 8,    "Og": 118, "Os": 76,  
"P": 15,   "Pa": 91,  "Pb": 82,  "Pd": 46,  "Pm": 61,
"Po": 84,  "Pr": 59,  "Pt": 78,  "Pu": 94,  "Ra": 88,  
"Rb": 37,  "Re": 75,  "Rf": 104, "Rg": 111, "Rh": 45,
"Rn": 86,  "Ru": 44,  "S": 16,   "Sb": 51,  "Sc": 21,  
"Se": 34,  "Sg": 106, "Si": 14,  "Sm": 62,  "Sn": 50,
"Sr": 38,  "Ta": 73,  "Tb": 65,  "Tc": 43,  "Te": 52,  
"Th": 90,  "Ti": 22,  "Tl": 81,  "Tm": 69,  "Ts": 117,
"U": 92,   "V": 23,   "W": 74,   "Xe": 54,  "Y": 39,   
"Yb": 70,  "Zn": 30,  "Zr": 40
}


def break_it_bad(input_text: List[str], max_words_to_change: int):
    """
    Takes a list of strings and returns them with formatting
    that is reminiscent of the Breaking Bad TV series title sequence.
    The formatting is based on matches to a list of chemical elements where matches
    are highlighted in green+bold text.
    :param max_words_to_change: max num. of words to be highlighted per line
    :param input_text: a list of strings
    :return output_text: a formatted list of: strings and lists_of_strings
    """
    output_text: List[str] = []
    elements_matched: List[str] = []  # a list of any elements matched 
    for each_line in input_text:  # process each string found in the input list
        processed_text, elements_matched = lines_into_words(each_line, max_words_to_change, elements_matched)
        output_text.append(processed_text)
    return output_text, elements_matched


def lines_into_words(input_line_string: str, max_words_to_change: int, 
                          elements_matched: List[str]) -> Tuple[str, List[str]]:
    """
    Takes a line of text as a string and breaks this into a list of words.
    Generates a randomised index list (word_sequence) to sequence the order in which the words are processed.
    Each word in the list is sent, as per 'word_sequence', to 'words_into_chars()' and each returned word is used to
    re-assembled the string (now including any formatting changes) which is then returned.
    :param elements_matched: the list containing any matches made
    :param input_line_string: a string
    :param max_words_to_change: how many formatting changes should be made in each line of text
    :return: output_line_string: text with formatting changes
    :return: elements_matched: a list of matched elements (str)
    """
    
    output_line_string: str = ""
    num_words_changed: int = 0  # a count of words changed in each line being processed

    input_line_word_list: List[str] = input_line_string.split()  # creates a list containing the words from this line of text
    output_line_word_list: List[str] = [""] * len(input_line_word_list)  # a list to contain the output as received from word_scan

    # creates a list of random indexes (matching the number of words in the input text)
    word_sequence = generate_word_sequence(len(input_line_word_list))

    # Iterate through the random indexes in word_sequence to grab each word in turn and...
    #   check if we should bypass processing for this word, or, if not...
    #       send the word to `words_into_chars`.
    # The word (potentially with formatting changes) is added into `output_line_string` to re-create the text.
    for i in word_sequence:
        # get each word in turn
        word: str = input_line_word_list[i]
        if not (( any(word.lower() == item.lower() for item in words_to_ignore_list)) or (num_words_changed == max_words_to_change) or len(word) < 2):
            # If none of these condition are true...
            #   then send the word to be processed into chars and checked against the elements list for matches
            word, char_match_found, elements_matched = words_into_chars(word, elements_matched)
            if char_match_found is True: # Were chars in the word changed?
                num_words_changed += 1
        output_line_word_list[i] = word # update the output
        
    # Change from a list of strings back to a string
    for word in output_line_word_list:
        output_line_string += word + " "

    return output_line_string, elements_matched


def words_into_chars(input_word: str, elements_matched: List[str]) -> Tuple[str, bool, List[str]]:
    """
    Takes a text string and breaks this into a list of chars which is then used to generate 2-letter 
    and 1-letter search terms that are sent to is_an_element to check if they are indeed elements.
    The following preferences are given: 2-char un-used matches, 1-char un-used matches,
    2-char previously used matches, 1-char previously used matches.
    Where matches are mader char formatting is changed to reflect this before the string is returned.
    :param input_word: string to broken down into chars
    :param elements_matched: a list of strings containing any matches made
    :return: word: input string (that may or may not be reformatted)
    :return: char_match_found: bool
    :return: elements_matched, a list of all elements that have been matched
    """

    matched_element: str = ""
 
    # convert the input into a list of chars
    list_of_chars: List[str] = [letter for letter in input_word]
    
    # Try for unused (not already listed in elements_matched) 2-char matches
    for i in range(1, len(list_of_chars)):  # get a 2 char search term
        search_chars: str = list_of_chars[i - 1] + list_of_chars[i]
        if search_chars.lower() not in elements_matched:  # try novel matches only
            char_match_found, matched_element = is_an_element(search_chars)
            if char_match_found is True:
                elements_matched.append(search_chars.lower())
                # exit with a match (if found)
                return (format_word(input_word, search_chars, matched_element), char_match_found,
                        elements_matched)

    # Try for unused (not already listed in elements_matched) 1-char matches
    for i in range(0, len(list_of_chars)):  # try a one char match
        search_chars: str = list_of_chars[i]
        if search_chars.lower() not in elements_matched:  # try novel matches only
            char_match_found, matched_element = is_an_element(search_chars)
            if char_match_found is True: 
                elements_matched.append(search_chars.lower())
                # exit with a match (if found)
                return (format_word(input_word, search_chars, matched_element), char_match_found,
                        elements_matched)
                
    # Try for 2-char matches (accepting previously used matches) 
    for i in range(1, len(list_of_chars)):  # get a 2 char search term
        search_chars: str = list_of_chars[i - 1] + list_of_chars[i]
        char_match_found, matched_element = is_an_element(search_chars)
        if char_match_found is True:
            elements_matched.append(search_chars.lower())
            # exit with a match (if found)
            return (format_word(input_word, search_chars, matched_element), char_match_found,
                    elements_matched)

    # Try for 1-char matches (accepting previously used matches)
    for i in range(0, len(list_of_chars)):  # try a one char match
        search_chars: str = list_of_chars[i]
        char_match_found, matched_element = is_an_element(search_chars)
        if char_match_found is True: 
            elements_matched.append(search_chars.lower())
            # exit with a match (if found)
            return (format_word(input_word, search_chars, matched_element), char_match_found,
                    elements_matched)
        else:
            pass

    # if we haven't exited by finding a match above:
    char_match_found = False
    return input_word, char_match_found, elements_matched


def is_an_element(search_chars: str) -> Tuple[bool, str]: 
    """
    Takes an input string and checks if it's in 'elements_dict'.
    :param search chars: two or one char search term
    :return: char_match_found: bool
    :return: match_found, the element that was matched
    """
    for symbol in elements.keys():
        if  symbol.lower() == search_chars.lower():
            char_match_found = True
            return char_match_found, symbol  # if a match is found: is_an_element
    char_match_found = False
    return char_match_found, ""   # if no match is found

def generate_superscript_number(number: str): 
    """
    Takes some numbers as strings and uses a map to convert each digit to superscript.
    :param: number - integer as string
    :return: the same number as a superscript string
    """
    super_map = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    return ''.join(super_map.get(digit, digit) for digit in number)

def format_word(input_word: str, search_chars: str, matched_element: str) -> str:
    """
    Takes an input string and a sub-string and highlights where they match using bold green formatting.
    The capitlisation is taked from the original list of checmical elements (rather than the lower case list
    that is used when searching for matches). 
    :param: input_word - the text string to be formatted. 
    :param: search_chars - used to get the index of the matched term in the elements lists and to split the input word.
    :return: the reformatted text string.
    """

    superscript_number  = generate_superscript_number(str(elements.get(matched_element)))
  

    return (f"[white]{input_word.split(search_chars)[0]}[bold white on green]{matched_element}{superscript_number}"
            f"[/bold white on green]{input_word.split(search_chars)[1]}") 


def generate_word_sequence(specified_length: int) -> List:
    """
    Generates a list, of specified length, of integers (always including 0) in random order.
    These are used to randomize the order in which words are sent to word_scan to prevent
    matches being biased towards the front of longer lines of text.
    :param: specified_length
    :return: word_sequence
    """
    word_sequence: List = []
    while len(word_sequence) < specified_length:
        index_num = random.randint(0, specified_length-1)
        if index_num not in word_sequence:
            word_sequence.append(int(index_num))
    return word_sequence
