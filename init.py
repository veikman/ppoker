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


# CBG typesetting:

BITSTREAM = cbg.style.Type(cbg.sample.font.BITSTREAM_CHARTER,
                           anchor='middle', weight=cbg.style.BOLD)
UME = cbg.style.Type(cbg.style.FontFamily('Ume Mincho', 1),
                     anchor='middle', weight=cbg.style.BOLD)


# CBG subclasses:

class CardPresenter(cbg.svg.presenter.CardFront):
    size = cbg.sample.size.SHORT_EURO


class StoryPointPresenter(cbg.svg.presenter.FieldOfText):
    '''The main field on a card, representing a story point estimate.'''

    wardrobe = cbg.style.Wardrobe(cbg.size.FontSize(35, line_height_factor=1),
                                  {cbg.style.MAIN: BITSTREAM},
                                  cbg.sample.wardrobe.COLORSCHEME)

    def set_up_paragraph(self):
        '''An override for switching fonts depending on content.

        This is needed because non-digit characters are East Asian and
        look too blocky with default handling.

        '''
        if str(self.content_source[0])[0] in string.digits:
            self.wardrobe.fonts[cbg.style.MAIN] = BITSTREAM
        else:
            self.wardrobe.fonts[cbg.style.MAIN] = UME


class PriorityPresenter(cbg.svg.presenter.FieldOfText):
    '''A secondary field representing a priority estimate.'''

    wardrobe = cbg.style.Wardrobe(cbg.size.FontSize(25,
                                  line_height_factor=1.05),
                                  {cbg.style.MAIN: BITSTREAM},
                                  {cbg.style.MAIN: ('#cc0000',)})

    def set_up_paragraph(self):
        '''Print upside down, at the bottom of the card face.'''
        self.bottom_up()
        self.line_feed()
        self.cursor.transform.rotate(180)


class StoryPointsField(cbg.content.field.Field):
    key = 'story'
    presenter_class_front = StoryPointPresenter


class PriorityValueField(cbg.content.field.Field):
    key = 'prio'
    presenter_class_front = PriorityPresenter


class PlanningPokerCard(cbg.content.card.Card):
    field_classes = (StoryPointsField, PriorityValueField)
    presenter_class_front = CardPresenter


# Main:

def main():
    app = cbg.app.Application('planning poker', {'ppoker': PlanningPokerCard})
    return app.execute()


if __name__ == '__main__':
    status = main()
    exit(status)
