## Planning poker SVG generator

This Python program generates an SVG image in A4 format. For convenience, the image is included under "svg" in the Git repo. Be advised that as of 2015-05, github's SVG renderer has an unorthodox interpretation of the image, so a download is recommended.

Fonts required to view or print the image: Bitstream Charter, Ume Mincho. These are not provided.

The program implements [CBG](https://github.com/veikman/cbg) v0.8.0, demonstrating a couple of small tricks beyond bare-bones usage.

### About the cards

The image produced by this program depicts a complete deck of [planning poker](https://en.wikipedia.org/wiki/Planning_poker) cards in a format close to a standard European playing card size. The format makes it easy to sleeve the cards as an alternative to lamination or printing on card stock.

This particular version of planning poker rates workpiece complexity from 1 to 64 points, with two extra cards provided to pause for discussion:

* A question mark to signify that the player needs more information.
* A character commonly used in Shift JIS art to represent a teacup, and in Japanese to mean "daybreak". It is used here to request a break.

The deck has a secondary function: estimating the rough priority of a workpiece on a scale from 1 to 9, using the red numbers. This is not normally a part of Scrum, where the product owner sets unique priorities.

### Legal

This program is licensed as detailed in the accompanying file COPYING.txt. The author hopes you will adapt it to the needs of your own team.

