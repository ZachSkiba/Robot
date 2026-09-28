# 497 Project Documentation

## Week 1: Project Planning and Proposal Updates

I began the project by updating the project proposal and planning documentation to better reflect the direction of the robot project and the goals of the course. This included reviewing the project structure, refining the project scope, and improving the written planning materials so that the project objectives, development phases, and expected outcomes were clearly documented.

I also met with Professor Das to discuss the updated proposal and project plans. These meetings provided an opportunity to confirm that the project direction and planned work were appropriate for the course and to incorporate feedback into the project documentation and development plan.

As the project progressed, I continued revising the planning documentation. The 497 plan was reorganized into the project archive, related planning and phase documentation was refreshed, and additional professor-facing and proposal material was organized under the appropriate archive directories. A new proposal PDF and supporting documentation were also added.

## Week 2: Docker and Development Environment Improvements

After the initial proposal work, I focused on improving the project's development environment. The goal was to make the project easier to set up, reproduce, and use across different development systems.

I worked through issues with the Docker development container and VS Code integration, including container ownership, mounted directories, USB and `hidraw` access, and startup behavior. PlatformIO was added to the development container to support embedded firmware development, and the Python dependency configuration was reorganized into a more curated dependency file.

I also expanded the root README several times. The final version contains a substantially improved project overview, current project status, setup guidance, development workflow, and repository layout. This documentation was intended to make the project easier for both current contributors and future users to understand and reproduce.

## Week 3: Git Workflow and Repository Process

I then worked on improving the Git and GitHub workflow used for development. This included reviewing how project changes were tracked, documenting the development process more clearly, and establishing a workflow that reduced the risk of unstable changes being committed directly to the main branch.

Together with my brother, I created a development branch that could be used to test changes before merging them into `main`. There were several issues while determining the correct branch and container workflow, but after troubleshooting and testing, the process was working properly.

The Git workflow was also integrated with the Docker development-container setup. This created a more consistent development process in which changes could be made and tested inside the development environment before being incorporated into the main project.

I also expanded the Git workflow documentation and updated the project's next-step documentation.

## Week 4: Repository Cleanup and Organization

I performed a significant cleanup and reorganization of the repository to make it more professional, maintainable, and easier to navigate.

This included reorganizing files and directories, removing obsolete or unnecessary content, adding ignore rules for generated files, and repeatedly removing generated VS Code browse-database files and related editor artifacts. VS Code settings and C++ properties were also updated, and a `Robot.code-workspace` file was added to make opening the project more consistent.

Professor-facing and archival material was reorganized as well. The `For-Rosa` material was moved into the professor documentation area and subsequently normalized to the `for-professor-Das` directory naming convention. Class, proposal, planning, and archive documentation were also reorganized.

Some large repository changes involved line-ending normalization rather than substantive modifications. This affected portions of the August 21 documentation and source changes, as well as existing notebooks, simulation files, and log files. I identified these changes so that repository history would not incorrectly suggest that large amounts of source material had been rewritten.

## Teensy 4.1 and ESP32 Development

A major portion of the project involved establishing the embedded development workflow for the Teensy 4.1 and preparing the project to support ESP32 development in a similar manner.

I created an archived Teensy 4.1 / PlatformIO test project under:

`archive/platformio-tests/teensy41-basic`

This included the PlatformIO configuration, local VS Code settings, ignore rules, and workspace configuration needed to reproduce the test environment.

I also developed several pieces of diagnostic and benchmark firmware for the Teensy. These included tests for:

* Serial throughput
* Loop timing
* Timing and latency
* Calculation performance
* Firmware/update behavior
* Universal board diagnostics
* Test-suite and test-protocol functionality

The firmware-update testing was later replaced with more useful diagnostic firmware as the testing approach evolved.

Supporting materials were also added, including a Python test utility, board-test-results documentation, and updates to the universal-board test framework.

### Teensy Firmware Upload and USB Troubleshooting

One of the major technical issues encountered was uploading firmware from the Docker development container. PlatformIO could successfully build the firmware, but the upload process failed with:

