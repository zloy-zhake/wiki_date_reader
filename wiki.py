import sys

from wiki_utils import get_article_sections, input_date, read_text


def main():
    # күнді еңгізу (КК.АА)
    date_str = input_date()

    # wiki-парақшаны жүктеп алу
    # парақшадан деректерді dict-ке оқу
    sections_dict = get_article_sections(article_title=date_str)

    # бір тақырыпатты тандау
    # тексті оқу
    while True:
        print()
        print("1: Басқа күнді еңгізу")
        sections_dict_keys = list(sections_dict.keys())
        for i, key in enumerate(sections_dict_keys, start=2):
            print(f"{i}: {key}")
        print("0: Программадан шығу")
        print()

        choice = int(input("Сізді қызықтыратын пунктті таңдаңіз: "))
        print()

        if choice == 0:
            sys.exit()

        elif choice == 1:
            date_str = input_date()
            sections_dict = get_article_sections(article_title=date_str)

        else:
            section_to_read = sections_dict_keys[choice - 2]
            read_text(text=sections_dict[section_to_read])


if __name__ == "__main__":
    main()
