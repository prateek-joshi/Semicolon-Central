# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 21:47:26 2021

@author: Prateek

HOMEPAGE
"""

from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    



