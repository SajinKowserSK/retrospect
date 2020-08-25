from random import randint

def chooseTagColor(num):
    tags_class = ["vctag w-button", "pmtag w-button",
                  "ibtag w-button","entrepreneurshiptag w-button",
                  "datag w-button", "consultingtag w-button"]

    select = randint(0,5)
    return tags_class[select]




