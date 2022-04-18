from setuptools import setup

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

reqs = parse_requirements('./requirements.txt')
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='korean_rule_helper',
    version='0.0.6',
    author='5yearsKim',
    author_email='hypothesis22@gmail.com',
    url='https://github.com/5yearsKim/koreanRuleHelper',
    project_url='https://pypi.org/project/korean-rule-helper/',
    description='한국어 rule-based 처리를 간단히',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['korean_rule_helper'],
    install_requires=reqs,
    # package_data={
    #   '': ['data/*']
    # }
)