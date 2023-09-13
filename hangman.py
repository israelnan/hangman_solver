#################################################################
# FILE : hangman.py
# WRITER : israel_nankencki , israelnan , 305702334
# EXERCISE : intro2cs2 ex4 2021
# DESCRIPTION: A program for running a hangman game.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES I USED: none.
# NOTES:
#################################################################


import hangman_helper as hh


def update_word_pattern(word, pattern, letter):
    """
    this function updating the current pattern in case of a correct guess.
    :param word: the word for the user to be found.
    :param pattern: the current pattern before update.
    :param letter: the letter which the player guessed correctly.
    :return: the current pattern after update.
    """
    for ind in range(len(word)):
        if word[ind] == letter:
            pattern = pattern[:ind] + letter + pattern[ind + 1:]
    return pattern


def run_single_game(words_list, score):
    """
    this function running a single game for the user finding a single word.
    :param words_list: a list with all words dedicated for the game.
    :param score: the users' initial score for this game.
    :return: the final users' score after playing a single game.
    """
    word = hh.get_random_word(words_list)
    pattern = '_' * len(word)
    wrong_guesses = []
    init_msg = "we've started the game, your word is in length " + str(len(word)) + " good luck!"
    hh.display_state(pattern, wrong_guesses, score, init_msg)
    while True:
        if '_' not in pattern or score == 0:
            break
        else:
            cur_user_input = hh.get_input()
            if cur_user_input[0] == 1:
                pattern, score = manage_single_letter_guess(word, pattern, cur_user_input[1], wrong_guesses, score)
            elif cur_user_input[0] == 2:
                pattern, score = manage_word_guess(word, pattern, cur_user_input[1], wrong_guesses, score)
            elif cur_user_input[0] == 3:
                score -= 1
                possible_words = filter_words_list(words_list, pattern, wrong_guesses)
                if len(possible_words) > hh.HINT_LENGTH:
                    possible_words = filter_to_hint_length(possible_words)
                hh.show_suggestions(possible_words)
    if score == 0:
        hh.display_state(pattern, wrong_guesses, score, "Game Over, the word you supposed to guess is " + word)
    elif pattern == word:
        hh.display_state(pattern, wrong_guesses, score, "you won the game, congrats!!")
    return score


def check_user_guess_validity(guess):
    """
    this function is checking the basic validation of the players' guess.
    :param guess: the user guess.
    :return: True if his guess is valid, False otherwise.
    """
    if len(guess) > 1:
        print('your guess is too long, you must guess a single letter in each round')
        return False
    if not guess.isalpha():
        print('sorry, but your guess must be in the alphabet')
        return False
    if guess.isupper():
        print('sorry, your guess must be lowercase letter')
        return False
    return True


def manage_single_letter_guess(word, pattern, guess, wrong_guesses, score):
    """
    this function is helping the 'single_game_function' function to manage the process for single letter guess.
    :param word: the word to be found in this single game.
    :param pattern: the current pattern in the game.
    :param guess: the single letter guess.
    :param wrong_guesses: a list with all wrong guess maid by the player in this game.
    :param score: the current score of the player.
    :return: tuple with the updated pattern and score.
    """
    if check_user_guess_validity(guess):
        if guess in pattern:
            hh.display_state(pattern, wrong_guesses, score, "you've already guessed this letter")
        else:
            score -= 1
            if guess not in word and guess not in wrong_guesses:
                wrong_guesses.append(guess)
                hh.display_state(pattern, wrong_guesses, score, "you've guessed it wrongly, "
                                                                "this letter isn't in the word")
            elif guess in word:
                pattern = update_word_pattern(word, pattern, guess)
                n = (pattern.count(guess) * (pattern.count(guess) + 1)) // 2
                score += n
                hh.display_state(pattern, wrong_guesses, score, "your guess is correct, you've earned "
                                 + str(n) + " points!")
    return pattern, score


def manage_word_guess(word, pattern, guess, wrong_guesses, score):
    """
    this function is helping the 'single_game_function' function to manage the process for whole word guess.
    :param word: the word to be found in this single game.
    :param pattern: the current pattern in the game.
    :param guess: the whole word guess.
    :param wrong_guesses: a list with all wrong guess maid by the player in this game.
    :param score: the current score of the player.
    :return: tuple with the updated pattern and score.
    """
    score -= 1
    if guess == word:
        n = pattern.count('_')
        pattern = guess
        score += (n * (n + 1)) // 2
    else:
        hh.display_state(pattern, wrong_guesses, score, "we're truly sorry, but this isn't the word:(")
    return pattern, score


def filter_to_hint_length(possible_words):
    """
    this function is filtering the hint list in case of too manny fitting hints.
    :param possible_words: a list with all fitting hints.
    :return: a list with only number of hints limited.
    """
    filtered_possible_words = [possible_words[ind] for ind in range(0,
                                                                    ((hh.HINT_LENGTH - 1) * len(
                                                                        possible_words)) // hh.HINT_LENGTH,
                                                                    len(possible_words) // hh.HINT_LENGTH)]
    return filtered_possible_words


def main():
    """
    this function is running the whole games round.
    :return: None
    """
    words_list = hh.load_words('words.txt')
    score = run_single_game(words_list, hh.POINTS_INITIAL)
    number_of_games_played = 1
    if score > 0:
        while hh.play_again("you've earned so far " + str(score) + " points in " + str(number_of_games_played)
                            + " games, do you wanna play again?"):
            number_of_games_played += 1
            score = run_single_game(words_list, score)
    elif score == 0:
        if not hh.play_again("you have right now 0 points from " + str(number_of_games_played)
                         + " games you've played. you wanna starts another games round?"):
            return
        else:
            main()


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    this function filters from all words list the possible words according the current pattern.
    :param words: a list with all words dedicated to the game.
    :param pattern: the current pattern guessed by the player.
    :param wrong_guess_lst: a list with all wrong single letter guesses maid by the player.
    :return: a list with all possible words for the current pattern.
    """
    filtered_words = [word for word in words if len(word) == len(pattern) and
                      not_in_wrong_guess_filter(word, ''.join(wrong_guess_lst)) and same_letters_filter(word, pattern)]
    return filtered_words


def not_in_wrong_guess_filter(word, wrong_guess_str):
    """
    this function helps the filtering function to firstly determine whether some letters in the given word is in wrong
     guess list.
    :param word: the given word to examine.
    :param wrong_guess_str: a string joined from wrong guesses list.
    :return: False if one of the letters words' is in wrong guesses list, True otherwise.
    """
    for letter in word:
        if letter in wrong_guess_str:
            return False
    return True


def same_letters_filter(word, pattern):
    """
    this function helps the filtering function to finally determine whether the given word is fitting as a hint.
    :param word: the given word to examine.
    :param pattern: the current pattern guessed by the player.
    :return: False if the given word isn't fits as a hint , True otherwise.
    """
    only_letters_pattern = ''.join(let for let in pattern if let.isalpha())
    for letter in only_letters_pattern:
        if letter not in word:
            return False
        elif word.count(letter) > only_letters_pattern.count(letter):
            return False
    for ind in range(len(word)):
        if pattern[ind].isalpha() and word[ind] != pattern[ind]:
            return False
    return True


if __name__ == '__main__':
    main()
