import json
import os
from unittest import TestCase, mock
from unittest.mock import MagicMock

import responses

from oracles.place import PlaceOracle


@mock.patch.dict(os.environ, {'GOOGLE_PLACE_API_KEY': 'api_key'})
class TestPlaceOracle(TestCase):

    def setUp(self):
        super().setUp()
        self.bot = MagicMock()
        self.update = MagicMock()
        self.chat_id = 'chat_id'
        self.update.message.chat_id = self.chat_id
        self.oracle = PlaceOracle.from_env(self.bot, self.update)

    @responses.activate
    def test_get_google_place_response(self):
        latitude = 10
        longitude = 15
        responses.add(responses.GET,
                      f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={PlaceOracle.RADIUS_METERS}&type=bar&key={os.environ.get("GOOGLE_PLACE_API_KEY")}',
                      body=get_fake_place_api(),
                      content_type='application/json')
        expected_json = json.loads(get_fake_place_api())
        self.assertEqual(expected_json.get('results'), self.oracle.get_google_places(latitude, longitude))

    def test_from_env(self):
        bot = "bot"
        update = "update"
        oracle = PlaceOracle.from_env(bot, update)
        self.assertEqual(bot, oracle.bot)
        self.assertEqual(update, oracle.update)
        self.assertEqual('api_key', oracle._google_place_api_key)

    def test_choose_place(self):
        google_places = get_fake_google_places()
        chosen_place = self.oracle.choose_place(google_places)
        self.assertIn(chosen_place.get('id'), {p.get('id') for p in google_places})


