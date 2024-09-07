from generate import neptunfej

text = input("Enter text: ")

img = neptunfej(text, scale=2, margin=(10, 10))
img.show()
# img.save("neptunfej.png")

input("Press Enter to exit...")