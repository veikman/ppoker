#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A card graphics generator for planning poker, a.k.a. Scrum poker.

------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2015 Viktor Eikman

'''

# Standard library:
import string

# Third party:
import cbg


# Typesetting:

BITSTREAM = cbg.style.Type(cbg.fonts.BITSTREAM_CHARTER,
                           anchor='middle', weight=cbg.style.BOLD)
UME = cbg.style.Type(cbg.style.FontFamily('Ume Mincho', 1),
                     anchor='middle', weight=cbg.style.BOLD)


# CBG subclasses:

class StoryPointsValue(cbg.svg.SVGField):
    '''The main field on a card, representing a story point estimate.'''

    style = cbg.style.Wardrobe(cbg.size.FontSize(35, line_height_factor=1),
                               {cbg.style.MAIN: BITSTREAM},
                               cbg.wardrobe.COLORSCHEME)

    def __init__(self, parent):
        super().__init__(parent, self.style)

    def front(self, tree):
        '''An override for switching fonts depending on content.

        This is needed because non-digit characters are East Asian and
        look too blocky with default handling.

        '''
        self.reset()
        for paragraph in self.parent:
            if str(paragraph)[0] in string.digits:
                self.wardrobe.fonts[cbg.style.MAIN] = BITSTREAM
            else:
                self.wardrobe.fonts[cbg.style.MAIN] = UME

            self.set_up_paragraph()
            self.insert_text(tree, str(paragraph))


class PriorityValue(cbg.svg.SVGField):
    '''A secondary field representing a priority estimate.'''

    def __init__(self, parent):
        style = cbg.style.Wardrobe(cbg.size.FontSize(25,
                                                     line_height_factor=1.05),
                                   {cbg.style.MAIN: BITSTREAM},
                                   {cbg.style.MAIN: ('#cc0000',)})
        super().__init__(parent, style)

    def set_up_paragraph(self):
        '''Print upside down, at the bottom of the card face.'''
        self.bottom_up()
        self.line_feed()
        self.g.cursor.transform.rotate(180)


class PlanningPokerCard(cbg.card.HumanReadablePlayingCard):
    story_content = cbg.elements.CardContentField('story', StoryPointsValue)
    prio_content = cbg.elements.CardContentField('prio', PriorityValue)

    def process(self):
        self.dresser = cbg.svg.SVGCard(self, cbg.wardrobe.WARDROBE,
                                       size=cbg.size.SHORT_EURO)
        self.populate_fields((self.story_content, self.prio_content))


# Main:

def main():
    app = cbg.app.Application('planning poker', {'ppoker': PlanningPokerCard})
    app.execute()
    return 0


if __name__ == '__main__':
    status = main()
    exit(status)