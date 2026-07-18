'''
A tween is a special method of an object. Each tween needs to be preceded by the @tween decorator, 
and needs to define an update() function, and return it.

An example of a tween would be:

class Game:
    def __init__(self):
        pass
    
    @tween
    def interpolate(self, value, start, end):
        def update(t):
            nonlocal value
            value = start + t(end-start)
        return update


The entirety of tweens structure is a bit complex: there is a lot of syntactic sugar that makes them easier
to use at high level, but controversial in their implementation and construction.
'''

import pygame
import numpy as np
from functools import wraps
from types import FunctionType as function
from project.utils import accepts_kwarg


def tween(func):
    @wraps(func)
    def wrapper(*args, duration: float = 1.0, easing_func: function = lambda t: t, on_end: function = lambda: None, **kwargs):
        if args:
            if isinstance(args[0], TweenObject):
                self = args[0]
                
                # If you need to access duration, easing_func, on_end within the tween, you can
                if accepts_kwarg(func, "duration"):
                    kwargs["duration"] = duration
                if accepts_kwarg(func, "easing_func"):
                    kwargs["easing_func"] = easing_func
                if accepts_kwarg(func, "on_end"):
                    kwargs["on_end"] = on_end

                def tween():
                    return func(*args, **kwargs), duration, easing_func, on_end
                tween._is_tween = True
                self.tween_manager.add_sequential(tween)
    wrapper._is_tween = True
    return wrapper


class TweenManager:
    def __init__(self):
        self.tween_streams: list[list[dict]] = []


    def add_sequential(self, tween: function):
        # Return error if the function passed isn't a state (i.e doesn't have the @state decorator)
        if not getattr(tween, '_is_tween', False):
            raise TypeError(f"{tween.__name__} is not a tween")
        tween_data = tween()
        if not self.tween_streams:
            self.tween_streams.append([])
        self.tween_streams[-1].append(
            {
                "update": tween_data[0],
                "duration": tween_data[1],
                "easing_func": tween_data[2],
                "on_end": tween_data[3],
                "time": 0.0
            }
        )
    

    def new_tween_stream(self):
        self.tween_streams.append([])
    

    def add_parallel(self, tween: function):
        self.new_tween_stream()
        self.add_sequential(tween)
    

    def do(self, func: function):
        if not self.tween_streams:
            func()
            return
        if not self.tween_streams[-1]:
            func()
            return
        self.tween_streams[-1][-1]["on_end"] = func


    def update(self, dt):
        for stream in self.tween_streams.copy():
            if not stream:
                self.tween_streams.remove(stream)
                continue
            tween = stream[0]
            if tween["time"] >= tween["duration"]:
                tween["on_end"]()
                stream.remove(tween)
                continue
            tween["update"](tween["easing_func"](tween["time"]/tween["duration"]))
            tween["time"] += dt


class TweenObject:
    def __init__(self):
        super().__init__()
        self.tween_manager = TweenManager()

    @tween
    def wait(self):
        return lambda t: None

    @tween
    def interpolate(self, value: np.ndarray, start: np.ndarray | function, end: np.ndarray | function):
        just_began = True
        fixed_start = None
        fixed_end = None
        def update(t):
            nonlocal value, start, end, just_began, fixed_start, fixed_end
            # At the beginning, make sure that start and end are up to date (they could depend on time)
            if just_began:
                if callable(start):
                    start = start()
                if callable(end):
                    end = end()
                just_began = False
                fixed_start = start.copy()
                fixed_end = end.copy()
            value += (fixed_start-value) + t*(fixed_end-fixed_start)
        return update


    def move_to(self, value: np.ndarray, dest: np.ndarray, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        self.interpolate(value=value, start=value, end=dest, duration=duration, easing_func=easing_func, on_end=on_end)


    def move(self, value: np.ndarray, by: np.ndarray, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        self.move_to(value=value, dest=lambda: value+by, duration=duration, easing_func=easing_func, on_end=on_end)

    @tween
    def fade_in(self, surface: pygame.Surface):
        def update(t):
            surface.set_alpha(int(255*t))

        return update
    
    @tween
    def fade_out(self, surface: pygame.Surface):
        def update(t):
            surface.set_alpha(int(255*(1-t)))

        return update


    def fade_in_out(self, surface: pygame.Surface, duration_in, duration, duration_out):
        '''NOTE: This is not a tween!'''
        self.fade_in(surface, duration=duration_in)
        self.wait(duration=duration)
        self.fade_out(surface, duration=duration_out)

    # Does this thing, but after the current last tween in the stream
    def do(self, func: function):
        self.tween_manager.do(func)

    # Adds a new stream of tweens
    def new_tween_stream(self):
        self.tween_manager.new_tween_stream()
    

    def update(self, dt):
        self.tween_manager.update(dt)

