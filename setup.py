import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sonarqube",
    version="1.0.0",
    author="David RACODON",
    author_email="david.racodon@linty-services.com",
    description="SonarQube API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Linty-Services/sonarqube-api",
    project_urls={
        "Bug Tracker": "https://github.com/Linty-Services/sonarqube-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Proprietary",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=['sonarqube']),
    python_requires=">=3.8",
)
