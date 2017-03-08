#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Libraries:
from __future__ import unicode_literals
import re
print 'Loading SpaCy library...'
from spacy.en import English
print 'Loading English...'
# Function for text processing with Spacy:
nlp = English()


##############
## Analyzer ##
##############

# This program receives a text input (message), and extracts valuable information from it within the DISEASE-TREATMENT cognitive frame, i.e. a disease and a potential solution for it.

# The Analyzer consists of 3 functions: (1) language_data_loader loads linguistic knowledge to feed the Analyzer (a simple NLP engine), (2) start_word_match finds disease mentions in the incoming text message, (3) Analyzer uses information from previous inputs to extract entities (syntactically, noun phrases) that semantically express solutions for a mentioned disease. 

# (1) Language data loader:

def language_data_loader():
    language_data = dict()
    # Load grammar:
    grammar_file = open('grammar.txt', 'r')
    grammar = []
    for l in grammar_file:
        l = l.strip()
        l = l.lower()
        grammar.append(l)
    grammar_file.close()
    language_data['grammar'] = grammar
    # Load start words (a term list to recover messages on diseases):
    start_words_file = open('start_words.txt', 'r')
    start_words = []
    for l in start_words_file:
        l = l.strip()
        l = l.lower()
        start_words.append(l)
    start_words_file.close()
    language_data['start_words'] = start_words
    # Load stop words (words tagged as noun phrases that cannot be extracted as entities (e.g. You, @username11):
    stop_words_file = open('stop_words.txt', 'r')
    stop_words = []
    for l in stop_words_file:
        l = l.strip()
        l = l.lower()
        stop_words.append(l)
    stop_words_file.close()
    language_data['stop_words'] = stop_words
    return language_data

# (2) 'start word' finder:

def start_word_match(message,start_word_list):
    start_word = ''
    for w in start_word_list:
        if re.search(w,message):
            start_word_is_now = message[re.search(w,message).start():re.search(w,message).end()]
            if len(start_word_is_now) > len(start_word):
                start_word = start_word_is_now
    # we search for the longest match ('Mindfulness for anorexia nervosa' gets 'anorexia nervosa' but not 'anorexia', although both are disease terms)
    if len(start_word) > 0:
        return start_word
    elif len(start_word) == 0:
        return '<No start word in message>'

# (3) Analyzer (treatment-entity finder)
# The input grammar follows two basic syntactic schemes, where X = treatment/solution and Y = disease/problem: 
# (a) X to treat Y -> X comes first, (b) Y treated with X -> Y comes first.

def analyzer(message,start_words,grammar,stop_words):
    # Find the start word in message:
    start_word = start_word_match(message,start_words)
    # Necessary variables:
    generated_grammar = []
    longest_march = ''
    output = []
    NP_list = []
    longest_y_match = ''
    matching_rule = ''
    # For every stored grammar rule, generate its counterpart including the start word (e.g. '[x] for [y]' -> '[x] for anorexia')
    for r in grammar:
        r_gen = r.replace('[y]',start_word)
        possible_y_match = re.sub('\s*\[x\]\s*','',r_gen)
        # Test every rule against the message:
        if re.search(possible_y_match,message):
            y_match = possible_y_match
            # Find the rule with the longest match in the string:
            if len(y_match) > len(longest_y_match):
                longest_y_match = y_match
                matching_rule = r
    # Rule matchs if 'longest_y_match' contains a string
    if len(longest_y_match) > 0:
        # The matching rule has the structure: X before Y, where X is a string potentially including the treatment entity
        if re.search('\[x\]',matching_rule).start() < re.search('\[y\]',matching_rule).start():
            x_match = message[:re.search(longest_y_match,message).start()]
            if len(x_match) > 0:
                # Search NPs within x_match (target string):
                for np in nlp(x_match).noun_chunks:
                    NP_list.append(np)
                if len(NP_list) > 0:
                    # Avoid the NP (noun phrase), if it's a stop word (e.g. You) 
                    forbidden_NP = False
                    for stop_word in language_data['stop_words']:
                        if re.search(stop_word, str(NP_list[-1])):
                            forbidden_NP = True
                    if forbidden_NP is False:
                        # Include start_word and NP in a list named 'ouput'. Choose the latest NP from the target string (e.g. 'This treatment is a medicine...' gets 'medicine' but not 'treatment')
                        output.append(NP_list[-1])
                        output.append(start_word)
                        return output
        # The matching rule has the structure: Y before X:
        elif re.search('\[x\]',matching_rule).start() > re.search('\[y\]',matching_rule).start():
            x_match = message[re.search(longest_y_match,message).end():]
            if len(x_match) > 0:
                for np in nlp(x_match).noun_chunks:
                    NP_list.append(np)
                if len(NP_list) > 0:
                    forbidden_NP = False
                    for stop_word in language_data['stop_words']:
                        if re.search(stop_word,str(NP_list[0])):
                            forbidden_NP = True
                    if forbidden_NP is False:
                        # Choose the first NP from the target string (e.g. 'treated by a medicine from the shop', gets 'medicine' but not 'shop')
                        output.append(NP_list[0])
                        output.append(start_word)
                        return output
    if len(output) == 0:
        return '<nothing found>'

### Running the code ###

language_data = language_data_loader()
print analyzer('@anastasia is a new treatment for alopecia',language_data['start_words'],language_data['grammar'],language_data['stop_words'])