def get_fake_place_api():
    return r"""
{
   "html_attributions" : [],
   "results" : [
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8585858,
               "lng" : 151.2100415
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.85723597010728,
                  "lng" : 151.2113913298927
               },
               "southwest" : {
                  "lat" : -33.85993562989272,
                  "lng" : 151.2086916701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/bar-71.png",
         "id" : "8e980ad0c819c33cdb1cea31e72d654ca61a7065",
         "name" : "Cruise Bar, Restaurant & Events",
         "opening_hours" : {
            "open_now" : true,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 1134,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/112582655193348962755/photos\"\u003eCruise Bar, Restaurant &amp; Events\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAAL0-OYb0qjIV9bDrGo1C019JOOEnucFPrapLRL4ir88OX7KQLwwq_rvRGJmFZu0Q4XaRgMZhkI5JfGOVVGLbbtNBSy0C_5qtVQFhfJNr-Z9lZazWcbHgw_31PDCNCEOQhEhDWMHW8wZGh8W3kpZNZ8frQGhSqlOgNzwtjzest4QsAcKlE0oWzZw",
               "width" : 2048
            }
         ],
         "place_id" : "ChIJi6C1MxquEmsR9-c-3O48ykI",
         "rating" : 3.9,
         "reference" : "CmRbAAAAACqoJ8mx5nL-Ac6YkWD4TyUzxdO6lIkeqyQ-qDETxm6kNjsmFLPIWBtRlI7PUFaBYkKA01D1nI3uhBV2aJmnhPW2LRLufvcQKjbndDkhasWVDhT4VxrhJFrwamKat2RVEhB_HT13DZHhtwYVhbhfvFOlGhSXI0w4QFI44VQoanYq_QTbINkSeg",
         "scope" : "GOOGLE",
         "types" : [ "bar", "restaurant", "food", "point_of_interest", "establishment" ],
         "vicinity" : "Circular Quay W, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8609472,
               "lng" : 151.209872
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.85959737010728,
                  "lng" : 151.2112218298927
               },
               "southwest" : {
                  "lat" : -33.86229702989272,
                  "lng" : 151.2085221701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
         "id" : "9ea7c77cb181b1f33d19c9d76121fcc6d5246ad8",
         "name" : "Australian Cruise Group Circular Quay",
         "opening_hours" : {
            "open_now" : false,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 1152,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/112378780393544273770/photos\"\u003eAustralian Cruise Group Circular Quay\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAA5GVSp31-J2XaXmcHTWnK8uZp7pBL2CUas0pUyqszv-NDK3FJjokYtvLeszmLrmcYBqmr8M3-FAzjWIqgCJdMetRiYvx3_t5U8pzrIS4_v9lr2ZCqi4ALPZZAIY1Mpz05EhAIE6hQWZz6-_KOdKa4kEHIGhTVcg3I6BihnMMptEIJyHMWgCy_rw",
               "width" : 2048
            }
         ],
         "place_id" : "ChIJpU8KgUKuEmsRKErVGEaa11w",
         "rating" : 4,
         "reference" : "CmRbAAAA27X3o-rikZ67dfBvNNEnsn50CIj7OPEV1Ozg8OrNxV03SS4v7OJqhuA880PFvOxfNro9wkcvbzEN74T54sbW7UByS_xAZTjCnljYca5YS_HSWDOUe46MJd7Zb15wAmbkEhBPv9V2SqaRel0QIZAqz4J1GhR2xY11kA8q5ZHLHJkqhQPMJnoTEg",
         "scope" : "GOOGLE",
         "types" : [
            "travel_agency",
            "restaurant",
            "food",
            "point_of_interest",
            "establishment"
         ],
         "vicinity" : "6 Cirular Quay, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.867591,
               "lng" : 151.201196
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.86624117010727,
                  "lng" : 151.2025458298927
               },
               "southwest" : {
                  "lat" : -33.86894082989271,
                  "lng" : 151.1998461701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
         "id" : "a97f9fb468bcd26b68a23072a55af82d4b325e0d",
         "name" : "Australian Cruise Group",
         "opening_hours" : {
            "open_now" : false,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 417,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/110751364053842618118/photos\"\u003eAustralian Cruise Group\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAARuqS5_Hjq33k1zoO5lF_ww1sjIvQe5vU1ou_ITxAEJC_n9mlJu7v1t6Vp2wmx6ErG6l8ezBKkS5wILE_HGdsX_VC56p73OTHfLpVZO1vhVfd_eDJqD-ThdS_tDxTtPpxEhBaYnqJeceSLpVECY5MMF1mGhRDhe-BWh6Z11I-hUh0yL2PIozrWg",
               "width" : 1334
            }
         ],
         "place_id" : "ChIJrTLr-GyuEmsRBfy61i59si0",
         "rating" : 4.6,
         "reference" : "CmRbAAAAua3hRI3OoeOBbKLWkKfvT6F9m_emWljKWSdZbJ89o1k5ZEOkWh7cP6bTPnj9EDSGe5ZncyvuDJGxAPsKk2TNGrNDc2h50KoNLyiOL7bfQLKhKHlPEtGKts90c1xH5oWyEhCaQ11pHg0uxxsQ9qWyko69GhSuREi5mfF4F6Zi1rG3ixOSO6MWGg",
         "scope" : "GOOGLE",
         "types" : [
            "travel_agency",
            "restaurant",
            "food",
            "point_of_interest",
            "establishment"
         ],
         "vicinity" : "King Street, Wharf 5, 32 The Promenade, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8686058,
               "lng" : 151.2018206
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.86725597010728,
                  "lng" : 151.2031704298927
               },
               "southwest" : {
                  "lat" : -33.86995562989272,
                  "lng" : 151.2004707701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
         "id" : "21a0b251c9b8392186142c798263e289fe45b4aa",
         "name" : "Rhythmboat Cruises",
         "opening_hours" : {
            "open_now" : false,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 480,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/104066891898402903288/photos\"\u003eRhythmboat Cruises\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAAgSQGqiKlLASKKcuJUwxeLzqhgWnO-yz5vDYEjymQE7lRsK3PUl6fiVwXxsCZx0LgxbIhjBOAg7wdihVV4TFNHkEJcuhN31CxjfWw-BfFX6QFZeoMc9aFwMepXz-J-Y_6EhCacKbqWhKg-VVPlj-jD3jEGhQcAWV_r5DNBxjrlDLH_6EaNrNMcw",
               "width" : 640
            }
         ],
         "place_id" : "ChIJyWEHuEmuEmsRm9hTkapTCrk",
         "rating" : 4.1,
         "reference" : "CmRbAAAAYXmtFSafR76D3v4UdvEmbJab-4eZm0NfCMDKxbSFGl77rGOC6FdIjhWGXAR3iYUxZoQCGu5oSBXxCba7IYkKS29IcOs7Qqz0kaemAYb_R3RRmiEMPfMxfCoaQLevzndnEhCzyvsmemgLBIK8zSzRG8FGGhRFRlxNsBPGL91Ifc2MRkMdyuI6bg",
         "scope" : "GOOGLE",
         "types" : [
            "travel_agency",
            "restaurant",
            "food",
            "point_of_interest",
            "establishment"
         ],
         "vicinity" : "King Street Wharf, King St, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.867591,
               "lng" : 151.201196
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.86624117010727,
                  "lng" : 151.2025458298927
               },
               "southwest" : {
                  "lat" : -33.86894082989271,
                  "lng" : 151.1998461701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
         "id" : "b0277cade7696e575824681aba949d68814f9efe",
         "name" : "Sydney New Year's Eve Cruises",
         "opening_hours" : {
            "open_now" : false,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 1152,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/107666140764925298472/photos\"\u003eSydney New Year&#39;s Eve Cruises\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAAmQ6veGLrm4J0btlOdTp1gNPsLZf33LHlHEBDjXj9MkteM6AZytoF8gYpmRPuYm3ihLRV4CD05EK96ilXFmAJhJnLC8MJhWosLXmtB1mjWXXeyf9WWRK1j4vf5X9sVDw0EhBVUyUaHm4NAqN3SSLS1moXGhT4c1vN6lT3wAlErqpv3LfTnjO77A",
               "width" : 2048
            }
         ],
         "place_id" : "ChIJ__8_hziuEmsR27ucFXECfOg",
         "rating" : 5,
         "reference" : "CmRbAAAAKNJ2uYhBPwBFZqMOWFazyNkS7lsZi9Y8Fpn0DgaOk1_mVfSGXIl9cwMECxMNS3MszgHv2ZRLIJCl5mcEq8HG79QQYHiNOwdZunKXZSkDIdHk5LBG3-PgbdUhwVU6F1IJEhAIWg99t4AIFhVJht1Uji17GhRV0SoEXS2ecVDSkL26VPaO77698g",
         "scope" : "GOOGLE",
         "types" : [
            "travel_agency",
            "restaurant",
            "food",
            "point_of_interest",
            "establishment"
         ],
         "vicinity" : "32 The Promenade, King Street Wharf 5, Sydney"
      }
   ],
   "status" : "OK"
}
"""


