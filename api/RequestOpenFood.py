import requests 

class QuerryError(Exception):
        
        BAD_REQUEST = 0x01
        BAD_KEY = 0x02
        NO_MATCHING = 0x03
        NO_NAME = 0x04

        def __init__(self, id_error, message):
            self.id_error = id_error
            self.message = message
            
class RequestOpenFood:

    BASE_URL='https://www.openfood.ch/api/v2'
    API_KEY='4c230279d7ab2cf2e1692497f44edc49'
    URL_SEARCH = BASE_URL + '/products/_search'
    QUERY_SUCCEED = 200
    
    HEADERS = {
        'Authorization': "Token token={}".format(API_KEY),
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }
    
    
    "******************************************* Querry DB *******************************************"
    @staticmethod
    def check_data(res):
        """ 
        Check if input stream is valid. Extrat product(s) from ElasticSearch DSL. Output is an array of product(s) 
        """
        # Check ir request succeed
        if (res.status_code != RequestOpenFood.QUERY_SUCCEED):
            raise QuerryError(QuerryError.BAD_REQUEST, 'Bad request')
        res = res.json()
        
        # Check if arguments failed
        try:
            res['error']
            raise QuerryError(QuerryError.BAD_KEY, 'Bad key')
        except KeyError:
            pass
        
        # Check if any results
        if(len(res['hits']['hits']) == 0):
            raise QuerryError(QuerryError.NO_MATCHING, 'No matching results')
            
        return res['hits']['hits']        
        
    @staticmethod
    def search_name(id_from=0, id_size=5, name=''):
        """
        Look for specific name along products. Will return n = id_size product containing the name. id_from is used
        to skip values
        """
        # Look for specific term
        query = {
            "from" : id_from, "size" : id_size,
            "query" : {
                  "terms" : { "name_translations.fr" : name}
               }
        }
        # Rend request
        r = requests.post(RequestOpenFood.URL_SEARCH, json=query, headers=RequestOpenFood.HEADERS)
        print(r)
        res = RequestOpenFood.check_data(r)
         
        return res
    
    @staticmethod
    def search_ingredient(id_from=0, id_size=5, name=''):
        """
        Look for specific ingredient along products. Will return n = id_size product containing the ingredient. 
        id_from is used to skip values
        """
        # Look for specific term
        query = {
            "from" : id_from, "size" : id_size,
            "query" : {
                "terms" : { "ingredients_translations.fr" : name}
               }
        }
        # Rend request
        r = requests.post(RequestOpenFood.URL_SEARCH, json=query, headers=RequestOpenFood.HEADERS)
        res = RequestOpenFood.check_data(r)
         
        return res
    
    @staticmethod
    def get_product(barcode=0):
        """
        Look for specific product according to barcode. Return only the product
        """
        query = {
            "query" : {
                  "term" : { "barcode": barcode }
               }
        }
        # Rend request
        r = requests.post(RequestOpenFood.URL_SEARCH, json=query, headers=RequestOpenFood.HEADERS)
        res = RequestOpenFood.check_data(r)
        
        return res[0]
    
    "******************************************* Extract product info *******************************************"
    @staticmethod
    def is_containing_ingredient(product=None, name=''):
        """
        Tell if product contains a specific ingredient
        """
        try:
            in_images = product['_source']['images']
            for in_image in in_images:
                text_scan = in_image['text']
                if name.lower() in text_scan.lower():
                    return True
        except KeyError:
            pass
        # Testing ingredients
        try:
            in_ingredient = product['_source']['ingredients_translations']
            for tag in in_ingredient:
                text_scan = in_ingredient[tag]
                if name.lower() in text_scan.lower():
                    return True
        except KeyError:
            pass
         
        return False
    
    @staticmethod
    def get_valid_name(product):
        """
        Get valid display name of product
        """
        name_fr = None
        try:
            name_fr = product['_source']['name_fr']
        except KeyError:
            pass
        if(name_fr is not None):
            return name_fr
        else:
            try:
                name_fr = product['_source']['name_translations']['fr']
                return name_fr
            except KeyError:
                pass
            try:
                name_fr = product['_source']['ingredients_translations']['fr']
                return name_fr
            except KeyError:
                raise QuerryError(QuerryError.NO_NAME, 'No name found')
        return 'No name'
    
    @staticmethod
    def get_valid_image(product, size='large'):
        """
        Get valid display name of product
        """
        img_valid_url = []
        try:
            imgs = product['_source']['images']
            for img in imgs:
                img_valid_url.append(img['data'][size]['url'])
        except KeyError:
            pass
        
        return img_valid_url
    
    "******************************************* Debug propuse *******************************************"
    
    @staticmethod
    def display_product_names(res):
        """
        Display product array or single product name
        """
        if isinstance(res, list):
            for i, product in enumerate(res):
                name = RequestOpenFood.get_valid_name(product)
                print('\t'+str(i+1)+'.', name)
        else:
            name = RequestOpenFood.get_valid_name(res)
            print('\t'+str(1)+'.', name)

