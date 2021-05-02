# This mocks a database that can be hosted locally or remotely by storing images metadata in a dictionary
import re


class mock_db:
    def __init__(self):
        # This is some examples of existing images in the mock database
        self.db = [
            {
                'id': 0,
                'title': 'fruit basket',
                'image_url': 'fruit_basket_image.jpeg',
                'category': ['fruit', 'item']
            },
            {
                'id': 1,
                'title': 'watermelon',
                'image_url': 'watermelon.jpeg',
                'category': ['fruit', 'item']
            },
            {
                'id': 2,
                'title': 'league of legends festival',
                'image_url': 'league_festival.jpeg',
                'category': ['game', 'character']
            },
            {
                'id': 3,
                'title': 'cs go dragon lore',
                'image_url': 'dragon_lore.jpeg',
                'category': ['game', 'weapon']
            },
            {
                'id': 4,
                'title': 'nba 2k20',
                'image_url': 'nba2k.jpeg',
                'category': ['game', 'basketball', 'character', 'human']
            },
            {
                'id': 5,
                'title': 'kyrie irving',
                'image_url': 'kyrie.jpg',
                'category': ['basketball', 'human']
            },
            {
                'id': 6,
                'title': 'naruto',
                'image_url': 'naruto.png',
                'category': ['character','cartoon']
            }
        ]
        # This can be another db called (image_category_detail) and stores the referrence of the image ids in json format 
        self.category_db = {
            'fruit': [0, 1],
            'item': [0, 1],
            'game': [2,3,4],
            'character': [2, 4, 6],
            'weapon': [3],
            'basketball': [4, 5],
            'human': [4, 5],
            'cartoon': [6],
        }

    def search(self, keys: list) -> list:
        result_images = []
        # if the key provided by the user is a key in category_db, it can speed up the runtime
        for key in keys:
            key = key.strip()
            if key in self.category_db:
                for image in self.category_db[key]:
                    if image not in result_images:
                        result_images.append(image)
            # Then check the key is a title, this process takes O(n) time, alternative way would be storing all the titles in another
            # db but if space is costy we can use this method
            else:
                for image in self.db:
                    # not breaking from here because there's possibility for two images having the same title
                    if re.search(key, image['title']):
                        result_images.append(image['id'])
        return result_images
    
    def data_from_id(self, image_id):
        if isinstance(image_id, int):
            return self.db[image_id]
        else:
            return [self.db[image] for image in image_id]
    
    
    def home_page(self):
        return self.db