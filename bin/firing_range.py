
def uzi(bullet):
    print "Uzi %s %s" % (bullet[0], bullet[1])
def ak47(bullet):
    print "Ak %s" % (bullet)
def water(bullet, clip):
    print "Water %s %s" % (bullet, clip)

my_dict = {
    "one": "fun",
    "two": uzi,
    "three": ak47,
    "four": water
}

args = ["bang"]
args1 = ["bing", "bong"]

my_dict["three"](args1, args)

