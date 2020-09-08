# Bonus : get wireshark working with streaming from device

Note : need to recompile entirely wireshark because centos repository is containing a very old version of wireshark

- Connect to lab vm thru guacamole

- Install gcc compilator

```
sudo yum install wget gcc gcc-c++
sudo yum install libgcrypt-devel
```

- Get Wireshark source
  
```
cd ~/Downloads
wget https://2.na.dl.wireshark.org/src/wireshark-3.0.6.tar.xz
tar xvf wireshark-3.0.6.tar.xz
mkdir build
cd build
sudo ../wireshark-3.0.6/tools/rpm-setup.sh --install-optional
```

- Uninstall cmake prviously installed by the wireshark script

`sudo yum remove cmake`

- Install right version of cmake (3.15.5)

```
cd ~
wget https://cmake.org/files/v3.15/cmake-3.15.5.tar.gz
tar zxvf cmake-3.15.5.tar.gz
cd cmake-3.15.5
./bootstrap --prefix=/usr/local
make -j$(nproc)
sudo make install
```

- Close terminal and Open new terminal => Check cmake => shoud be 3.15.5

```
cmake --version
--> cmake version 3.15.5
```

- Finish wireshark install

```
cd ~/Downloads
cmake wireshark-3.0.6
make
sudo make install
```

- unlog / log again because of guacamole screen stuff

- Stream tcpdump from device 

`ssh admin@leaf1 “bash tcpdump -s 0 -Un -w - -i et2” | wireshark -k -i -`

(don't forget to enter device passwor `arista`)