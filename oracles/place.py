import os
import random

import requests
from telegram import KeyboardButton, ReplyKeyboardMarkup

from oracles.oracle import Oracle


class PlaceOracle(Oracle):
    RADIUS_METERS = 20000

    def __init__(self, bot, update, google_place_api_key):
        super().__init__(bot, update)
        self._google_place_api_key = google_place_api_key

    def handle(self):
        location = self.update.message.location
        if not location:
            location_keyboard = KeyboardButton(text="Invia posizione", request_location=True)
            custom_keyboard = [[location_keyboard]]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard)
            return self.reply('Per consigliarti, ho bisogno della tua posizione.', reply_markup=reply_markup)
        google_place = self.choose_place(self.get_google_places(location.latitude, location.longitude))
        self.reply(f"Il posto per te è {google_place.name}.\nhttps://maps.google.com/?cid={google_place.place_id}")

    def get_google_places(self, latitude, longitude):
        response = requests.get( f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={PlaceOracle.RADIUS_METERS}&type=bar&key={self._google_place_api_key}').json()
        return response.get('results')

    @staticmethod
    def choose_place(google_places):
        return random.choice(google_places)

    @staticmethod
    def from_env(bot, update):
        return PlaceOracle(bot, update, os.environ.get("GOOGLE_PLACE_API_KEY"))
