from .Models import Category
from .Extension import db


def seedCategories():
    if Category.query.count() == 0:
        categories = {
            Category(name="Ficción"),
            Category(name="No Ficción"),
            Category(name="Misterio"),
            Category(name="Romance"),
            Category(name="Horror"),
            Category(name="Arte"),
            Category(name="Deportes"),
            Category(name="Guerra"),
        }
        db.session.bulk_save_objects(categories)
        db.session.commit()
        print("Categories seeded successfully")
    else:
          print("Categories already seeded, skipping.")


def runSeeders():
    seedCategories()
