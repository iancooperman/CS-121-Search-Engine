import re

# lemmatize a string of ascii characters
# assuming individual words as input
def lemmatization(word: str) -> str:
    word = word.lower()

    step1_result = _step1(word)
    step2_result = _step2(step1_result)
    step3_result = _step3(step2_result)
    step4_result = _step4(step3_result)
    step5_result = _step5(step4_result)
    return step5_result



def _replacement(word, pattern, sequence):
    matches_pattern = re.match(pattern, word)
    if matches_pattern:
        return matches_pattern.group(1) + sequence


# Step 1 of lemmatization as outlined in the slides
def _step1(word: str) -> str:
    has_sess = re.match(r"(.*)sses", word)
    if has_sess:
        return has_sess.group(1) + "ss"


    _replacement()

    has_ies = re.match(r"(.*)ies", word)
    if has_ies:
        return has_ies.group(1) + "i"





# Step 2 of lemmatization as outlined in the slides
def _step2(word: str) -> str:
    return word


# Step 3 of lemmatization as outlined in the slides
def _step3(word: str) -> str:
    return word


# Step 4 of lemmatization as outlined in the slides
def _step4(word: str) -> str:
    return word


# Step 5 of lemmatization as outlined in the slides
def _step5(word: str) -> str:
    return word
