"""
Vercel serverless entry point.

Vercel's @vercel/python builder requires a WSGI `app` object in this file.
All routes are forwarded here via vercel.json.
"""
from app import create_app

app = create_app("vercel")
