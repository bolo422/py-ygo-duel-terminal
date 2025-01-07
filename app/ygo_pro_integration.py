import requests

API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

class YGOProAPI:

    @staticmethod
    def search_cards(
        id=None, name=None, fname=None, konami_id=None, type=None, atk=None, def_=None,
        level=None, race=None, attribute=None, link=None, linkmarker=None, scale=None,
        cardset=None, archetype=None, banlist=None, sort=None, format=None, misc=None,
        staple=None, has_effect=None, startdate=None, enddate=None, dateregion=None
    ):
        """
        Search for cards using the YGOPro API.
        
        :param id: Card passcode (8-digit). Cannot be used with `name`.
        :param name: Exact card name. Multiple names separated by '|'.
        :param fname: Fuzzy search for cards containing this string.
        :param konami_id: Konami ID of the card.
        :param type: Card type to filter by. Multiple types separated by ','.
        :param atk: ATK value to filter (use lt, lte, gt, gte).
        :param def_: DEF value to filter (use lt, lte, gt, gte).
        :param level: Card level/RANK to filter.
        :param race: Card race/type (e.g., Warrior, Insect). Multiple separated by ','.
        :param attribute: Card attribute (e.g., LIGHT, DARK). Multiple separated by ','.
        :param link: Link value to filter by.
        :param linkmarker: Link Marker value(s). Multiple separated by ','.
        :param scale: Pendulum Scale value to filter by.
        :param cardset: Card set (e.g., Metal Raiders, Soul Fusion).
        :param archetype: Archetype to filter by (e.g., Dark Magician, Blue-Eyes).
        :param banlist: Banlist to filter by (TCG, OCG, Goat).
        :param sort: Sort cards by (atk, def, name, type, level, id, new).
        :param format: Card format (tcg, goat, ocg goat, speed duel, master duel, rush duel, duel links).
        :param misc: Pass "yes" to show additional response info.
        :param staple: Check if card is a staple (boolean).
        :param has_effect: Check if card has an effect (boolean).
        :param startdate: Filter by release start date (YYYY-mm-dd).
        :param enddate: Filter by release end date (YYYY-mm-dd).
        :param dateregion: Region to filter release date by (tcg or ocg).
        :return: Card class instances.
        """
        # Prepare parameters dictionary
        params = {
            "id": id,
            "name": name,
            "fname": fname,
            "konami_id": konami_id,
            "type": type,
            "atk": atk,
            "def": def_,
            "level": level,
            "race": race,
            "attribute": attribute,
            "link": link,
            "linkmarker": linkmarker,
            "scale": scale,
            "cardset": cardset,
            "archetype": archetype,
            "banlist": banlist,
            "sort": sort,
            "format": format,
            "misc": misc,
            "staple": staple,
            "has_effect": has_effect,
            "startdate": startdate,
            "enddate": enddate,
            "dateregion": dateregion,
        }
        
        params = {k: v for k, v in params.items() if v is not None}
        print(f"Searching for cards with parameters: {params}")
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            card_data = response.json().get('data', [])
            # print the name of all cards found
            #for card in cards:
                #print(card.name)
            return card_data
        else:
            print(f"Error fetching card data: {response.status_code}")
            return None
        
