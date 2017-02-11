import requests 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

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
    URL_NUTRIENT = BASE_URL + '/nutrients'
    QUERY_SUCCEED = 200
    
    margin_size = 1.3
    text_margin = 0.35
    
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
        
        return res
    
    @staticmethod
    def get_nutrient(name):
        """
        Look for specific product according to barcode. Return only the product
        """
        # Rend request
        res = requests.get(RequestOpenFood.URL_NUTRIENT, params={}, headers=RequestOpenFood.HEADERS)
        
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
        
        name_res = ['' for x in name]
        
        for nutrient in res['data']:
            name_nut = nutrient['attributes']['name-translations']['fr']
            unit_nut = nutrient['attributes']['unit']
            
            try:
                pos = [x for x in name.keys()].index(name_nut)
                name_res[pos] = unit_nut
            except ValueError:
                pass
        
        return name_res
    
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
                if text_scan is not None and name.lower() in text_scan.lower():
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
        
        try:
            in_nutrients = product['_source']['nutrients']
            for in_nutrient in in_nutrients:
                try:
                    nut_fr = in_nutrient['name_fr']
                    if name in nut_fr:
                        return True
                except KeyError:
                    pass
        except KeyError:
            pass
         
        return False
    
    
    def compare_data(p1, p2):
        dict_comp = {}
        dict_comp_tag = {}
        # Add nutirent for both ids
        for key in p1['nutrients']:
            val = key['per_hundred']
            try:
                dict_comp[key['name']][0] = float(val)
                dict_comp_tag[key['name']][0] = val
            except:
                dict_comp[key['name']] = [float(val), 0]
                dict_comp_tag[key['name']] = [val, '-']

        for key in p2['nutrients']:
            val = key['per_hundred']
            try:
                dict_comp[key['name']][1] = float(val)
                dict_comp_tag[key['name']][1] = val
            except:
                dict_comp[key['name']] = [0, float(val)]
                dict_comp_tag[key['name']] = ['-', val]

        # Plot according to dictionary
        val_p1 = []; val_p2 = []
        val_tag = []
        for key in dict_comp.keys():
            val_p1.append(dict_comp[key][0])
            val_tag.append(dict_comp_tag[key][0])
        for key in dict_comp.keys():
            val_p2.append(dict_comp[key][1])
            val_tag.append(dict_comp_tag[key][1])
        val_p1 = np.array(val_p1); val_p2 = np.array(val_p2); 
        max_val = np.max([val_p1, val_p2])
        val_p1 = val_p1/max_val
        val_p2 = val_p2/max_val
        
        fig=plt.figure()
        ax=fig.add_subplot(111)
        l = ax.barh(range(len(val_p1)), -val_p1, align='center', color='red')
        l2 = ax.barh(range(len(val_p2)), val_p2, align='center', color='blue')
        plt.xlim([-RequestOpenFood.margin_size, RequestOpenFood.margin_size])
        plt.axis('off')

        unit_data = RequestOpenFood.get_nutrient(dict_comp_tag)

        rects = ax.patches
        for i, (rect, label) in enumerate(zip(rects, val_tag)):
            height = rect.get_height()
            label_tag = label
            if label is not '-':
                label_tag = label +' ' + unit_data[i%len(val_p1)]
            if not (i < len(val_p1)):
                ax.text(rect.get_x() + rect.get_width() + 0.15, rect.get_y() + height/2, 
                        label_tag , ha='left', va='center', size='large')
            else:
                ax.text(rect.get_x() - 0.15 , rect.get_y() + height/2, 
                        label_tag, ha='right', va='center', size='large')
        for i, (rect, label) in enumerate(zip(rects, dict_comp_tag.keys())):
            height = rect.get_height()
            ax.text(RequestOpenFood.margin_size+RequestOpenFood.text_margin , rect.get_y() + height/2, label, ha='left', va='center', size='large')

        p1_name = p1['name']
        p2_name = p2['name']
        if len(p1_name) > 20:
            p1_name = p1_name[:20] + '...'
        if len(p2_name) > 20:
            p2_name = p2_name[:20] + '...'
            
        plt.legend([l, l2], [p1_name, p2_name], loc='upper center', bbox_to_anchor=(0.5, -0.05),
        fancybox=True, shadow=True, ncol=5)
        
        plt.savefig('foo.png', bbox_inches='tight')
        buf = io.BytesIO(open('foo.png','rb').read())
        
        #canvas=FigureCanvas(fig)
        #png_output = io.BytesIO()
        #canvas.print_png(png_output)
        #return png_output.getvalue()
        
        return buf.getvalue()
    
    "******************************************* Debug propuse *******************************************"
    
    @staticmethod
    def display_product_names(res):
        """
        Display product array or single product name
        """
        if isinstance(res, list):
            for i, product in enumerate(res):
                name = ProductBuilder.get_valid_name(product)
                print('\t'+str(i+1)+'.', name)
        else:
            name = ProductBuilder.get_valid_name(res)
            print('\t'+str(1)+'.', name)

import json

class ProductBuilder:
    
    def __init__(self, product):
        self.name = ''
        self.images = []
        # Get name
        try:
            self.name = ProductBuilder.get_valid_name(product)
        except QuerryError as err:
            self.name = 'None'
            print(err.message)
        # Get images
        try:
            self.images = ProductBuilder.get_valid_image(product)
        except QuerryError as err:
            print(err.message)
        # Get barcode
        self.barcode = ProductBuilder.get_valid_barcode(product)
        # Get composition
        self.nutrients = ProductBuilder.get_valid_nutrient(product)
        self.raw = product
        
    def get_json(self):
        res_dict = {}
        res_dict['name'] = self.name
        res_dict['barcode'] = self.barcode
        res_dict['images'] = self.images
        res_dict['nutrients'] = self.nutrients
        return res_dict
    
    @staticmethod
    def clean_data(res_tab):
        res = []
        for i, product in enumerate(res_tab):
            product_build = ProductBuilder(product)
            res.append(product_build.get_json()) 
        return res
    
    @staticmethod
    def get_valid_nutrient(product):
        """
        Get valid nutrient
        """
        nutrient_tab = [];
        try:
            nutirents = product['_source']['nutrients']
            for nutirent in nutirents:
                try:
                    name = nutirent['name_fr']
                    per_hundred = nutirent['per_hundred']
                    nutrient_tab.append({'name':name, 'per_hundred': per_hundred})
                except:
                    pass
        except KeyError:
            pass
        
        return nutrient_tab
        
    @staticmethod
    def get_valid_barcode(product):
        """
        Get valid barcode of product
        """
        try:
            return product['_source']['barcode']
        except KeyError:
            pass
        return '0'
    
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
    
