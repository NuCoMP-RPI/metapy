# Copy language server build
#cp -r /home/peter/eclipse2022/MCNP-LS/gov.lanl.mcnp.parent/gov.lanl.mcnp.ide/build/install/gov.lanl.mcnp.ide/lib /home/peter/Research/mm_server_api/metapy

cp -r /home/peter/eclipse2022/Serpent-LS/fi.vtt.serpent.parent/fi.vtt.serpent.ide/build/install/fi.vtt.serpent.ide/lib /home/peter/Research/mm_server_api/metapy

# Recompile EntryPoint.jar
cd /home/peter/Research/mm_server_api/metapy
bash compile.sh

# Rebuild wheel
cd ../
python setup.py bdist_wheel

# Uninstall metapy
printf "y" | pip uninstall metapy

# Install new wheel
pip install ./dist/metapy-0.0.0-py3-none-any.whl
