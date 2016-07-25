from setuptools import setup


setup(
	name='tiny',
	version='0.1',
	py_modules=['tiny'],
	install_requires=[
		'click',
		'tinify',
	],
	entry_points='''
		[console_scripts]
		tiny=tiny:cli
	''',
)