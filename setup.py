from setuptools import setup

install_requires = [
    "cmdtree>=0.0.3",
    "RPi.GPIO>=0.6.0",
]

entry_points = {
        'console_scripts': ['pi-fan-tuner=pi_fan_tuner:main'],
    }

setup(
    name='PIFanTuner',
    version='0.0.1',
    py_modules=["pi_fan_tuner", ],
    install_requires=install_requires,
    entry_points=entry_points,
    url='https://github.com/winkidney/PIFanTuner',
    license='MIT',
    author='winkidney',
    author_email='winkidney@gmail.com',
    description='RaspberryPI CPU fan tuner with a s8050 Triode',
)
