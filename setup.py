from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='FloydMind', 
    version='3.12.7', 
    author='Haojie Liu, Zihan Lin, Qinlin Lin',  
    author_email='200310074213l@gmail.com',  
    packages=find_packages(), 
    install_requires=requirements,  # Dependencies from requirements.txt
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update license if different
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12'
)
