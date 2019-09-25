import setuptools
import re, ast
    
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('re_map/__init__.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="re_map",
    version=version,
    author="Aleksas Pielikis",
    author_email="ant.kampo@gmail.com",
    description="Apply multiple regex patterns and keep change index map.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aleksas/re-map",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)