import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-akretion-geonames-import-simple",
    description="Meta package for akretion-geonames-import-simple Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-base_address_extended_geonames_import>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
