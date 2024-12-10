from setuptools import setup, find_packages

setup(
    name='xui_api',
    version='0.1.0',
    description='Модуль для взаимодействия с XUI API, включая управление входящими соединениями и клиентами.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Ваше Имя',
    author_email='timoxa.m.is@icloud.com',
    url='https://github.com/yourusername/asynxui',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'pydantic',
        'pytest',
        'aioresponses'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)
