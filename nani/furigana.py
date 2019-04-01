import MeCab
import jaconv
import re


is_text = re.compile(r"^[A-Za-z0-9]+$")
is_hira_kata = re.compile(r"^[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f]+$")


def html_furigana(text):
    words = glue_punctuation(mecab(text))
    html = ""
    for source, reading in words:
        if is_text.match(source) or not reading:
            html += source
        else:
            html += to_ruby(source, reading)

    return html


def mecab(text):
    mecab = MeCab.Tagger("")
    words = []
    # Replace spaces with forced spaces so that mecab doesn't strip them
    text = text.replace(chr(32), chr(160))
    output = mecab.parse(text).splitlines()[:-1]
    lines = [raw_line.split("\t") for raw_line in output]
    for word, info in lines:
        # Flip back spaces
        word = word.replace(chr(160), chr(32))
        elems = info.split(",")
        if len(elems) > 7:
            reading = jaconv.kata2hira(info.split(",")[7])
        else:
            reading = None
        words.append((word, reading))

    return words


punctuation = "。、！？‼️⁉️,.!?〜ー"


def glue_punctuation(words):
    new_words = []
    for source, reading in words:
        if source in punctuation:
            if not new_words:
                new_words.append((source, reading))
            elif new_words[-1][1] is None:
                new_words[-1] = ((new_words[-1][0] + source), None)
            else:
                new_words[-1] = ((new_words[-1][0] + source), new_words[-1][1] + source)
        else:
            new_words.append((source, reading))
    return new_words


def to_ruby(source, reading):
    if source == reading or is_hira_kata.match(source):
        return "<ruby><rb>%s</rb></ruby>" % source  # prevents breaking mid-word
    if source == "だ" and reading == "で":
        return "だ"
    if reading == "かおもじ" and source != "顔文字":
        return source

    first_diff, last_diff = 0, 0

    j = 0
    for i in range(len(source)):
        last_diff = i
        j = i + 1
        if source[len(source) - j] != reading[len(reading) - j]:
            break

    for i in range(len(source)):
        first_diff = i
        if source[i] != reading[i]:
            break

    before = reading[0:first_diff]
    rb = source[first_diff:len(source) - last_diff]
    rt = reading[first_diff:len(reading) - last_diff]
    after = reading[len(reading) - last_diff:]

    return (
        '<span class="nobreak">%s<ruby><rb>%s</rb><rt>%s</rt></ruby>%s</span>'
        % (before, rb, rt, after)
    )
