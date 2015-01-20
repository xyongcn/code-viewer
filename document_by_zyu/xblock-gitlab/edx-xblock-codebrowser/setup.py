from setuptools import setup

setup(
    name='xblock-codebrowser',
    version='0.1',
    description='codebrowser xblock',
    py_modules=['codebrowser'],
    install_requires=['XBlock'],
    entry_points={
        'xblock.v1': [
            'codebrowser = codebrowser:CodeBrowserBlock',
        ]
    }
)
