
from difflib import SequenceMatcher
import Levenshtein


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


print(similar("samh", "sam"))
print(Levenshtein.ratio("samh", "sam"))
