import pygame as pg
from os.path import join
from random import randint, choice, uniform
import json

TITLE = "Pong"
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 600
BALL_SPAWN = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)


SIZE = {
    'paddle': (30,100),
    'ball': (30,30)
        }
POS = {
    'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2),
    'opponent': (50, WINDOW_HEIGHT / 2),
    "ball": (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
       }
SPEED = {
    'player': 500,
    'opponent': 400,
    'ball': 500,
    "speed mult": 1
         }
COLORS = {
    'paddle': '#57e0ff',
    'paddle shadow': '#000212',
    'ball': (255, 56, 103, 255),
    'bg': '#eeeeee',
    "bg detail": "#00042e"
}