def get_fake_google_places():
    return json.loads(r"""
    [
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8585858,
               "lng" : 151.2100415
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.85723597010728,
                  "lng" : 151.2113913298927
               },
               "southwest" : {
                  "lat" : -33.85993562989272,
                  "lng" : 151.2086916701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/bar-71.png",
         "id" : "8e980ad0c819c33cdb1cea31e72d654ca61a7065",
         "name" : "Cruise Bar, Restaurant & Events",
         "opening_hours" : {
            "open_now" : true,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 1134,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/112582655193348962755/photos\"\u003eCruise Bar, Restaurant &amp; Events\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAAL0-OYb0qjIV9bDrGo1C019JOOEnucFPrapLRL4ir88OX7KQLwwq_rvRGJmFZu0Q4XaRgMZhkI5JfGOVVGLbbtNBSy0C_5qtVQFhfJNr-Z9lZazWcbHgw_31PDCNCEOQhEhDWMHW8wZGh8W3kpZNZ8frQGhSqlOgNzwtjzest4QsAcKlE0oWzZw",
               "width" : 2048
            }
         ],
         "place_id" : "ChIJi6C1MxquEmsR9-c-3O48ykI",
         "rating" : 3.9,
         "reference" : "CmRbAAAAACqoJ8mx5nL-Ac6YkWD4TyUzxdO6lIkeqyQ-qDETxm6kNjsmFLPIWBtRlI7PUFaBYkKA01D1nI3uhBV2aJmnhPW2LRLufvcQKjbndDkhasWVDhT4VxrhJFrwamKat2RVEhB_HT13DZHhtwYVhbhfvFOlGhSXI0w4QFI44VQoanYq_QTbINkSeg",
         "scope" : "GOOGLE",
         "types" : [ "bar", "restaurant", "food", "point_of_interest", "establishment" ],
         "vicinity" : "Circular Quay W, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8609472,
               "lng" : 151.209872
            },
            "viewport" : {
               "northeast" : {
                  "lat" : -33.85959737010728,
                  "lng" : 151.2112218298927
               },
               "southwest" : {
                  "lat" : -33.86229702989272,
                  "lng" : 151.2085221701072
               }
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
         "id" : "9ea7c77cb181b1f33d19c9d76121fcc6d5246ad8",
         "name" : "Australian Cruise Group Circular Quay",
         "opening_hours" : {
            "open_now" : false,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 1152,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/112378780393544273770/photos\"\u003eAustralian Cruise Group Circular Quay\u003c/a\u003e"
               ],
               "photo_reference" : "CmRaAAAA5GVSp31-J2XaXmcHTWnK8uZp7pBL2CUas0pUyqszv-NDK3FJjokYtvLeszmLrmcYBqmr8M3-FAzjWIqgCJdMetRiYvx3_t5U8pzrIS4_v9lr2ZCqi4ALPZZAIY1Mpz05EhAIE6hQWZz6-_KOdKa4kEHIGhTVcg3I6BihnMMptEIJyHMWgCy_rw",
               "width" : 2048
            }
         ],
         "place_id" : "ChIJpU8KgUKuEmsRKErVGEaa11w",
         "rating" : 4,
         "reference" : "CmRbAAAA27X3o-rikZ67dfBvNNEnsn50CIj7OPEV1Ozg8OrNxV03SS4v7OJqhuA880PFvOxfNro9wkcvbzEN74T54sbW7UByS_xAZTjCnljYca5YS_HSWDOUe46MJd7Zb15wAmbkEhBPv9V2SqaRel0QIZAqz4J1GhR2xY11kA8q5ZHLHJkqhQPMJnoTEg",
         "scope" : "GOOGLE",
         "types" : [
            "travel_agency",
            "restaurant",
            "food",
            "point_of_interest",
            "establishment"
         ],
         "vicinity" : "6 Cirular Quay, Sydney"
      }
      ]""")

