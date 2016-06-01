#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app, db
from flask import request, render_template, url_for, session, flash, redirect
import datetime
from utils import logger

@app.route('/create_instance/<image_id>', methods=['GET', 'POST'])
def create_instance(image_id):
    logger.info(image_id)
    if request.method == 'POST':
        logger.info(image_id)
