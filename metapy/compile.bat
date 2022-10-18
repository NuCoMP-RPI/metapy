javac -cp %~dp0\lib\* EntryPoint.java
echo compiled
python updateManifest.py
jar cfm EntryPoint.jar manifest.mf EntryPoint.class
echo jar created