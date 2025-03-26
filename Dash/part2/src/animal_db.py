from src.base_db import BaseDB
import pandas as pd

PATH_DB = 'data/animals.sqlite'

class AnimalDB(BaseDB):
    def __init__(self):
        super().__init__(path=PATH_DB, create=True)
        if not self._existed:
            pass
        return
    
    def get_category_list(self) -> list:
        return self.run_query("SELECT category FROM tCategory;")['category'].tolist()
    
    def get_subcategory_list(self, category: str) -> list:
        return self.run_query("SELECT subcategory FROM tSubcategory WHERE category = :category;", 
                              {'category': category})['subcategory'].tolist()
    
    def get_item_list(self, 
                      category: str, 
                      subcategory: str
                      ) -> list:
        sql = """
            SELECT name
            FROM tAnimal
            WHERE category = :category
              AND subcategory = :subcategory
        ;"""
        params = {'category': category,
                  'subcategory': subcategory
                  }
        return self.run_query(sql, params)['name'].tolist()
    
    def get_data(self,
                 category: str = None,
                 subcategory: str = None,
                 animal: str = None
                 ) -> pd.DataFrame:
        
        if category == '':
            category = None
        if subcategory == '':
            subcategory = None
        if animal == '':
            animal = None
        
        params = {
            'category': category,
            'subcategory': subcategory,
            'name': animal
            }
        if animal is not None:
            sql = """
            SELECT x, y
            FROM tData
            WHERE name = :name
            ;"""
        elif subcategory is not None:
            sql = """
            WITH
            Animals as
            (
                SELECT name
                FROM tAnimal
                WHERE category = :category
                  AND subcategory = :subcategory
            )

            SELECT x, y
            FROM tData
            JOIN Animals USING(name)
            ;"""
        elif category is not None:
            sql = """
            WITH 
            Animals as
            (
                SELECT name
                FROM tAnimal
                WHERE category = :category
            )
            SELECT x, y
            FROM tData
            JOIN Animals USING(name)
            ;"""
        else:
            sql = """
            SELECT x, y
            FROM tData
            ;"""

        return self.run_query(sql, params)