#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A card graphics generator for planning poker, a.k.a. Scrum poker.'''

# This file is part of CBG.
#
# CBG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CBG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CBG.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014-2016 Viktor Eikman


###########
# IMPORTS #
###########

# Standard library:
import string

# Third party:
import cbg
import cbg.svg.wardrobe as cw


#############
# CONSTANTS #
#############

RED = ('#cc0000',)


###########
# CLASSES #
###########

class CardPresenter(cbg.svg.card.CardFront):
    '''This is the main card presenter (SVG group generator).

    It's got a standard size representing a full card, and a wardrobe
    that's only good for drawing a simple frame around the card.

    '''
    size = cbg.sample.size.SHORT_EURO
    Wardrobe = cbg.sample.wardrobe.Frame


class StoryPointPresenter(cbg.svg.presenter.TextPresenter):
    '''An SVG generator for showing a big number, or a Japanese character.'''

    class Wardrobe(cbg.sample.wardrobe.MiniEuroMain):
        font_size = 35
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_CHARTER,
                                  middle=True, bold=True),
                 'square': cw.Mode(font=cw.Font('Ume Mincho',
                                                width_to_height=1),
                                   middle=True, bold=True)}

    def set_up_paragraph(self):
        '''An override for switching fonts depending on content.

        This is needed because non-digit characters are East Asian and
        look too blocky with default handling.

        '''
        if str(self.field[0])[0] not in string.digits:
            self.wardrobe.set_mode('square')


class PriorityPresenter(cbg.svg.presenter.TextPresenter):
    '''An SVG generator for showing a number in red, upside down.

    Using a cursor from the bottom of the card, this presenter will show
    its field's content at the bottom of the card face.

    '''

    class Wardrobe(cbg.sample.wardrobe.MiniEuroMain):
        font_size = 25
        line_height_factor = 1.05
        modes = StoryPointPresenter.Wardrobe.copy_modes(fill_colors=RED)
        transformations = [cbg.svg.transform.Rotate(180)]

    cursor_class = cbg.cursor.FromBottom

    def set_up_paragraph(self):
        '''Don't start at the very bottom. Leave some room.'''
        self.line_feed()


class PlanningPokerCard(cbg.content.card.Card):
    '''The model for a card's content, independent of its presentation.

    This class contains just a little bit of data instructing CBG in
    how to interpret the YAML specification file before trying to draw.

    '''

    class StoryPointsField(cbg.content.text.TextField):
        '''The main field on a card, representing a story point estimate.'''
        key = 'story'
        presenter_class_front = StoryPointPresenter

    class PriorityValueField(cbg.content.text.TextField):
        '''A secondary field representing a priority estimate.'''
        key = 'prio'
        presenter_class_front = PriorityPresenter

    plan = (StoryPointsField, PriorityValueField)
    presenter_class_front = CardPresenter


#############
# EXECUTION #
#############

def main():
    app = cbg.app.Application('planning poker', {'ppoker': PlanningPokerCard})
    return app.execute()

if __name__ == '__main__':
    status = main()
    exit(status)
