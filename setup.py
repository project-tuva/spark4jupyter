from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='scala_spark_plugin',
    version='0.0.1',
    author='Timoteo Colnaghi',
    author_email='',
    py_modules=['scala_spark_plugin', 'v0.v0', 'common.helper','common.settings'],
    url='https://github.com/project-tuva/spark4jupyter.git',
    license='FreeBSD',
    description='Jupyter notebook plugin to run scala and scala-spark code'
    # long_description=open('README.md').read(),
)
