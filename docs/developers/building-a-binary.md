# Building a binary

Builds are focused on Windows - but we have started to work on a MacOS build.&#x20;

**For Windows**

You need [nsis](http://nsis.sourceforge.io/) installed and install SimpleSC Plugin: [https://nsis.sourceforge.io/NSIS\_Simple\_Service\_Plugin](https://nsis.sourceforge.io/NSIS\_Simple\_Service\_Plugin). \
\
Then

```
pip install -r requirements.txt
pip install -r equirements-build.txt 
python build.py 
```

You will then get a setup.exe

