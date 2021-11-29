import datetime
import subprocess

import wikipedia

wikipedia.set_lang("kk")


def validate_date(date_text):
    """Еңгізілген күнді тексеретін функция."""
    if len(date_text) != 5:
        raise ValueError(
            "Күн форматы дұрыс емес, КК.АА форматта болу керек "
            "(21 қараша 21.11 болу керек)."
        )
    try:
        datetime.datetime.strptime(date_text, "%d.%m")
        return True
    except ValueError:
        raise ValueError(
            "Күн форматы дұрыс емес, КК.АА форматта болу керек "
            "(21 қараша 21.11 болу керек)."
        )


def translate_date(date):
    """Күннің айын цифрлық түрінен сөздермен жазылған түріне аударатын
    функция ("21.11" -> "21_қараша")
    """
    months_dict = {
        "01": "қаңтар",
        "02": "ақпан",
        "03": "наурыз",
        "04": "сәуір",
        "05": "мамыр",
        "06": "маусым",
        "07": "шілде",
        "08": "тамыз",
        "09": "қыркүйек",
        "10": "қазан",
        "11": "қараша",
        "12": "желтоқсан",
    }

    d, m = date.split(".")
    if d.startswith("0"):
        d = d[1:]
    m = months_dict[m]

    return f"{d}_{m}"


birlikter_dict = {
    "0": "",
    "1": "бір",
    "2": "екі",
    "3": "үш",
    "4": "төрт",
    "5": "бес",
    "6": "алты",
    "7": "жеті",
    "8": "сегіз",
    "9": "тоғыз",
}


def birlik_to_text(digit):
    """Бірліктерді цифрлық түрінен сөздермен жазылған түріне аударатын
    функция
    """
    return birlikter_dict[digit]


ondyqtar_dict = {
    "0": "",
    "1": "он",
    "2": "жиырма",
    "3": "отыз",
    "4": "қырық",
    "5": "елу",
    "6": "алпыс",
    "7": "жетпіс",
    "8": "сексен",
    "9": "тоқсан",
}


def ondyq_to_text(digit):
    """Ондықтарды цифрлық түрінен сөздермен жазылған түріне аударатын
    функция
    """
    return ondyqtar_dict[digit]


def digits_to_text(digits):
    """Сандарды цифрлық түрінен бір-бір цифрдан сөздермен жазылған
    түріне аударатын функция
    """
    result = []
    for i, d in enumerate(digits[::-1]):
        if i == 0:
            result.append(birlik_to_text(d))
        elif i == 1:
            result.append(ondyq_to_text(d))
        elif i == 2 and d != "0":
            result.append(birlik_to_text(d) + " жүз")
        elif i == 3 and d != "0":
            result.append(birlik_to_text(d) + " мын")

    return " ".join(reversed(result))


def preprocess_text(text):
    """Текстті дыбыстауға дайындайтын функция"""
    # токенизация
    text = text.replace("(", " ( ")
    text = text.replace(")", " ) ")
    text = text.replace("-", " - ")
    text = text.replace("—", " — ")
    text = text.replace("«", " « ")
    text = text.replace("»", " » ")
    text = text.replace(".", " . ")
    if "жж." in text:
        text = text.replace("жж.", "жылдары")
    if " ж . " in text:
        text = text.replace(" ж . ", " жылы ")
    while "  " in text:
        text = text.replace("  ", " ")

    # сандарды сөздермен жазылған түріне аудару
    result = ""
    for token in text.split():
        if token[0].isdigit() and token[-1].isdigit():
            result += digits_to_text(digits=token) + " "
        else:
            result += token + " "

    # "бір - ші" -> "бірінші"
    if " - ші " in result:
        result = result.replace(" - ші ", "інші ")
    if " - шы " in result:
        result = result.replace(" - шы ", "ыншы ")

    # "Қаңтардың бір" -> "Қаңтардың бірі"
    if (
        result.startswith("Қаңтардың")
        or result.startswith("Ақпанның")
        or result.startswith("Наурыздың")
        or result.startswith("Сәуірдің")
        or result.startswith("Мамырдың")
        or result.startswith("Маусымның")
        or result.startswith("Шілденің")
        or result.startswith("Тамыздың")
        or result.startswith("Қыркүйектің")
        or result.startswith("Қазанның")
        or result.startswith("Қарашаның")
        or result.startswith("Желтоқсанның")
    ):
        last_digit_index = result.find(" — ") - 1
        if last_digit_index > 0:
            if (
                result[: last_digit_index + 1].endswith("бір")
                or result[: last_digit_index + 1].endswith("үш")
                or result[: last_digit_index + 1].endswith("төрт")
                or result[: last_digit_index + 1].endswith("бес")
                or result[: last_digit_index + 1].endswith("сегіз")
            ):
                result = (
                    result[: last_digit_index + 1]
                    + "і"
                    + result[last_digit_index + 1 :]
                )
            if (result[: last_digit_index + 1].endswith("екі")) or (
                result[: last_digit_index + 1].endswith("жеті")
            ):
                result = (
                    result[: last_digit_index + 1]
                    + "сі"
                    + result[last_digit_index + 1 :]
                )
            elif (
                result[: last_digit_index + 1].endswith("алты")
                or result[: last_digit_index + 1].endswith("тоғыз")
                or result[: last_digit_index + 1].endswith("он")
                or result[: last_digit_index + 1].endswith("отыз")
            ):
                result = (
                    result[: last_digit_index + 1]
                    + "ы"
                    + result[last_digit_index + 1 :]
                )
            elif result[: last_digit_index + 1].endswith("жиырма"):
                result = (
                    result[: last_digit_index + 1]
                    + "сы"
                    + result[last_digit_index + 1 :]
                )
    while "  " in result:
        result = result.replace("  ", " ")

    return result


def input_date():
    """Күнді еңгізетін функция"""
    date_from_cli = input("КК.АА форматта күнді еңгізіңіз: ")
    if validate_date(date_text=date_from_cli):
        date_str = translate_date(date=date_from_cli)
    return date_str


def get_article_sections(article_title):
    """Wikipedia мақаланы жүктеп алып, секцияларын бөлек сақтайтын
    функция
    """
    wiki_page = wikipedia.page(title=article_title)

    sections_dict = dict()

    sections = wiki_page.content.split("\n=")

    sections_dict["Жалпы деректер"] = preprocess_text(text=sections[0]).strip()
    for section in sections[1:-1]:
        section_header, section_text = section.split("=\n")
        section_header = section_header.replace("=", "")
        section_header = section_header.strip()
        section_text = preprocess_text(text=section_text)
        section_text = section_text.strip()

        sections_dict[section_header] = section_text
    return sections_dict


def read_text(text):
    """Текстті дауыспен айтатын функция"""
    subprocess.run(["python", "synthesize.py", "--text", text], cwd="..")
    subprocess.run(
        ["play", "--no-show-progress", "synthesized_wavs/example.wav"],
        cwd="..",
    )
