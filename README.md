# DIY Udoo Quad Distributed Computing Cluster

<img src="https://raw.githubusercontent.com/Ballistyxx/eliferrara/master/assets/Distributed-Computing/full-assembly.webp" alt="Distributed Computing Cluster" width="50%" ALIGN="left" HSPACE="0" VSPACE="20"/>

<img src="https://raw.githubusercontent.com/Ballistyxx/eliferrara/master/assets/Distributed-Computing/udoo-quad-top.webp" alt="Cluster Desktop Screenshot" width="50%" ALIGN="right" HSPACE="0" VSPACE="120"/>

## Overview
This project is a **DIY Distributed Computing Cluster** built from **13 Udoo Quad SBCs**, running **Armbian Linux**, and tied together with custom 3D-printed enclosures, a cooling manifold, and a custom-built power distribution board.

✨ **Read the full blog post here:** [Building a Distributed Computing Cluster with Udoo Quads](https://eliferrara.com/2025/04/26/Distributed-Computing.html)

## Features
✔ **13-node Parallel Computing Cluster**  
✔ **Armbian 21.08.5 (XFCE)** running on each node  
✔ **MPICH + MPI4Py** installed for distributed Python programs  
✔ **Custom-built power distribution board** for compact wiring  
✔ **3D-printed modular frame** with airflow-optimized cooling  
✔ **Centralized controller with Python GUI management**

## Files

- main.py: main GUI file
- md5_attack.py: MD5 cracker using MPI
- machinefile: list of all IP addresses on the clusters local network

- Due to the large filesize (>1GB), full-assembly.stl is not included in /stl. Please convert from the substantially smaller full-assembly.step file.

### Cluster Overview


## Hardware Components
- **13x Udoo Quad Single Board Computers**
- **2x 8-port TRENDnet TEG-S80g Gigabit Switches**
- **300W 12V Power Supply**
- **120mm Cooling Fan + Custom 3D-printed Manifold**
- **Custom-made Power Distribution Board**
- **14x Ethernet Cables (~12 inches each)**
- **13x 8/16GB MicroSD Cards**
- **Wire, Connectors, JST and Molex Pins, Protoboard**

## Software & Code
The cluster uses **Armbian Linux** running **MPICH** for parallel message passing and **MPI4Py** for Python compatibility. Custom scripts allow:

- **Parallel execution of Python programs**
- **GUI-based board management (status, SSH access, file transfers)**
- **Automatic SSH key setup for passwordless communication**

### Example MPI Test
```bash
mpiexec -f machinefile -n 13 hostname
```

### Python GUI Control Panel
- Monitor board temperatures and uptime
- Push code updates globally
- Open SSH terminals from a simple interface

## 3D Printing Files & PCB Design
All **STL**, **STEP**, and **library** are provided in this repository.


🖌️ **Onshape CAD Models:** [Onshape Project](https://cad.onshape.com/documents/75f5671b78b346b758aa2efd/w/f36d5c58d0108a32ef1fbe4a/e/eaaa6f714bb4dcef7b77a385?renderMode=0&uiState=680d96a28b51db61358ac1d3)

## Setup
1. Flash **Armbian 21.08.5 XFCE** to each SD card.
2. Install MPICH and MPI4Py.
3. Setup SSH key exchange between all nodes.
4. Define `machinefile` listing all IP addresses.
5. Launch programs across the cluster using `mpiexec`.

### Networking
- Nodes interconnected via two 8-port switches.
- Static IPs assigned for easier configuration.

### Power Distribution
- 300W 12V PSU feeds each board through custom-made JST connectors.
- All boards mounted with 3D-printed supports.

## Known Limitations & Future Improvements
⚠ **Performance Gains Limited** — Only ~2x speedup observed; bottlenecked by network overhead and Python interpreter.  
⚠ **Hardware Fragility** — Two boards damaged due to passive overheating.  
⚠ **Control Circuit Issues** — Initial design overheated voltage regulators; needs proper buck converters.

### Future Ideas
- Upgrade to Kubernetes or Docker Swarm.
- Stronger 3D-printed base frame.
- Improved software parallelism (cryptomining, matrix ops).

## License
This project is open-source under the **MIT License**.

## Author
Developed by **Ballistyxx**  
📧 **Contact:** [GitHub Issues](https://github.com/Ballistyxx/udoo-distributed-computer/issues)

---

✨ **If you like this project, consider giving it a ⭐ on GitHub!**