# Weighted Round Robin Load Balancing in Mini-NDN using Inherent Topology                                         
## What is Weighted Round Robin?
Weighted Round Robin is an advanced load balancing technique employed in network scheduling. Weighted Round Robin takes into account the processing power or ‘weight’ of each server in the network. This means that a server with a higher weight, indicating superior capacity, is assigned a larger share of the requests compared to a server with a lower weight.This method of load distribution is more efficient as it aligns the workload with the server’s capacity, thereby enhancing network performance and user experience. It also minimizes the likelihood of server overload by preventing any single server from being overwhelmed with requests, ensuring a balanced and efficient network operation [1].

<p align="center">
  <img src="https://www.mdpi.com/sensors/sensors-20-07342/article_deploy/html/images/sensors-20-07342-g002.png" width="700"/>
</p>

<br>
<p>Disusun oleh: Kelompok 2</p>
<table border = "1">
  <tr>
    <td><b>NIM</b></td>
    <td><b>Nama</b></td>
  </tr>
  
   <tr>
    <td>18121019</td>
    <td>Syah Muafa Al Kautsar</td>
  </tr>

  <tr>
    <td>18121021</td>
    <td>Albert</td>
  </tr>
  
  <tr>
    <td>18121024</td>
    <td>Gatra Akhira</td>
  </tr>
  
  <tr>
    <td>18121034</td>
    <td>Muhammad Arrifqi</td>
  </tr>

  <tr>
    <td>18121040</td>
    <td>Achmad Kabir Rifa’i</td>
  </tr>
</table>

## How to run
`sudo python src/main.py topology/inherent.conf`

## Notes:
kalau mau edit di branch `dev` dulu kemudian pull request ke `main'

### References
[1] https://webhostinggeeks.com/blog/what-is-weighted-round-robin/