```text
Found device but unable to open

Error opening USB device: Resource temporarily unavailable
```

The problem was traced to the Teensy being passed through multiple USB environments:

```text
Windows → WSL 2 → Docker Desktop → VS Code Dev Container
```

The Teensy HalfKay bootloader was visible, but the loader running inside Docker could not reliably obtain access to the USB device.

I changed the workflow so that the firmware was built inside the VS Code/Docker development environment, transferred to WSL, and then uploaded from WSL using `teensy_loader_cli`.

The resulting workflow was:

```text
VS Code / Docker
      │
      ▼
PlatformIO builds firmware.hex
      │
      ▼
Copy HEX to WSL
      │
      ▼
teensy_loader_cli in WSL
      │
      ▼
Teensy 4.1
```

The successful flash produced:

```text
Found HalfKay Bootloader

Programming..................

Booting
```

The Teensy subsequently appeared as:

```text
16c0:0483 Van Ooijen Technische Informatica Teensyduino Serial
```

I then verified the firmware through serial communication:

```text
Teensy 4.1 heartbeat
```

This confirmed that the physical Teensy, USB cable, WSL USB forwarding, firmware build process, flashing process, and serial communication were all functioning correctly.

I documented the complete Teensy and ESP32 setup process in `docs/setup/teensy-and-esp32.md`, including building firmware, transferring firmware, attaching the board through WSL, flashing, and verifying operation.

## Universal Board Diagnostics and Testing

After establishing the basic Teensy firmware workflow, I expanded the embedded testing work into a more comprehensive board-diagnostics and test-suite system.

The goal was to determine how much useful hardware validation could be performed using software alone, without requiring external test equipment. The resulting universal board test suite combines multiple diagnostic categories into a single firmware-based testing framework intended to work across Arduino-framework boards where the required core functionality is available.

The tests focus on characteristics that can be meaningfully evaluated through firmware, including timing behavior, loop performance, serial communication, computation performance, and general board operation.

This work also included developing a test protocol and supporting documentation so that test results could be recorded and compared systematically rather than relying only on visual confirmation that firmware uploaded successfully.

The diagnostic work is particularly important because it provides a repeatable baseline for evaluating both the Teensy and future ESP32 implementations before they are integrated into the larger robot system.

## Simulation and Data Organization

I also continued organizing and preserving simulation data generated during development. This included adding arm-dynamics CSV logs, including additional runs such as runs 8 and 9, as well as a complete second set of motor logs.

Existing notebooks, simulation files, and earlier simulation logs were retained and organized. Changes affecting many of these files were primarily line-ending normalization rather than changes to the underlying simulation content.

These artifacts provide a record of the simulation work and will allow later development to compare simulated behavior with measurements from the physical robot.

## 3D Printing and Material Research

Alongside the software and embedded development, I worked on establishing the manufacturing process that will be used for the robot's printed components.

I finished calibrating the filament and worked through the printer settings needed to obtain more consistent and repeatable results. This provides a more reliable foundation for producing functional mechanical prototypes rather than relying on uncalibrated default settings.

I also researched different filament materials and how they should be assigned to different robot components based on their mechanical properties.

The current material strategy is to use different materials for different engineering requirements rather than attempting to construct the entire robot from one filament:

| Material                  | Intended Use                                                         |
| ------------------------- | -------------------------------------------------------------------- |
| PETG                      | Initial prototypes and functional validation                         |
| PLA-CF                    | Stiffness-critical structural components                             |
| PC                        | High-load, tough, creep-sensitive, and higher-temperature components |
| PET-CF                    | Optional higher-performance structural material                      |
| TPU                       | Compliant components such as gripper pads and bumpers                |
| Steel                     | Shafts and fasteners                                                 |
| Commercial steel bearings | Important rotating joints                                            |
| Steel BBs                 | Rolling elements for large custom printed bearings                   |

