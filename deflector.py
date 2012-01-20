'''
Deflectouch

Copyright (C) 2012  Cyril Stoller

For comments, suggestions or other messages, contact me at:
<cyril.stoller@gmail.com>

This file is part of Deflectouch.

Deflectouch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Deflectouch is distributed in the hope that it will be fun,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Deflectouch.  If not, see <http://www.gnu.org/licenses/>.
'''


import kivy
kivy.require('1.0.9')

from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scatter import Scatter

from kivy.graphics.transformation import Matrix
from kivy.vector import Vector
from math import atan2


class Deflector(Scatter):
    touch1 = ObjectProperty(None)
    touch2 = ObjectProperty(None)
    
    end_point1 = ObjectProperty(None)
    end_point2 = ObjectProperty(None)
    
    deflector_line = ObjectProperty(None)
    
    lenght = NumericProperty(0)
    
    '''
    ####################################
    ##
    ##   Class Initialisation
    ##
    ####################################
    '''
    def __init__(self, **kwargs):
        super(Deflector, self).__init__(**kwargs)
        
        # I create the two points and the line exactly under the two fingers.
        # They can be moved and scaled from within this class now.
        
        # Create the two points
        self.end_point1.pos = self.touch1.pos - self.end_point1.size
        self.end_point2.pos = self.touch2.pos - self.end_point2.size
        
        # Create the line:
        self.lenght = Vector(self.touch1.pos).distance(self.touch2.pos).length()
        self.deflector_line.points = self.touch1.pos, self.touch2.pos
        
        # We have to adjust the bounding box of ourself to the dimension of all the canvas objects (Do we have to?)
        #self.size = 
        
        # Now we finally grab both touches we received
        self.touch1.grab(self)
        self.touch2.grab(self)
    
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    '''
    def on_touch_down(self, touch):
        
        if not self.collide_point(*touch.pos):
            return False
        
        # This event handler is only used to ensure that transforming the scatter is exclusively possible on the two end points
        if self.end_point1.collide_point(*touch.pos) or self.end_point2.collide_point(*touch.pos):
            # if the user touched one of the end points (valid touch), dispatch the touch to the scatter
            print 'end point touched - dispatching to scatter'
            return super(Deflector, self).on_touch_down(touch)
        else:
            # if not, keep the touch
            print 'no end point touched'
            return True
    '''
    
    '''
    ####################################
    ##
    ##   On Touch Up
    ##
    ####################################
    '''
    '''
    def on_touch_up(self, touch):
        # remove the two grabbed touches from the list
        if self.touch1 in self._touches and self.touch1.grab_state:
            self.touch1.ungrab(self)
            del self._last_touch_pos[self.touch1]
            self._touches.remove(self.touch1)
        if self.touch2 in self._touches and self.touch2.grab_state:
            self.touch2.ungrab(self)
            del self._last_touch_pos[self.touch2]
            self._touches.remove(self.touch2)
    '''
    
    '''
    ####################################
    ##
    ##   Graphical Functions
    ##
    ####################################
    '''
    def create_circle(self, touch):
        # create the circle image
        circle = Image(
            source=self.app.config.get('Advanced', 'CircleImage'),
            color=(.7, .85, 1, 1),
            allow_stretch=True,
            size=(self.app.config.getint('Advanced', 'CircleSize'), self.app.config.getint('Advanced', 'CircleSize')))
        
        # center the circle on the finger position
        circle.x = touch.x - circle.size[0] / 2
        circle.y = touch.y - circle.size[1] / 2
        
        self.add_widget(circle)
        
        # and just right fade it out after having displayed it
        animation = Animation(
            color=(.7, .85, 1, 0),
            size=(self.app.config.getint('Advanced', 'CircleSize') * 2, self.app.config.getint('Advanced', 'CircleSize') * 2),
            x=circle.pos[0] - (self.app.config.getint('Advanced', 'CircleSize')/2), # workaround for centering the image during resizing
            y=circle.pos[1] - (self.app.config.getint('Advanced', 'CircleSize')/2), # workaround for centering the image during resizing
            t='out_expo', duration=2)
        
        animation.start(circle)
        animation.bind(on_complete=self.circle_fadeout_complete)
    
    def circle_fadeout_complete(self, animation, widget):
        self.remove_widget(widget)
