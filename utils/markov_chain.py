from collections import defaultdict
from dataclasses import dataclass
from random import choices
from math import floor

@dataclass
class State:
    word: str
    occurences: int
    probability: float

    def __eq__(self, value):
        return self.word == value
    
    def __repr__(self):
        return f"<State word:{self.word}, occurences:{self.occurences}, probability:{self.probability}>"
    
    def __hash__(self):
        return self.word.__hash__()


class MarkovChain:
    def __init__(self):
        self.__states = defaultdict(list)
        self.__start_state = State("", 0, 0.0)

    def train(self, text):
        lines = text.splitlines()
        for line in lines:
            words = line.split()
            for idx, word in enumerate(words):
                if idx == 0:
                    if word in self.__states[self.__start_state]:
                        self.__states[self.__start_state][self.__states[self.__start_state].index(word)].occurences += 1
                    else:
                        self.__states[self.__start_state].append(State(word, 1, 0.0))
                try:
                    next_word = words[idx + 1]
                    if next_word in self.__states[word]:
                        self.__states[word][self.__states[word].index(next_word)].occurences += 1
                    else:
                        self.__states[word].append(State(next_word, 1, 0.0))
                except IndexError:
                    self.__states[word].append(State("", 1, 1.0))

    def next(self, word, iteration=0):
        if self.__states[word]:
            total_occurences = sum([w.occurences if w != "" else min(iteration, w.occurences) for w in self.__states[word]])
            return choices(self.__states[word], [w.occurences / total_occurences if w != "" else min(iteration / total_occurences, w.occurences / total_occurences) for w in self.__states[word]])[0].word
        else:
            return ""

    def generate(self, seed=None, length=None):
        if seed:
            generated = seed + " "
        else:
            seed = self.__start_state.word
            generated = ""
        count = 0
        while True:
            seed = self.next(seed, max(floor(count / 10), 1))
            if seed:
                generated += seed + " "
                count += 1
                if length and count >= length:
                    break
            else:
                break
        return generated

if __name__ == "__main__":
    with open("messages.txt", "r") as f:
        text = f.read()

    mc = MarkovChain()
    mc.train(text)
    print(mc.generate())