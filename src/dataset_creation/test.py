import pytest

from dataset_creation.parsers import filter_symbols, correct_punctuation


def test_filter_symbols_english_letters():
    input_string: str = "abcABC"

    assert filter_symbols(input_string) == input_string

def test_filter_symbols_russian_letters():
    input_string: str = "абвАБВ"

    assert filter_symbols(input_string) == input_string

def test_filter_symbols_numbers():
    input_string: str = "0123456789"

    assert filter_symbols(input_string) == input_string

def test_filter_symbols_spaces():
    input_string: str = "   "

    assert filter_symbols(input_string) == input_string

def test_filter_symbols_special_symbols():
    input_string: str = "—!?.,-+=@;:'" + '"' + "_«»*"

    assert filter_symbols(input_string) == input_string

def test_filter_symbols_wrong_symbols():
    input_string: str = "()#$%^[]{}"

    assert filter_symbols(input_string) == ""


testdata: list[tuple[str, str]] = [
    ("— Я ухожу]]], — говорит женщин{а но()()вой няне##","— Я ухожу, — говорит женщина новой няне"),
    ("Муж&&ик во>зв%ращается из ко^манд<ировки,", "Мужик возвращается из командировки,")
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_filter_symbols_random_input(input_string: str, answer: str):
    assert filter_symbols(input_string) == answer

def test_correct_punctuation_casual_test():
    input_string: str = "Привет,  Адрей.        Как ты?    "

    assert correct_punctuation(input_string) == "Привет, Адрей. Как ты? "


testdata = [
    ("Я.Тебя.Люблю.", "Я. Тебя. Люблю. "),
    ("Привет . ", "Привет. "),
    ("Рад.  Тебя.  Видеть.  ", "Рад. Тебя. Видеть. "),
    ("Атака  .   Титанов  .   ", "Атака. Титанов. "),
    ("Атака  ..   Титанов  ...   ", "Атака. Титанов. "),
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_dots(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("Давно!Не!Виделись!", "Давно! Не! Виделись! "),
    ("Армин ! Сейчас ! ", "Армин! Сейчас! "),
    ("Огонь!  ", "Огонь! "),
    ("К  !   тебе  !   жившей  !   2000  !   лет  !   назад  !   ",
        "К! тебе! жившей! 2000! лет! назад! "),
    ("Было!время!!", "Было! время! "),
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_exclamation_points(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("Давай?", "Давай? "),
    ("За ? Человечество ? ", "За? Человечество? "),
    ("Сражайся?  Сражайся?  ", "Сражайся? Сражайся? "),
    ("Я  ?   сломаю  ?   колесо  ?   ", "Я? сломаю? колесо? "),
    ("Если?убьёт??то???умрёшь????", "Если? убьёт? то? умрёшь? "),
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_question_marks(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("Брат:2:", "Брат: 2: "),
    ("Как : тебя : зовут", "Как: тебя: зовут"),
    ("Трогай:  ", "Трогай: "),
    ("Мы  :   не  :   сеем  :   ", "Мы: не: сеем: "),
    ("Вперёд:на::смерть:::", "Вперёд: на: смерть: ")
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_colons(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("Услышь;мой;рёв;", "Услышь; мой; рёв; "),
    ("Вырастая ;  крепнем", "Вырастая; крепнем"),
    ("Нам;  ярость;  ", "Нам; ярость; "),
    ("Зима  ;   близко  ;   ", "Зима; близко; "),
    ("Жизнь;полна;;разочаровний;;;", "Жизнь; полна; разочаровний; ")
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_semicolons(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("Вставай,", "Вставай, "),
    ("За , Альянс , ", "За, Альянс, "),
    ("Я,  Ахиллес,  сын,  Пелея,  ", "Я, Ахиллес, сын, Пелея, "),
    ("Прохода  ,   нет  ,   ", "Прохода, нет, "),
    ("Именем,короля,,", "Именем, короля, "),
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_commas(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("—Здравствуй", " — Здравствуй"),
    ("Я—хочу—кушать—", "Я — хочу — кушать — "),
    ("А——ты", "А — ты"),
    (" —  Нет   —    ", " — Нет — "),
    ("Чёрные—или——зелёные", "Чёрные — или — зелёные"),
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_dashes(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer


testdata = [
    ("«А", " «А"),
    (" «Б", " «Б"),
    ("  «В", " «В"),
    ("Г»", "Г» "),
    ("Д» ", "Д» "),
    ("Е»  ", "Е» "),
    ("«Привет»", " «Привет» "),
]

@pytest.mark.parametrize("input_string, answer", testdata)
def test_correct_punctuation_quotes(input_string: str, answer: str):
    assert correct_punctuation(input_string) == answer