The research showed that material selection must be based on the actual loading requirements of each component. PLA-CF is being considered primarily where stiffness and dimensional stability are important, while PC is being considered for components where toughness, strength, creep resistance, or temperature resistance are more important. PET-CF may be used selectively where its additional stiffness and strength justify the additional cost and printing considerations.

I also researched annealing and determined that it should not automatically be applied to every PLA-CF component. Structural components such as long arm beams and large non-precision plates may benefit from annealing, while bearing seats, gears, motor mounts, pulley bores, shaft bores, and other precision interfaces should generally not be annealed unless they will subsequently be machined and requalified.

The overall structural-print strategy also considers perimeter count, infill, print orientation, stress concentrations, bearing support, metal shafts, fasteners, and heat-set inserts. This is important because the mechanical performance of a printed robotic component depends on much more than the nominal strength of the filament.

## Mechanical Prototyping and Heat-Set Inserts

I printed a simple arbor press intended for installing heat-set threaded inserts into 3D-printed components.

This was a useful mechanical-development project because threaded inserts will allow printed components to use more reliable threaded connections than repeatedly threading directly into plastic. The arbor press provides a more controlled way to install the inserts consistently and reduces the risk of installing them at an angle or applying excessive force.

This work also supports the broader structural-printing strategy by allowing printed parts to incorporate mechanical fastening methods appropriate for higher-load robotic assemblies.

## 3D Scanning and Turntable Development

I researched and experimented with 3D scanning as a potential method for capturing physical objects and producing usable digital models.

I found Kiri Engine, a phone-based application capable of creating 3D scans from photographs. Although the free version has limitations compared with more advanced scanning solutions, it provides a practical way to experiment with object capture without requiring dedicated scanning hardware.

To improve the scanning process, I designed and built a simple turntable specifically for photographing objects from multiple angles. The turntable provides a controlled method for rotating an object while maintaining a consistent camera position and background.

The turntable was designed to make image capture more repeatable and to provide a cleaner background, which helps produce more consistent results during photogrammetry-based scanning.

I also worked on understanding the complete workflow for preparing an object, capturing the required images, processing the scan, and producing a usable model. This provides experience with a potential workflow for incorporating real-world objects into the robot's design and modeling process.

## Slip-Ring Research

I also performed an initial investigation into slip rings as a potential solution for transferring electrical power and signals through rotating joints.

The purpose of this research was to determine whether slip rings could be useful for robot joints where continuous or high-range rotation could otherwise cause wires to twist or become constrained.

The research was preliminary and focused on understanding the basic application requirements, including the number of electrical circuits required, current capacity, signal requirements, physical size, rotational requirements, and integration constraints. Further selection and testing will depend on the final mechanical architecture and electrical requirements of the robot.

## Additional Robotics Learning

In parallel with the direct project work, I continued studying robotics concepts through technical videos and educational material covering robotics hardware, software, mathematics, kinematics, dynamics, actuators, electronics, simulation, and artificial intelligence.

This work has been helping establish the background needed to connect the individual parts of the project together. Rather than treating the mechanical, electrical, embedded, and software systems as separate tasks, the goal is to develop an understanding of how they interact as one robotic system.

## Current Project Status

The project has progressed from primarily planning and repository setup into active development of the embedded, mechanical, manufacturing, and testing infrastructure.

The development environment and Git workflow have been established, the repository has been substantially reorganized, and the Teensy 4.1 firmware build, flashing, and serial communication workflow has been successfully validated. A reusable board-diagnostics and testing framework has also been developed to provide a systematic way of evaluating the embedded hardware.

On the mechanical side, filament calibration has been completed, material-selection research has been performed, a functional turntable for 3D scanning has been designed and built, and an arbor press for heat-set inserts has been printed and developed. Initial research has also been completed into bearings, lubrication, structural printing strategies, and slip-ring applications.

Simulation data and development artifacts have been organized so that future physical testing can be compared against previous simulation work.

The project is therefore moving into a phase where the established software, embedded, manufacturing, and mechanical foundations can begin supporting more substantial robot-system development and physical prototyping.
