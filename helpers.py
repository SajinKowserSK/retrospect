from random import randint

class tagColor:
    def __init__(self, number, color):
        self.number = number
        self.color = color

def chooseTagColor(index):
    tags_class = ["consultingtag w-button", "vctag w-button",
                    "pmtag w-button", "ibtag w-button",
                  "entrepreneurshiptag w-button", "datag w-button"]


    index = index - 1
    index = index % len(tags_class)

    return tags_class[index]




