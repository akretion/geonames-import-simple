import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-akretion-geonames-import-simple",
    description="Meta package for akretion-geonames-import-simple Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-base_address_city_geonames_import',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
