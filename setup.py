from setuptools import setup, find_packages

setup(
    name='SnippetManager',
    version='0.004',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
    ],
    entry_points={
        'console_scripts': [
            'snippet-manager = snippet_manager:main',
        ],
    },
    package_data={
        '': ['icons/*.png', 'snippet_settings.json'],
    },
    include_package_data=True,
    author='Your Name',
    author_email='your.email@example.com',
    description='A modern, light-themed application for managing code snippets and text notes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/snippet-manager',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
) 