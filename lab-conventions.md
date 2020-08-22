# Addressing and conventions

## Services

<table>
  <tr>
   <td><strong>Service</strong>
   </td>
   <td><strong>Subnet</strong>
   </td>
   <td><strong>Scenario</strong>
   </td>
  </tr>
  <tr>
   <td>10</td>
   <td>10.0.10.0/24</td>
   <td>L2VPN</td>
  </tr>
  <tr>
   <td>15</td>
   <td>10.0.15.0/24</td>
   <td>L2VPN</td>
  </tr>
  <tr>
   <td>20</td>
   <td>10.0.20.0/24</td>
   <td>Asymmetric IRB</td>
  </tr>
  <tr>
   <td>25</td>
   <td>10.0.25.0/24</td>
   <td>Asymmetric IRB</td>
  </tr>
  <tr>
   <td>30</td>
   <td>10.0.30.0/24</td>
   <td>Asymmetric IRB</td>
  </tr>
  <tr>
   <td>40</td>
   <td>10.0.25.0/24</td>
   <td>Symmetric IRB</td>
  </tr>
  <tr>
   <td>45</td>
   <td>10.0.45.0/24</td>
   <td>Symmetric IRB</td>
  </tr>
  <tr>
   <td>50</td>
   <td>10.0.50.0/24</td>
   <td>Symmetric IRB</td>
  </tr>
  <tr>
   <td>55</td>
   <td>10.0.55.0/24</td>
   <td>Symmetric IRB</td>
  </tr>
  <tr>
   <td>60</td>
   <td>10.0.60.0/24</td>
   <td>Symmetric IRB</td>
  </tr>
  <tr>
   <td>Et4 - Leaf12</td>
   <td> 200.1.0.0/24<br>200.2.0.0/24</td>
   <td>L3VPN</td>
  </tr><tr>
   <td>100 - Leaf34</td>
   <td> 200.3.0.0/24<br>200.4.0.0/24</td>
   <td>L3VPN</td>
  </tr>
  <tr>
   <td>2002 - Leaf34</td>
   <td> 101.101.101.0/31 </td>
   <td>L3VPN</td>
  </tr>
</table>

## Addressing

<table>
  <tr>
   <td><strong>Use case</strong>
   </td>
   <td><strong>Block</strong>
   </td>
   <td><strong>Format</strong>
   </td>
  </tr>
  <tr>
   <td>P2P</td>
   <td>10.0.0.0/24</td>
   <td>/31 per link</td>
  </tr>
  <tr>
   <td>loopback (VXLAN)</td>
   <td>1.1.1.1/32<br>2.2.2.2/32</td>
   <td>per leaf pair</td>
  </tr>
  <tr>
   <td>MLAG (iBGP)</td>
   <td>172.16.0.0/31</td>
   <td>0 = A<br>1 = B<br>of MLAG pair</td>
  </tr>
  <tr>
   <td>loopback (EVPN)</td>
   <td>123.1.1.X/32</td>
   <td>BGP router-id<br>spine1/2 x=1/2<br>leaf1/2/3/4 x=3/4/5/6</td>
  </tr>
  <tr>
   <td>Gateway</td>
   <td>x.y.x.254/24</td>
   <td>Last Ip for virtual address</td>
  </tr>
  <tr>
   <td>P2P (L3VPN)</td>
   <td>100.0.0.0/8</td>
   <td>/31 per link</td>
  </tr>
</table>

## Others

<table>
  <tr>
   <td><strong>ID</strong>
   </td>
   <td><strong>Value</strong>
   </td>
  </tr>
  <tr>
   <td>RD</td>
   <td>Router ID : L2VNI (MAC-VRF)<br>Router ID : L3VNI (IP-VRF)</td>
  </tr>
  <tr>
   <td>RT</td>
   <td>VNI : VNI (for all)<br>VNI + VNI : VNI + VNI (vlan-aware) - 2030</td>
  </tr>
  <tr>
   <td>L2VNI</td>
   <td>VLAN ID : Service (VNI)</td>
  </tr>
  <tr>
   <td>L3VNI</td>
   <td>tenant-blue : 12345<br>tenant-green : 8888<br>tenant-yellow : 4444</td>
  </tr>
  <tr>
   <td>Hosts</td>
   <td>VRF = VLAN when testing</td>
  </tr>
  <tr>
   <td>vMAC</td>
   <td>aaaa.bbbb.cccc</td>
</table>