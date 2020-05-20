import unittest
import matplotlib.pyplot as plt
import PIL

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

        img = plt.imread("assets/tenkeyless_layout.jpg")
        fig, ax = plt.subplots()
        ax.imshow(img)


if __name__ == '__main__':
    unittest.main()
