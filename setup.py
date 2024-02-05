import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ticket_sales_to_spreadsheet",
    version="1.0.0",
    author="schef",
    author_email="",
    description="Ticket sales to spreadsheet",
    long_description=long_description,
    url="https://github.com/schef/ticket_sales_to_spreadsheet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ticket-sales-to-spreadsheet = ticket_sales_to_spreadsheet.main:run',
        ],
    },
    install_requires=[
        'selenium',
        'gspread',
        'google-api-python-client',
        'oauth2client'
    ],
)
